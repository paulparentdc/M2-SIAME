#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# dataCOllector web. app.
#
# F.Thiebolt    Mar.20  initial release
#



# #############################################################################
#
# Import zone
#
import os
import sys
import time
import json
import datetime

# Logging
import logging
from logger import log, setLogLevel, getLogLevel

# Settings
import settings

# Flask
from flask import Flask



# #############################################################################
#
# Global variables
# (scope: this file)
#

# defined debug mode ?
if( os.getenv("DEBUG")=='1' or os.getenv("DEBUG") is True ):
    log.info("DEBUG mode activation ...")
    setLogLevel( logging.DEBUG )
    # print all environment variables
    print(os.environ)

# Flask app. declaration
app = Flask(__name__)



# #############################################################################
#
# Functions
#

#
# Example function to get routed to
@app.route('/')
def hello_world():
    log.info("a short INFO msg :)")
    log.debug("this is a DEBUG msg !")
    return "Hello World"



# #############################################################################
#
# MAIN
#

# Execution or import
if __name__ == "__main__":

    #
    print("\n###\n[neOCampus] idataCOllector web. app.\n###")

    # start
    app.run( host='0.0.0.0' )


# The END - Jim Morrison 1943 - 1971
#sys.exit(0)

