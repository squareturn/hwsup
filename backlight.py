#!/usr/bin/python -u
# Python 2.7.9

#
# Driver for the backlight on a Newhaven Display, NHD-C12832A1Z-xxx-yyy
# family of devices using the RasbperryPi hardware PWM.
#
# WiringPi-Python is used to access the hardware.  See:
#   https://github.com/WiringPi/WiringPi-Python
#
# This module is intended to be imported into a larger application, but
# can be run directly.  In which case, the argument is the duty cycle,
# 0 - 100%, to which the brightness is set.
#

import wiringpi
import sys
import time
from math import copysign
import threading

level_on = 1020         # level when the backlight is on
level_off = 0           # level when the backlight is off
delay_before_off = 5.0  # if the switch isn't moved for this many seconds
                        # then dim the backlight
rate_on = 0.005
rate_off = 0.010

step_on = 4
step_off = 4

_current = level_off    # current backlight level
_thread_on = None       # background thread for turning the backlight on
_thread_off = None      # background thread for turning off the backlight
                        # after a timeout of no switch activity
_thread_exit = False    # flag to signal thread to exit

# setup the PWM output for the backlight LED
max = 1024              # PWM max count
wiringpi.wiringPiSetup()
wiringpi.pinMode(1, 2)
wiringpi.pwmSetRange(max)

def duty(percent):          # testing...
  if percent > 100:
    percent = 100
  if percent < 0:
    percent = 0
  set_pwm(int(percent * max / 100))

def set_pwm(value):         # access to the hardware
  global _current

  _current = int(value)
#  print "pwm: " + str(_current) # + " (" + str(type(_current)) + ")"
  wiringpi.pwmWrite(1, _current)

def _ramp(goal, step, rate):
  global  _thread_exit

  step = copysign(step, goal - _current)
  print "curr: " + str(_current) + " goal: " + str(goal)
  print "step: " + str(step) + " rate: " + str(rate)
  current = _current
  while _current != goal:
    current += step
    if step > 0 and current > goal:
      current = goal
    if step < 0 and current < goal:
      current = goal
    set_pwm(current)
    if _thread_exit:
      _thread_exit = False
      return
    time.sleep(rate)

def _ramp_on():
  global  _thread_on
  global  _thread_off

  _ramp(level_on, step_on, rate_on)
  _thread_off = threading.Thread(target=_ramp_off)
  _thread_off.start()
  _thread_on = None

def _ramp_off():
  global  _thread_off
  global  _thread_exit

  cumm = 0
  while cumm < delay_before_off:
    if _thread_exit:
      _thread_exit = False
      return
    cumm += 0.05
    time.sleep(0.05)

  _ramp(level_off, step_off, rate_off)
  _thread_off = None

def turn_on():
  global _thread_on
  global _thread_off
  global _thread_exit

  if _thread_off is not None:
    print "kill backlight off thread"
    _thread_exit = True
    while _thread_exit:
      time.sleep(0.05)

  if _thread_on is None:
    print "backlight on"
    _thread_on = threading.Thread(target=_ramp_on)
    _thread_on.start()

def main():
  print "time_on:  " + str((level_on - level_off) / step_on * rate_on)
  print "time_off: " + str((level_on - level_off) / step_off * rate_off)
  if len(sys.argv) > 1:
    duty(float(sys.argv[1]))
  else:
    time.sleep(3)
    turn_on()
    time.sleep(delay_before_off + 5)

set_pwm(_current)
if __name__ == "__main__":
  main()

# vim:set ts=2 expandtab:
