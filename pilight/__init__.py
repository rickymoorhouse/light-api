import abc
import six
import pilight.web
import cherrypy
import os

@six.add_metaclass(abc.ABCMeta)
class LightBase(object):
    """Base class for example plugin used in the tutorial.
    """

    def __init__(self, max_width=60):
        self.max_width = max_width

    @abc.abstractmethod
    def rgb(self, red, green, blue):
        """Set the light colour

        :param red: Red value 0-255
        :param green: Green value 0-255
        :param blue: Blue value 0-255
        :returns: True or False
        """
    @abc.abstractmethod
    def led(self, red, green, blue, led, row):
        """ Sets an individual LED """


def startWebServer():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.getenv('PORT',8004)),
        },
    }
    device = os.getenv('PILIGHT_DEVICE','console')
    cherrypy.quickstart(pilight.web.WebLight(device), '/', config=conf)

if __name__ == "__main__":
    startWebServer()
