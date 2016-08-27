#!/usr/bin/env python

import unicornhat as uh
import time
uh.set_layout(uh.AUTO)
(width,height) = uh.get_shape()
for y in range(height):
  for x in range(width):
    bright = y*10
    uh.set_pixel(x,y, 70+bright, 20+bright,100+ bright)
    uh.show()
    time.sleep(0.05)

while 1 == 1:
  time.sleep(1)
