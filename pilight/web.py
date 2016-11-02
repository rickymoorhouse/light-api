#!/usr/bin/python
""" API interface to pilight """
import logging
import struct
import colorsys
import cherrypy
from stevedore import driver

class WebLight(object):
    """ Main web api methods """
    red = 0
    green = 0
    blue = 0
    _hue = 1
    _sat = 1
    _lum = 1
    is_on = False
    logger = None


    def __init__(self, device='unicornhat'):
        self.logger = logging.getLogger()
        self.mgr = driver.DriverManager(
            namespace='pilight.device',
            name=device,
            invoke_on_load=True,
        )

    def _setrgb(self, red=None, green=None, blue=None):
        if red is None:
            red = self.red
        if green is None:
            green = self.green
        if blue is None:
            blue = self.blue
        self.mgr.driver.rgb(red, green, blue)
        return {"red":red, "green":green, "blue":blue}

    @cherrypy.expose
    def led(self, led=0, red=0, green=0, blue=0, row=0):
        """ Set specific LED to a colour """
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        if self.mgr.driver.led(red, green, blue, led, row):
            return "OK"
        else:
            cherrypy.response.status = 400
            return "NO"


    @cherrypy.expose
    def status(self):
        """ return power status 1 for on, 0 for off """
        if self.is_on:
            return "1"
        else:
            return "0"

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def power_on(self):
        """ turn light on """
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        self.is_on = True
        return self._setrgb(self.red, self.green, self.blue)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def power_off(self):
        """ Turn the light off """
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        self.is_on = False
        return self._setrgb(0, 0, 0)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def hue(self, value):
        """ Set the hue """
        self._hue = value
        if self.is_on:
            return self.hsl(value, self._sat, self._lum)
        else:
            return "off"

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def sat(self, value):
        """ Set the saturation """
        self._sat = value
        if self.is_on:
            return self.hsl(self._hue, value, self._lum)
        else:
            return "off"

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def lum(self, value):
        """ Set the luminance """
        self._lum = value
        if self.is_on:
            return self.hsl(self._hue, self._sat, value)
        else:
            return "off"

    def _hsl(self):
        hue, sat, lum = colorsys.rgb_to_hls(self.red / 255.0, self.green / 255.0, self.blue / 255.0)
        hue = hue * 360
        if hue < 1:
            hue = 1.0
        sat = sat * 100
        if sat < 1:
            sat = 1.0
        lum = lum * 100
        if lum < 1:
            lum = 1.0
        return (hue, sat, lum)


    @cherrypy.tools.json_out()
    @cherrypy.expose
    def hsl(self, hue=0, sat=0, lum=0):
        """ Set Hue, Saturation and Luminance """
        self._hue = hue
        self._sat = sat
        self._lum = lum
        red, green, blue = colorsys.hls_to_rgb(float(hue)/360, float(lum)/100, float(sat)/100)
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        if red + green + blue > 0:
            self.logger.info("Greater than zero - logging rgb: %d, %d, %d", red, green, blue)
            self.red = red * 255
            self.blue = blue * 255
            self.green = green * 255
        return self._setrgb()

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def rgb(self, red=0, green=0, blue=0):
        """ Set light to this RGB vakue """
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        if red+green+blue > 0:
            self.red = red
            self.blue = blue
            self.green = green
            self.is_on = True
        else:
            self.is_on = False
        return self._setrgb()

    @cherrypy.expose
    def colour(self):
        """ return current hex code """
        return ''+struct.pack("BBB", *(self.red, self.green, self.blue)).encode('hex')

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def state(self):
        """ Return LED state """
        return "unimplemented" #unicornhat.get_pixels()

    @cherrypy.expose
    def brightness(self):
        """ return calculated brightness 0-100 """
        vals = []
        for value in self.red, self.green, self.blue:
            vals.append(value/255.0)
        brightness = (min(vals) + max(vals))/2
        return str(brightness*100)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def hex(self, value="#000000"):
        """ Set light to this hex colour """
        hex_code = value.replace("#", "")
        (red, green, blue) = struct.unpack('BBB', hex_code.decode('hex'))
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        self.red = red
        self.blue = blue
        self.green = green
        self.is_on = True
        return self._setrgb()
