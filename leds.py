#!/usr/bin/python

import	RPi.GPIO as GPIO
import	sys

LED_RED = 7			# 3 color led on POE HAT
LED_GREEN = 22			# 3 color led on POE HAT
LED_BLUE = 9			# 3 color led on POE HAT
LED_RJ45 = 25			# second green led on rj45 connector

def	initialize():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED_RED, GPIO.OUT)
	GPIO.setup(LED_GREEN, GPIO.OUT)
	GPIO.setup(LED_BLUE, GPIO.OUT)
	GPIO.setup(LED_RJ45, GPIO.OUT)

def	led(value):
	GPIO.output(LED_RJ45, value & 8 != 0)
	GPIO.output(LED_RED, value & 4 != 0)
	GPIO.output(LED_GREEN, value & 2 != 0)
	GPIO.output(LED_BLUE, value & 1 != 0)

def main():
	initialize()
	if len(sys.argv) == 1:
		led(0)
	else:
		led(int(sys.argv[1]))

if __name__ == "__main__":
	main()

