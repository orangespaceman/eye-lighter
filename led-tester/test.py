#!/usr/bin/python

import time
from dotstar import Adafruit_DotStar

numpixels = 24

strip = Adafruit_DotStar(numpixels)
strip.begin()
strip.setBrightness(50)

head = 0
tail = -10
color = 0xFF0000

while True:
    strip.setPixelColor(head, color)
    strip.setPixelColor(tail, 0)
    strip.show()
    time.sleep(1.0 / 50)

    head += 1

    if(head >= numpixels):
        head = 0
        color >>= 8

    if(color == 0):
        color = 0xFF0000

    tail += 1

    if(tail >= numpixels):
        tail = 0
