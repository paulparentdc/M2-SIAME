import time
import json
import threading
import paho.mqtt.client as mqtt_client
import os
import sys
import connect
import logging    
import signal
import RPi.GPIO as GPIO


# #############################################################################
#
# Global Variables
#
MQTT_SERVER="192.168.0.214"
MQTT_PORT=1883
# Full MQTT_topic = MQTT_BASE + MQTT_TYPE



MQTT_PUB_TEMP = "1R1/014/temperature"
MQTT_PUB_LIGHT = "1R1/014/luminosity"
MQTT_PUB_SHUTTER = "014/shutter/command"


MQTT_SUB_T = "1R1/014/temperature"
MQTT_SUB_L = "1R1/014/luminosity"
MQTT_SUB_SHUTTER = "014/shutter/"


MQTT_QOS=0 # (default) no ACK from server
#MQTT_QOS=1 # server will ack every message

MQTT_USER=""
MQTT_PASSWD=""


client      = None
timer       = None
log         = None
__shutdown  = False


lumi_min = 400
lumi_max = 1200
ampoule_on = False
shutter_state = None
moving = False

luminosity = None
temperature = None


def ask_status():
    print("Dis moi qui tu es ")
    jsonFrame = { }
    jsonFrame['dest'] = "all"
    jsonFrame['order'] = "status"
    client.publish(MQTT_PUB_SHUTTER, json.dumps(jsonFrame), MQTT_QOS)

def open_shutter():
    jsonFrame = { }
    jsonFrame['dest'] = "all"
    jsonFrame['order'] = "up"
    client.publish(MQTT_PUB_SHUTTER, json.dumps(jsonFrame), MQTT_QOS)

def close_shutter():
    jsonFrame = { }
    jsonFrame['dest'] = 'all'
    jsonFrame['order'] = 'down'
    client.publish(MQTT_PUB_SHUTTER, json.dumps(jsonFrame), MQTT_QOS)


def on_ampoule():
    global ampoule_on
    GPIO.output(12, GPIO.HIGH)
    ampoule_on = True

def off_ampoule():
    global ampoule_on
    GPIO.output(12, GPIO.LOW)
    ampoule_on = False



#
# Function ctrlc_handler
def ctrlc_handler(signum, frame):
    global __shutdown
    log.info("<CTRL + C> action detected ...");
    __shutdown = True
    # Stop monitoring
    stopMonitoring()

#
# Function stoping the monitoring
def stopMonitoring():
    global client
    global timer
    log.info("[Shutdown] stop timer and MQTT operations ...");
    timer.cancel()
    timer.join()
    del timer
    client.unsubscribe(MQTT_SUB_L)
    client.unsubscribe(MQTT_SUB_T)
    client.unsubscribe(MQTT_SUB_SHUTTER)
    client.disconnect()
    client.loop_stop()
    del client



# --- MQTT related functions --------------------------------------------------
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global mesure_interleave,moving
    log.info("Connected with result code : %d" % rc)

    if( rc == 0 ):
        log.info("subscribing to topic: %s" % MQTT_SUB_T)
        # Subscribe to topic
        client.subscribe(MQTT_SUB_T)
        client.subscribe(MQTT_SUB_L)
        client.subscribe(MQTT_SUB_SHUTTER)

# The callback for a received message from the server.
def on_message(client, userdata, msg):
    global temp_interleave, light_interleave, interrupt_mode, capture, luminosity, temperature, shutter_state
    ''' process incoming message.
        WARNING: threaded environment! '''
    payload = json.loads(msg.payload.decode('utf-8'))
    log.debug("Received message '" + json.dumps(payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

    if(msg.topic == MQTT_SUB_L):
        luminosity = int(payload['value'])
        manage()

    elif((msg.topic == MQTT_SUB_T)):
        temperature = payload['value']
        manage()

    elif((msg.topic == MQTT_SUB_SHUTTER)):
        shutter_state = payload["status"]
        manage()


    log.warning("TODO: process incoming message!")




def manage():
    global moving, shutter_state

    print("Etat volet :")
    print(shutter_state)
    print("Moving :")
    print(moving)
    print("Luminosity :")
    print(luminosity)
    print("Ampoule allumé :")
    print(ampoule_on)
    
    if (shutter_state == "CLOSED" or shutter_state == "OPEN"):
        moving = False

    if(luminosity < lumi_min) : # not enough light
        print("Pas assez de lumière !")
        if(shutter_state != "OPEN" and moving == False): 
            print("Envoie ouverture vollet")
            open_shutter()
            moving = True
        elif(shutter_state == "OPEN" and ampoule_on == False): # Last option is switching on the light
            print("Allume ampoule")
            on_ampoule()

    elif ( luminosity > lumi_max): # Too much light
        print("Trop de lumière !!!")
        if (ampoule_on == True) :
            print("Eteind ampoule")
            off_ampoule()
        elif(shutter_state != "CLOSED" and moving == False ):
            print("Envoie fermeture vollet")
            close_shutter()
            moving = True

    else : # light is real goooood ;)
        print("Lumière ok")
        if (ampoule_on == True) :
            print("Eteind ampoule")
            off_ampoule()



# The callback to tell that the message has been sent (QoS0) or has gone
# through all of the handshake (QoS1 and 2)
def on_publish(client, userdata, mid):
    log.debug("mid: " + str(mid)+ " published!")

def on_subscribe(mosq, obj, mid, granted_qos):
    log.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    log.debug(string)


# #############################################################################
#
# MAIN
#

def main():

    # Global variables
    global client, timer, log

    # GPIO ampoule setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.OUT)
    GPIO.output(12, GPIO.LOW)

    # Trap CTRL+C (kill -2)
    signal.signal(signal.SIGINT, ctrlc_handler)

    # MQTT setup
    client = mqtt_client.Client( clean_session=True, userdata=None )
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    if len(MQTT_USER)!=0 and len(MQTT_PASSWD)!=0:
        client.username_pw_set(MQTT_USER,MQTT_PASSWD); # set username / password

    # Start MQTT operations
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    client.loop_start()

    ask_status()

    # Launch Acquisition & publish sensors till shutdown
    while(1):
        pass

    # waiting for all threads to finish
    if( timer is not None ):
        timer.join()


# Execution or import
if __name__ == "__main__":

    # Logging setup
    logging.basicConfig(format="[%(asctime)s][%(module)s:%(funcName)s:%(lineno)d][%(levelname)s] %(message)s", stream=sys.stdout)
    log = logging.getLogger()

    print("\n[DBG] DEBUG mode activated ... ")
    log.setLevel(logging.DEBUG)
    #log.setLevel(logging.INFO)

    # Start executing
    main()


# The END - Jim Morrison 1943 - 1971
#sys.exit(0)