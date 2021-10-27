#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Shutter module
#
# Thiebolt  aug.19  updated
# Francois  apr.16  initial release
#



# #############################################################################
#
# Import zone
#
import time
import json
import threading
import paho.mqtt.client as mqtt_client
import os
import sys
import connect
import logging    
import signal

_shutDownEvent = None



# #############################################################################
#
# Functions
#

def signal_handler(sig, frame):
    global __shutDown
    print('You pressed Ctrl+C!')
    _shutDownEvent.set()

# #############################################################################
#
# Classes
#
class Shutter(object):

    # class attributes
    SHUTTER_POS_CLOSED  = 0
    SHUTTER_POS_OPEN    = 1
    SHUTTER_POS_UNKNOWN = 2

    SHUTTER_ACTION_CLOSE    = 0
    SHUTTER_ACTION_OPEN     = 1
    SHUTTER_ACTION_STOP     = 2
    SHUTTER_ACTION_IDLE     = 3
    SHUTTER_ACTION_UNKNOWN  = 4



    MQTT_TYPE_TOPIC = "shutter"

    # Min. and max. values for shutter course time
    MIN_COURSE_TIME         = 5
    MAX_COURSE_TIME         = 60

    # attributes
    _status = SHUTTER_POS_UNKNOWN
    _courseTime  = 10;       # (seconds) max. time for shutter to get fully open / close

    _unitID     = None
    _clientMQTT = None
    _curCmd     = None
    _condition  = None      # threading condition
    _thread     = None      # thread to handle shutter's course

    def __init__(self, unitID, courseTime, mqtt_server, mqtt_topic_command, mqtt_topic_publish, shutDownEvent, *args, **kwargs):
        ''' Initialize object '''
        self._unitID = unitID
        self._courseTime = courseTime
        self._status = Shutter.SHUTTER_POS_OPEN
        self._curCmd = Shutter.SHUTTER_ACTION_STOP
        self._clientMQTT = connect.CommModule(mqtt_server, mqtt_topic_command, mqtt_topic_publish, unitID, self, shutDownEvent)
        self._clientMQTT.start()

    def thread_action(self, action):
        if(action == 'down'):
            print("Thread "+str(self._unitID)+" : state : down")
            self._curCmd = Shutter.SHUTTER_ACTION_STOP
            self._status = Shutter.SHUTTER_POS_CLOSED
        elif(action == 'up'):
            print("Thread "+str(self._unitID)+" : state : up")
            self._curCmd = Shutter.SHUTTER_ACTION_STOP
            self._status = Shutter.SHUTTER_POS_OPEN
        else:
            print("Thread creation error!")
        
        self.send_status()


    def handle_message(self, payload):
        order = payload['order']

        if(self._curCmd == Shutter.SHUTTER_ACTION_OPEN):
            if(order == 'down' or order == 'stop'):
                self._thread.cancel()
                self._curCmd = Shutter.SHUTTER_ACTION_STOP 

        elif(self._curCmd == Shutter.SHUTTER_ACTION_CLOSE):
            if(order == 'up' or order == 'stop'):
                self._thread.cancel()
                self._curCmd = Shutter.SHUTTER_ACTION_STOP
            
        elif(self._curCmd == Shutter.SHUTTER_ACTION_STOP):
            if(order == 'down'):
                self._curCmd = Shutter.SHUTTER_ACTION_CLOSE
                self._status = Shutter.SHUTTER_POS_UNKNOWN
                self._thread = threading.Timer(self._courseTime, self.thread_action, ['down'])
                self._thread.start()

            elif(order == 'up'):
                self._curCmd = Shutter.SHUTTER_ACTION_OPEN
                self._status = Shutter.SHUTTER_POS_UNKNOWN 
                self._thread = threading.Timer(self._courseTime, self.thread_action, ['up'])
                self._thread.start()
            else:
                print("Ordre ignore")


        self.send_status()
    


    def send_status(self):
        print("Envoie")
        log.info("Envoi du status ...")
        payload = {}
        
        if self._status == Shutter.SHUTTER_POS_CLOSED :
            payload["status"] = "CLOSED"
        elif self._status == Shutter.SHUTTER_POS_UNKNOWN :
            payload["status"] = "UNKNOWN"
        else :
            payload["status"] = "OPEN"
        self._clientMQTT.send_message(payload)
        


# #############################################################################
#
# MAIN
#

def main():
    global _shutDownEvent
    _shutDownEvent = threading.Event()
    signal.signal(signal.SIGINT, signal_handler)
    
    Shutter("front", 30, "192.168.0.214", "014/shutter/command", "014/shutter/", _shutDownEvent)
    Shutter("center", 30, "192.168.0.214", "014/shutter/command", "014/shutter/", _shutDownEvent)
    Shutter("back", 30, "192.168.0.214", "014/shutter/command", "014/shutter/", _shutDownEvent)
 



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

