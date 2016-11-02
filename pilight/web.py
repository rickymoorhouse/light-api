#!/usr/bin/python
import json
import cherrypy
import os
import sys
import logging
import time
import struct
import colorsys
from stevedore import driver
from logging.handlers import SysLogHandler

class WebLight(object):
    env = None
    width = 0
    height = 0
    red = 0
    green = 0
    blue = 0
    h = 1
    s = 1
    l = 1
    on = False
    levels = [
        [0,0,0],
        [0,255,0],
        [255,255,0],
        [255,0,0]
    ]
    logger = None


    def __init__(self, device='unicornhat'):
        self.logger = logging.getLogger()
        self.env = json.loads(os.getenv('VCAP_APPLICATION','{}'))
        self.mgr = driver.DriverManager(
            namespace='pilight.device',
            name=device,
            invoke_on_load=True,
        )

    def _setrgb(self,r=0, g=0, b=0):
        self.mgr.driver.rgb(r, g, b)
        return {"red":r, "green":g, "blue":b}

    @cherrypy.expose
    def led(self,led=0, r=0, g=0, b=0, row=0):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        if self.mgr.driver.led(r, g, b, led, row):
            return "OK"
        else:
            cherrypy.response.status = 400
            return "NO"


    @cherrypy.expose
    def status(self):
        if self.on:
            return "1"
        else:
            return "0"

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def onn(self):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        self.on = True
        return self._setrgb(self.red, self.green, self.blue)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def off(self):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        self.on = False
        return self._setrgb(0, 0, 0)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def hue(self, value):
        self.h = value
        if self.on:
            return self.hsl(value, self.s, self.l)
        else:
            return "off"

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def sat(self, value):
        self.s = value
        if self.on:
            return self.hsl(self.h, value, self.l)
        else:
            return "off"

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def lum(self, value):
        self.l = value
        if self.on:
            return self.hsl(self.h, self.s, value)
        else:
            return "off"

    def _hsl(self):
        h, s, l = colorsys.rgb_to_hls(self.red / 255.0, self.green / 255.0, self.blue / 255.0)
        h = h * 360
        if h < 1:
            h = 1
        s = s * 100
        if s < 1:
            s = 1
        l = l * 100
        if l < 1:
            l = 1
        return (h, s, l)


    @cherrypy.tools.json_out()
    @cherrypy.expose
    def hsl(self,h=0, s=0, l=0):
        self.h = h
        self.s = s
        self.l = l
        r, g, b = colorsys.hls_to_rgb(float(h)/360, float(l)/100, float(s)/100)
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        if r+g+b > 0:
            self.logger.info("Greater than zero - logging rgb: %d, %d, %d", r, g, b)
            self.red = r * 255
            self.blue = b * 255
            self.green = g * 255
        return self._setrgb(r * 255, g * 255, b * 255)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def rgb(self,r=0, g=0, b=0):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        if r+g+b > 0:
            self.red = r
            self.blue = b
            self.green = g
            self.on = True
        else:
            self.on = False
        return self._setrgb(r, g, b)

    @cherrypy.expose
    def colour(self):
      return ''+struct.pack("BBB",*(self.red, self.green, self.blue)).encode('hex')

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def state(self):
      return "unimplemented" #unicornhat.get_pixels()

    @cherrypy.expose
    def brightness(self):
      vals = []
      for x in self.red, self.green, self.blue:
        vals.append(x/255.0)
      l = (min(vals) + max(vals))/2
      return str(l*100)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def hex(self,value="#000000"):
        hex_code = value.replace("#","")
        (r, g, b) = struct.unpack('BBB',hex_code.decode('hex'))
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        self.red = r
        self.blue = b
        self.green = g
        self.on = True
        return self._setrgb(r, g, b)
