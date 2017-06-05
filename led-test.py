#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import leds

colors = [ 'off', 'blue', 'green', 'blue-green', 'red', 'red-blue', 'red-green', 'white' ]

leds.initialize()
GPIO.output(leds.LED_RJ45, 1)
GPIO.output(leds.LED_PI_RED, 1)
for v in [4, 2, 1, 3, 6, 5, 7, 0]:
	leds.led(v)
	print colors[v]
	time.sleep(2.5)

# GPIO.cleanup()
GPIO.output(leds.LED_RJ45, 0)
GPIO.output(leds.LED_PI_RED, 0)
