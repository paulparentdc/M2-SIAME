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
import connect.py



# #############################################################################
#
# Functions
#



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
    courseTime  = 30;       # (seconds) max. time for shutter to get fully open / close

    _clientMQTT = None
    _curCmd     = None
    _condition  = None      # threading condition
    _thread     = None      # thread to handle shutter's course

    def __init__(self, unitID, courseTime, mqtt_server, mqtt_topic_command, mqtt_topic_publish, *args, **kwargs):
        ''' Initialize object '''
        self._clientMQTT = connect.CommModule(mqtt_server, mqtt_topic_command, mqtt_topic_publish, unitID, self)
        self._clientMQTT.start()

    def handle_message(payload):
        order = payload['order']

        if(order == 'up'):
            print("Le volet monte")
        elif(order == 'down'):
            print("Le volet descend")
        elif(order == 'stop'):
            print("Le volet se stop")
        elif(order == 'status'):
            print("Le status du volet est %")
        
        else:



# #############################################################################
#
# MAIN
#

def main():

    #TODO: implement simple tests of your module
    _______________
    _______________
    _______________
    _______________
    _______________
    _______________




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

