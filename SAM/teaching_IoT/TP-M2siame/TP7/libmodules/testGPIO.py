import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

GPIO.output(22, GPIO.HIGH)

time.sleep(1)

GPIO.output(22, GPIO.LOW)

GPIO.output(23, GPIO.HIGH)

time.sleep(1)

GPIO.output(23, GPIO.LOW)

GPIO.output(6, GPIO.HIGH)

time.sleep(1)

GPIO.output(6, GPIO.LOW)

GPIO.output(12, GPIO.HIGH)

time.sleep(1)

GPIO.output(12, GPIO.LOW)

GPIO.output(27, GPIO.HIGH)

time.sleep(1)

GPIO.output(27, GPIO.LOW)

GPIO.output(24, GPIO.HIGH)

time.sleep(1)

GPIO.output(24, GPIO.LOW)