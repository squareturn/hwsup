#!/usr/bin/python

import time
import RPi.GPIO as GPIO

LED_RED = 7			# 3 color led on POE HAT
LED_GREEN = 22			# 3 color led on POE HAT
LED_BLUE = 9			# 3 color led on POE HAT
LED_RJ45 = 25			# second green led on rj45 connector
LED_PI_RED = 35			# on some raspberry pi model PCBs

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_BLUE, GPIO.OUT)
GPIO.setup(LED_RJ45, GPIO.OUT)
GPIO.setup(LED_PI_RED, GPIO.OUT)

def	led(value):
	GPIO.output(LED_RED, value & 4 != 0)
	GPIO.output(LED_GREEN, value & 2 != 0)
	GPIO.output(LED_BLUE, value & 1 != 0)

for v in [0, 1, 2, 4, 3, 6, 5, 7]:
	led(v)
	GPIO.output(LED_RJ45, v & 1 != 0)
	GPIO.output(LED_PI_RED, v & 1 != 0)
	time.sleep(2.0)

GPIO.cleanup()
