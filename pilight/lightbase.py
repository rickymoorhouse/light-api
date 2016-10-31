import abc
import six


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
