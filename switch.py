#!/usr/bin/python -u
# Python 2.7.9


#
# Assume that adjustments to a new switch position are expensive. So, work
# aggressively to not interpret transients as desired new settings.  The
# variables that control this are:
#   tick_rate:  How often the switch is polled to detect
#       if the switch has been moved.
#   ticks_needed_for_change:  The number of ticks that the switch must
#       remain stationary before the new position is interpreted
#       as the desired setting.
#
tick_rate = 0.1				# seconds
ticks_needed_for_change = 15		# 1 second in position

#
# Call with the new position and previous.  Previous is provides because it
# may be necessary to tear down the previous state.
#
def setting_demo(pos, prev):
	if prev is not None:		# normal case
		print "setting=%d was=%d" % (pos, prev)
	else:				# first time initialization
		print "setting=%d" % pos

#
# Call with the instantanious switch position and where it just moved from
# and the current stable setting.
#
def transition_demo(pos, previous, current):
	if current is not None:		# normal case
		print "provisional=%d previous=%d setting=%d" \
				% (pos, previous, current)
	else:
		print "provisional=%d" % pos


new_setting = setting_demo
new_transition = transition_demo
#
# Returns 0 if the input hardware value is invalid, otherwise
# a value 1..n is returned.
#
def hw_2_index(hw):
	bit = 0x8000				# start at high bit
	index = 1

	while (hw & bit) == 0:
		bit >>= 1
		index += 1

	if bit == 0:				# check if switch is between positions
		return 0					# is in between
	if hw & ~bit:				# check for multiple positions
		return 0					# is in multiple positions...
	return index				# valid


# I2C hardware register format is:
#	+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#	|B7|B6|B5|B4|B3|B2|B1|B0|A7|A6|A5|A4|A3|A2|A1|A0|
#	+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#	 p1 p2 p3 p4 p5 p6 x7 x8 c0 c1 x9 xa xb xc xd xe
#
#	B7..0, A7..0 are the Microchip MCP23017 port bits.
#	p1..pN are switch position bits.
#	x1..xM are switch position bits which are unused in this configuration.
#	c0, c1 are common terminals of the switch.
#
# See: Microchips MCP23017/MCP23S17 datasheet, 20001952C.pdf
#

from smbus import SMBus
from time import sleep

expander = 0x20					# I2C address

def initialize():
	global	smb

	# Get a handle to the I2C bus to which port expander is connected.
	smb = SMBus(1)
	bits_switch = 0xff3f		# only 0xfc00 are used for the 6 position switch
	bits_common = 0x00c0		# switch common terminals

	# Define input vs. output bits.  Commons are outputs.  Bits tied to the
	# switch positions are inputs.
	smb.write_word_data(expander, 0, bits_switch)

	# Invert the switch position bits for easier interpretation of
	# the selected position.
	smb.write_word_data(expander, 0x02, bits_switch)

	# Enable pull-ups on the switch bits.
	smb.write_word_data(expander, 0x0c, bits_switch)

	# Write a logic low to the common bits so that the selected position will be
	# pulled to ground while the others are pulled hi through the above pull-ups.
	smb.write_word_data(expander, 0x12, 0)

def shutdown():
	pass						# nothing to do for now

# Poll for switch position changes.
provisional = previous = None

#
#	return the number of switch positions the hardware supports
#
def	positions():
	return 6

def	service():
	global	provisional
	global	previous
	global	ticks_remaining_for_change

	switch_position = smb.read_word_data(expander, 0x12)

	if switch_position == 0:		# debounce
		return

	switch_position = hw_2_index(switch_position)

	if switch_position != provisional:
		new_transition(switch_position, provisional, previous)

	if switch_position != previous:
		if switch_position != provisional:
			ticks_remaining_for_change = ticks_needed_for_change
		else:
			ticks_remaining_for_change -= 1

	if ticks_remaining_for_change == 0:
		new_setting(switch_position, previous)
		provisional = previous = switch_position
		ticks_remaining_for_change = ticks_needed_for_change

	provisional = switch_position

def main():
	initialize()
	while True:
		service()
		sleep(tick_rate)

if __name__ == "__main__":
	main()

# vim:set ts=2:
