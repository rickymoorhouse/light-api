#!/usr/bin/python
import unicornhat
import time
from sunrise import sun
import datetime

unicornhat.set_layout(unicornhat.PHAT)
(width,height) = unicornhat.get_shape()

while 1 == 1:
  s=sun(lat=50.82,long=1.09)
  now = datetime.datetime.now()
  print(s.sunrise(),s.solarnoon(),s.sunset())
  time_to_sunset = datetime.datetime.combine(datetime.date.today(), s.sunset()) - now
  print time_to_sunset
  ttsmin = int(time_to_sunset.total_seconds()/60) 
  print ttsmin
  if ttsmin < 60:
      bright = (1440 - ttsmin) / 6 -150 
      print bright
      for y in range(height):
        for x in range(width):
          unicornhat.set_pixel(x,y, 20+bright, bright, bright)
          unicornhat.show()
          time.sleep(0.05)
  time.sleep(10)
