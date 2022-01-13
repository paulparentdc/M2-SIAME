#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Thiebolt  aug.19  updated
# Francois  apr.16  initial release
#


# #############################################################################
#
# Import zone
#
import errno
import os
import signal
import syslog
import sys
import RPi.GPIO as GPIO
import time

import threading
import json

import random

import logging

# MQTT related imports
import paho.mqtt.client as mqtt

from libutils.rpi_utils import getmac

#I2C related imports
from smbus2 import SMBus
import Adafruit_MCP9808.MCP9808 as MCP9808


# #############################################################################
#
# Global Variables
#
MQTT_SERVER="192.168.0.214"
MQTT_PORT=1883
# Full MQTT_topic = MQTT_BASE + MQTT_TYPE
MQTT_BASE_TOPIC = "1R1/014"
MQTT_TYPE_TOPIC = "temperature"
MQTT_PUB_TEMP = "1R1/014/temperature"
MQTT_PUB_LIGHT = "1R1/014/luminosity"


MQTT_SUB_T = "1R1/014/temperature/command"
MQTT_SUB_L = "1R1/014/luminosity/command"

MQTT_QOS=0 # (default) no ACK from server
#MQTT_QOS=1 # server will ack every message

MQTT_USER=""
MQTT_PASSWD=""

# Measurement related
# seconds between each measure.
light_interleave = 10
temp_interleave = 10
light_INTER = 10

client      = None
timer       = None
log         = None
__shutdown  = False


bus = SMBus(1)

#Address of I2C devices
devices = []

#Sorted address of I2C devices
temps  = []
lights = []
others = []

#Sensors created using Adafruit library
sensorsT = []


# #############################################################################
#
# Functions
#
def interrupt(self):
    global bus
    print("Interrupt")
    publishlight()
    bus.write_byte_data(lights[0],0xC0,0x00)



#SRF08 REQUIRES 5V
def scan(force=False):
    devices = []
    for addr in range(0x03, 0x77 + 1):
        read = SMBus.read_byte, (addr,), {'force':force}
        write = SMBus.write_byte, (addr, 0), {'force':force}

        for func, args, kwargs in (read, write):
            try:
                with SMBus(1) as bus:
                    data = func(bus, *args, **kwargs)
                    devices.append(addr)
                    break
            except OSError as expt:
                if expt.errno == 16:
                    # just busy, maybe permanent by a kernel driver or just temporary by some user code
                    pass
    return devices


def taxonomy(devices):
    global lights,temps,others
    for d in devices:
        if d == 57:
            lights.append(d)
        elif d>=24 and d<=31:
            temps.append(d)
        else:
            others.append(d)


def readLight(address):
    bus.write_byte_data(address, 0x08, 0x03)
    time.sleep(0.05)
    val = bus.read_word_data(address, 0xAC)    
    return val

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
    client.disconnect()
    client.loop_stop()
    del client

#
# threading.timer helper function
def do_every_temp (worker_func, iterations = 0):
    global timer, temp_interleave
    # launch new timer
    if ( iterations != 1):
        timer = threading.Timer (
                        temp_interleave,
                        do_every_temp, [ worker_func, 0 if iterations == 0 else iterations-1])
        timer.start();
    # launch worker function
    worker_func();


def do_every_light (worker_func, iterations = 0):
    global timer, light_interleave
    # launch new timer
    if ( iterations != 1):
        timer = threading.Timer (
                        light_interleave,
                        do_every_light, [ worker_func, 0 if iterations == 0 else iterations-1])
        timer.start();
    # launch worker function
    worker_func();


# --- MQTT related functions --------------------------------------------------
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global mesure_interleave
    log.info("Connected with result code : %d" % rc)

    if( rc == 0 ):
        log.info("subscribing to topic: %s" % MQTT_SUB_T)
        # Subscribe to topic
        client.subscribe(MQTT_SUB_T);
        client.subscribe(MQTT_SUB_L);

# The callback for a received message from the server.
def on_message(client, userdata, msg):
    global temp_interleave, light_interleave
    ''' process incoming message.
        WARNING: threaded environment! '''
    payload = json.loads(msg.payload.decode('utf-8'))
    log.debug("Received message '" + json.dumps(payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))
    if(msg.topic == MQTT_SUB_T):
        if(payload['order'] == "frequency"):
            log.debug("Frequency will be set to %s" % (payload['value']))
            temp_interleave = int(payload['value'])
        elif(payload['order'] == "capture"):
            log.debug("Start an immediate capture")
            do_every_temp(publishTemp, 1)

    elif((msg.topic == MQTT_SUB_L) and (payload['dest'] == str(getmac()))):
        if(payload['order'] == "frequency"):
            log.debug("Frequency will be set to %s" % (payload['value']))
            light_INTER = int(payload['value'])
        elif(payload['order'] == "capture"):
            log.debug("Start an immediate capture")
            do_every_light(publishlight, 1)
    log.warning("TODO: process incoming message!")


# The callback to tell that the message has been sent (QoS0) or has gone
# through all of the handshake (QoS1 and 2)
def on_publish(client, userdata, mid):
    log.debug("mid: " + str(mid)+ " published!")

def on_subscribe(mosq, obj, mid, granted_qos):
    log.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    log.debug(string)


# --- neOCampus related functions ---------------------------------------------
# Acquire sensors and publish
def publishlight():

    light = readLight(lights[0])
    jsonFrame = { }
    jsonFrame['unitID'] = str(getmac())
    jsonFrame['subID'] = str(lights[0])
    jsonFrame['value'] = str(light)
    jsonFrame['value_units'] = 'lux'
    # ... and publish it!
    client.publish(MQTT_PUB_LIGHT, json.dumps(jsonFrame), MQTT_QOS)

def publishTemp():
    global sensorsT
    for add, t in sensorsT:
        temp = t.readTempC()
        # generate json payload
        jsonFrame = { }
        jsonFrame['unitID'] = str(getmac())
        jsonFrame['subID'] = str(add)
        jsonFrame['value'] = str(temp)
        jsonFrame['value_units'] = 'celsius'
        # ... and publish it!
        client.publish(MQTT_PUB_TEMP, json.dumps(jsonFrame), MQTT_QOS)


# #############################################################################
#
# MAIN
#

def main():

    # Global variables
    global client, timer, log

    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(13,GPIO.FALLING,callback=interrupt)

    # Sensors setup
    devices = scan(force=True)
    taxonomy(devices)

    for d in temps:
        sensor = MCP9808.MCP9808(address=d, busnum=1)
        sensorsT.append({d, sensor})
        sensor.begin()

    print("Lights :")
    print(lights)
    print("Temps :")
    print(temps)


    # Trap CTRL+C (kill -2)
    signal.signal(signal.SIGINT, ctrlc_handler)

    # MQTT setup
    client = mqtt.Client( clean_session=True, userdata=None )
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

    if (light_INTER <= 0): # MODE INTERRUPT

        light_interleave = 1200 # 20 min
        #write into the interrupt register
        bus.write_byte_data(lights[0],0x86,0x11)

        #write into the threshold bounds registers
        bus.write_byte_data(lights[0],0xA2,0x00)
        bus.write_byte_data(lights[0],0xA3,0x00)
        bus.write_byte_data(lights[0],0xA4,0xE8)
        bus.write_byte_data(lights[0],0xA5,0x03)

    else:
        light_interleave = light_INTER;
        
    do_every_light(publishlight);
    do_every_temp(publishTemp);

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

