#!/bin/bash

OPTS='-size 128x32 -background white -fill black -shave 1x1 -bordercolor black -border 1 -font courier -gravity center'

convert $OPTS label:"H       " -monochrome bmp3:- | ./display.py > sample1.graphic
convert $OPTS label:"He      " -monochrome bmp3:- | ./display.py > sample2.graphic
convert $OPTS label:"Hel     " -monochrome bmp3:- | ./display.py > sample3.graphic
convert $OPTS label:"Hell    " -monochrome bmp3:- | ./display.py > sample4.graphic
convert $OPTS label:"Hello   " -monochrome bmp3:- | ./display.py > sample5.graphic
convert $OPTS label:"Hello.  " -monochrome bmp3:- | ./display.py > sample6.graphic
convert $OPTS label:"Hello.. " -monochrome bmp3:- | ./display.py > sample7.graphic
convert $OPTS label:"Hello..." -monochrome bmp3:- | ./display.py > sample8.graphic
