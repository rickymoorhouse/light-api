import json
import cherrypy
import os
import sys
import logging
import unicornhat
import time

class WebLight(object):
    env = None
    width = 0
    height = 0

    def __init__(self):
        self.env = json.loads(os.getenv('VCAP_APPLICATION','{}'))
        unicornhat.set_layout(unicornhat.AUTO)
        (self.width,self.height) = unicornhat.get_shape()

    @cherrypy.expose
    def rgb(self,r=0, g=0, b=0):
        for y in range(self.height):
            for x in range(self.width):
                unicornhat.set_pixel(x,y, int(r), int(g), int(b))
                unicornhat.show()
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return "OK"


current_dir = os.path.dirname(os.path.abspath(__file__))
conf = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.getenv('VCAP_APP_PORT',8004)),
    },
}

logging.basicConfig(stream = sys.stderr, level=logging.WARNING)
cherrypy.quickstart(WebLight(), '/', config=conf)

