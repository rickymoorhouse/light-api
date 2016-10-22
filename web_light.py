#!/usr/bin/python
import json
import cherrypy
import os
import sys
import logging
import unicornhat
import time
import struct
import colorsys
from logging.handlers import SysLogHandler


class WebLight(object):
    env = None
    width = 0
    height = 0
    r = 0
    g = 0
    b = 0
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

    def __init__(self):
        self.logger = logging.getLogger()
        self.env = json.loads(os.getenv('VCAP_APPLICATION','{}'))
        unicornhat.set_layout(unicornhat.AUTO)
        (self.width,self.height) = unicornhat.get_shape()
   
    def _setrgb(self,r=0, g=0, b=0):
        for y in range(self.height):
            for x in range(1,self.width):
                unicornhat.set_pixel(x,y, int(r), int(g), int(b))
            unicornhat.show()
        return {"red":r, "green":g, "blue":b}

    @cherrypy.expose
    def led(self,led=0, r=0, g=0, b=0, row=0):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        if int(led) < self.height:
            unicornhat.set_pixel(row, int(led), int(r), int(g), int(b))
            unicornhat.show()
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
        return self._setrgb(self.r, self.g, self.b)

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
        h, s, l = colorsys.rgb_to_hls(self.r / 255.0, self.g / 255.0, self.b / 255.0)
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


    @cherrypy.expose
    def hsl(self,h=0, s=0, l=0):
        self.h = h
        self.s = s
        self.l = l
        r, g, b = colorsys.hls_to_rgb(float(h)/360, float(l)/100, float(s)/100)
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        if r+g+b > 0:
            self.r = r
            self.b = b
            self.g = g
        return self._setrgb(r * 255, g * 255, b * 255)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def rgb(self,r=0, g=0, b=0):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        if r+g+b > 0:
            self.r = r
            self.b = b
            self.g = g
            self.on = True
        else:
            self.on = False
        return self._setrgb(r, g, b)

    @cherrypy.expose
    def colour(self):
      return ''+struct.pack("BBB",*(self.r, self.g, self.b)).encode('hex')

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def state(self):
      return unicornhat.get_pixels()
      
    @cherrypy.expose
    def brightness(self):
      vals = [x/255.0 for x in self.r, self.g, self.b]
      l = (min(vals) + max(vals))/2
      return str(l*100)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def hex(self,value="#000000"):
        hex_code = value.replace("#","")
        (r, g, b) = struct.unpack('BBB',hex_code.decode('hex'))
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        self.r = r
        self.b = b
        self.g = g
        self.on = True
        return self._setrgb(r, g, b)

    @cherrypy.expose
    def rgba(self,r=0, g=0, b=0, a=0):
        out = str(a) + " "
        i = 0
        for y in range(self.height):
            for x in range(self.width):
                i += 1
                if i == int(a):
                    unicornhat.set_pixel(x,y, int(r), int(g), int(b))
                    unicornhat.show()
                    i = 0
                    out += '1'
                else:
                    out += '0'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return "OK" + out

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.getenv('VCAP_APP_PORT',8004)),
        },
    }

    cherrypy.quickstart(WebLight(), '/', config=conf)

