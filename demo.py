#!/usr/bin/python -u

import time
import switch
import display
import backlight

def changed(pos, prev):
	print "NOW: " + str(pos)
	display.show_picture(img_set[pos])

def moved(pos, prev, curr):
	backlight.turn_on()
	print "now: " + str(pos)
	if curr == pos:
		display.show_picture(img_set[pos])
	else:
		display.show_picture(img_move[pos])

display.initialize()
switch.initialize()

switch.new_transition = moved
switch.new_setting = changed

print "Switch positions: " + str(switch.positions())
img_set = [ [] for _ in range(switch.positions()+1) ]
img_move = [ [] for _ in range(switch.positions()+1) ]
for i in range(switch.positions()+1):
	img = "images/set" + str(i) + ".graphic"
	print "load images: " + img
	img_set[i] = display.load_picture(img)
	img = "images/move" + str(i) + ".graphic"
	img_move[i] = display.load_picture(img)

while True:
	switch.service()
	time.sleep(switch.tick_rate)

switch.shutdown()
display.shutdown()
