#!/usr/bin/env python3
#coding: utf-8
#

import sys;

import threading

def do_every(interval,worker_func,iterations = 0):
    global timer
    if(iter != 1):
        timer = threading.Timer (
            interval,
            do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1] );
        timer.start()
        # launch worker function
        worker_func();


def display_temp():
    f = open("/sys/devices/platform/coretemp.0/hwmon/hwmon3/temp1_input")
    print("%s" %f.readline())

def main():
    do_every(3,display_temp,0)

#Execution or import

if __name__ == "__main__":
    main()
    sys.exit(0)
