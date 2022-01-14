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



MQTT_PUB = "1R1/014/presence"



MQTT_QOS=0 # (default) no ACK from server
#MQTT_QOS=1 # server will ack every message

MQTT_USER=""
MQTT_PASSWD=""


client      = None
timer       = None
log         = None
__shutdown  = False

present = True



def send_present():
    jsonFrame = { }
    jsonFrame['dest'] = "all"
    jsonFrame['value'] = True
    client.publish(MQTT_PUB, json.dumps(jsonFrame), MQTT_QOS)

def send_absent():
    jsonFrame = { }
    jsonFrame['dest'] = "all"
    jsonFrame['value'] = False
    client.publish(MQTT_PUB, json.dumps(jsonFrame), MQTT_QOS)




# --- MQTT related functions --------------------------------------------------
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global mesure_interleave,moving
    log.info("Connected with result code : %d" % rc)

    if( rc == 0 ):
        log.info("subscribing to topic: " )
        # Subscribe to topi

# The callback for a received message from the server.
def on_message(client, userdata, msg):
    ''' process incoming message.
        WARNING: threaded environment! '''
    payload = json.loads(msg.payload.decode('utf-8'))
    log.debug("Received message '" + json.dumps(payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

    log.warning("TODO: process incoming message!")



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
    global client, timer, log,present
    but_pushed = False

    # GPIO ampoule setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  

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

    # Launch Acquisition & publish sensors till shutdown
    while(1):
        if GPIO.input(6) :
            but_pushed = True
        elif (but_pushed == True):
            but_pushed = False
            if present == True:
                present = False
                send_absent()
                print("Absent !!!!")
            else :
                present = True
                send_present()
                print("Present !!!!")

            

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