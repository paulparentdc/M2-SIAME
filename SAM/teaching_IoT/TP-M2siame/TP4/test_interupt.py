from smbus2 import SMBus
import RPi.GPIO as GPIO
import time

bus = SMBus(1)

def readLight(address):
    #bus.write_byte_data(address, 0x08, 0x03)
    time.sleep(0.05)
    val = bus.read_word_data(address, 0xAC)
    print(val)
    bus.write_byte_data(address, 0xC0, 0x03)
    bus.write_byte_data(address,0x86,0x11)
    return val

def interruptionTSL(self):
    global bus
    print("interrupt")
    print(readLight(0x39))
    bus.write_byte_data(0x39,0xC0,0x03)
    bus.write_byte_data(0x39,0x86,0x11) 

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(16, GPIO.FALLING, callback = interruptionTSL)

bus.write_byte_data(0x39,0x80,0x03)
bus.write_byte_data(0x39,0x86,0x11)    
# Threshold Low
bus.write_byte_data(0x39,0xA2,0x00)
bus.write_byte_data(0x39,0xA3,0x00)
# Threshold High
bus.write_byte_data(0x39,0xA4,0xE8)
bus.write_byte_data(0x39,0xA5,0x03)

while(1):
    time.sleep(0.5)
    print(readLight(0x39))
    
    