#!/bin/bash -x

convert -size 128x32 -background white -fill black -font Bookman-LightItalic -gravity center label:"-error-" -monochrome bmp3:- | ./display.py > move0.graphic
convert -size 128x32 -background white -fill black -font Times-Roman -gravity center label:"breakfast" -monochrome bmp3:- | ./display.py > move1.graphic
convert -size 128x32 -background white -fill black -font Bookman-LightItalic -gravity center label:"Coffee?" -monochrome bmp3:- | ./display.py > move2.graphic
convert -size 128x32 -background white -fill black -font Century-Schoolbook-L-Roman -gravity center label:"Lunch?" -monochrome bmp3:- | ./display.py > move3.graphic
convert -size 128x32 -background white -fill black -font URW-Palladio-L-Roman -gravity center label:"espresso" -monochrome bmp3:- | ./display.py > move4.graphic
convert -size 128x32 -background white -fill black -font Nimbus-Sans-L -gravity center label:"Beer!" -monochrome bmp3:- | ./display.py > move5.graphic
convert -size 128x32 -background white -fill black -font Nimbus-Sans-L-Regular-Condensed-Italic -gravity center label:"dinner" -monochrome bmp3:- | ./display.py > move6.graphic
convert -size 128x32 -background white -fill black -font DejaVu-Sans -gravity center label:"television" -monochrome bmp3:- | ./display.py > move7.graphic
convert -size 128x32 -background white -fill black -font DejaVu-Serif -gravity center label:"Sleep..." -monochrome bmp3:- | ./display.py > move8.graphic

convert -size 128x32 -background white -fill black -shave 1x1 -bordercolor black -border 1 -font Bookman-LightItalic -gravity center label:"-error-" -monochrome bmp3:- | ./display.py > set0.graphic
convert -size 128x32 -background white -fill black -shave 1x1 -bordercolor black -border 1 -font Times-Roman -gravity center label:"breakfast" -monochrome bmp3:- | ./display.py > set1.graphic
convert -size 128x32 -background white -fill black -shave 1x1 -bordercolor black -border 1 -font Bookman-LightItalic -gravity center label:"Coffee?" -monochrome bmp3:- | ./display.py > set2.graphic
convert -size 128x32 -background white -fill black -shave 1x1 -bordercolor black -border 1 -font Century-Schoolbook-L-Roman -gravity center label:"Lunch?" -monochrome bmp3:- | ./display.py > set3.graphic
convert -size 128x32 -background white -fill black -shave 1x1 -bordercolor black -border 1 -font URW-Palladio-L-Roman -gravity center label:"espresso" -monochrome bmp3:- | ./display.py > set4.graphic
convert -size 128x32 -background white -fill black -shave 1x1 -bordercolor black -border 1 -font Nimbus-Sans-L -gravity center label:"Beer!" -monochrome bmp3:- | ./display.py > set5.graphic
convert -size 128x32 -background white -fill black -shave 1x1 -bordercolor black -border 1 -font Nimbus-Sans-L-Regular-Condensed-Italic -gravity center label:"dinner" -monochrome bmp3:- | ./display.py > set6.graphic
convert -size 128x32 -background white -fill black -shave 1x1 -bordercolor black -border 1 -font DejaVu-Sans -gravity center label:"television" -monochrome bmp3:- | ./display.py > set7.graphic
convert -size 128x32 -background white -fill black -shave 1x1 -bordercolor black -border 1 -font DejaVu-Serif -gravity center label:"Sleep..." -monochrome bmp3:- | ./display.py > set8.graphic

