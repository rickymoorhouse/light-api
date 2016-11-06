import os
import abc
import six
import pilight.web
import cherrypy

@six.add_metaclass(abc.ABCMeta)
class LightBase(object):
    """Base class for example plugin used in the tutorial.
    """
    @abc.abstractmethod
    def __init__(self):
        """ Abstract init method """

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

    @abc.abstractmethod
    def state(self):
        """ Returns current state """

def configure():
    """ Prepare the configuration """
    device = os.getenv('PILIGHT_DEVICE', 'console')
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.getenv('PORT', 8004)),
        },
        'device':device
    }
    return conf
def start_server():
    """ Load the environment and start the webserver """
    conf = configure()
    cherrypy.quickstart(pilight.web.WebLight(), '/', config=conf)

if __name__ == "__main__":
    start_server()
