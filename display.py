#!/usr/bin/python
 
#
# Driver for Newhaven Display, NHD-C12832A1Z-xxx-yyy family of devices.
# These are SPI devices with a display resolution of 128 x 32, with 1
# Bit per pixel (on or off).
#  
# SPI functionality is from:  http://tightdev.net/SpiDev_Doc.pdf
#
# ImageMagick can be used to create images.  See the sample commands
# in the scripts directory.
#
# This module is intended to be included in a larger application, but if
# run interactively, provides 2 functions:
#
# Called with no arguments, converts the Microsoft BMP file on stdin to
# the optimized format needed for efficient updating of the display.  Output
# is to stdout.
#
# Called with one argument, that argument is a filename of an optimized
# image to display.  (see above.)
#
import array
import sys
import spidev
import RPi.GPIO as GPIO
import time
import struct

SPI_A0 = 27
SPI_RST = 17
SPI_CS = 8


def log(st):
  print >> sys.stderr, st

# assume the output array is initialized to all zeros
bmask = [128, 64, 32, 16, 8, 4, 2, 1]
cmask = [1, 2, 4, 8, 16, 32, 64, 128]
def bitset(out, indata, inbyte, inbit):
  if indata[inbyte] & bmask[inbit]:  # only set bits
    outbyte = ((inbyte & 0xf)<<3) + (inbyte & 0x180) + inbit
    outbit = (inbyte & 0x70)>>4
#    log(str(inbyte) + "[" + str(inbit) + "]\t->\t" + \
#        str(outbyte) + "[" + str(outbit) + "]")
    out[outbyte] |= cmask[outbit]

def translate_bmp(fhandle):
  filedata = [ _ for _ in fhandle ][0]

  # BMP3 Metadata:
  #  0: magic
  #  1: file size
  #  2: reserved1
  #  3: reserved2
  #  4: start offset of bitmap
  #  5: size of this header
  #  6: image width
  #  7: image height
  #  8: number of color planes
  #  9: number of bits per pixel
  magic, size, res1, res2, offset, hdrsz, width, height, colors, pixelbits = \
      struct.unpack('<HiHHiiiihh', filedata[0:30])
  log("file metadata: " + str([magic, size, offset, hdrsz, width, height, colors, pixelbits]))
  if magic != 0x4d42:
    log("bad magic")
    sys.exit(1)
  if width != 128:
    log("expected image width: 128.  Got: " + width)
    sys.exit(1)
  if height != 32:
    log("expected image height: 32.  Got: " + height)
    sys.exit(1)
  if pixelbits != 1:
    log("expected bits per pixel: 1.  Got: " + pixelbits)
    sys.exit(1)
  if size - offset != 512:
    log("expected bytes of data: 512.  Got: " + str(size - offset))
    sys.exit(1)
  data = filedata[offset:size]
  data = [ ord(data[_]) for _ in range(len(data)) ]

  # Transform the BMP file so it's ordered the way the display
  # expects.  BMP is row at a time, MSB first.  Display is 8
  # rows at a time.  
  image = [ 0 for _ in range(512) ]
#  log("BMP row\t->")
  for i in range(512):
    for j in range(8):
      bitset(image, data, i, j)
  return image
 
def load_picture(path):
  f = open(path, 'r')
  pic = array.array('B')
  pic.fromfile(f, 128 * 32 / 8)
  return pic.tolist()

# Split an integer input into a two byte array to send via SPI
def lcd_command(cmd):
  GPIO.output(SPI_A0, 0)  # A0 low for commands
  spi.xfer([cmd])    # releases CS between bytes

def show_picture(pic):
  page = 0xb0
#  lcd_command(0xae)  # display off
  lcd_command(0x40)  # display start address + 0x40
  for i in range(4):
    lcd_command(page)
    lcd_command(0x10)  # column address upper 4 bits + 0x10
    lcd_command(0x00)  # column address lower 4 bits + 0x00
    j = i << 7
    GPIO.output(SPI_A0, 1)  # A0 high for data
    spi.xfer2(pic[j:j+128])
    page += 1
  lcd_command(0xaf)  # display on

def reset():
  # module reset
  GPIO.output(SPI_RST, 0)
  time.sleep(0.1)
  GPIO.output(SPI_RST, 1)

# LCD controller initialization
def initialize():
  global  spi

  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(SPI_A0, GPIO.OUT)
  GPIO.setup(SPI_RST, GPIO.OUT, initial=1)
  GPIO.setup(SPI_CS, GPIO.OUT, initial=1)

  spi = spidev.SpiDev()
  spi.open(0, 0)      # CS0
#  spi.max_speed_hz = 25000000
  spi.max_speed_hz = 20000000

  # LDC controller setup
  # ADC select -- normal    1010 000x
  lcd_command(0xa0)
  # LCD off      1010 111x
  lcd_command(0xae)
  # common output mode select  1100 xyyy
  lcd_command(0xc0)
  # LCD bias set: 1:1/9    1010 001x
  lcd_command(0xa3)
  # power control set    0010 1xxx
  lcd_command(0x2f)
  # V0 voltage regulator internal resistor ratio set  0010 0xxx
  lcd_command(0x20)      # USE TO SET BRIGHTNESS
  # Electronic volume mode set  1000 0001
  lcd_command(0x81)
  # ???
  lcd_command(0x2f)

def shutdown():
  spi.close()

def main():
  #
  # USAGE: Call with no args, converts the Microsoft Windows BMP3 file,
  # on stdin, to the format required by the display hardware.  (on stdout)
  # Called with a name of a hardware ready file to display.
  #
  argc = len(sys.argv)
  if argc == 1:         # convert bitmap on stdin to optimized format
    graphic = translate_bmp(sys.stdin)
    data = array.array('B', graphic)
    data.write(sys.stdout)
  elif argc == 2:       # display the optimized image in file
    graphic = load_picture(sys.argv[1])
    initialize()
    show_picture(graphic)
  else:                 # cycle through images. delay, image0, image1, image...
    delay = float(sys.argv[1])
    images = [ None for _ in range(argc-2) ]
    for i in range(2, argc):
      images[i-2] = load_picture(sys.argv[i])
    initialize()
    log("display " + str(len(images)) + " images.  ^C to exit.")
    while True:
      for i in range(0, argc-2):
        show_picture(images[i])
        time.sleep(delay)

if __name__ == "__main__":
  main()

# vim:set ts=2 expandtab:
