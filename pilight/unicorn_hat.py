from pilight import LightBase
import unicornhat

class Unicorn(LightBase):
    """ Unicorn hat
    """
    width = 0
    height = 0

    def __init__(self):
        unicornhat.set_layout(unicornhat.AUTO)
        (self.width, self.height) = unicornhat.get_shape()


    def rgb(self, red, green, blue):
        """ Set the hat to this colour
        """
        for y in range(self.height):
            for x in range(1, self.width):
                unicornhat.set_pixel(x,y, int(red), int(green), int(blue))
            unicornhat.show()
        return True

    def led(self, red, green, blue, led=0, row=0):
        if int(led) < self.height and int(row) < self.width:
            unicornhat.set_pixel(int(row), int(led), int(red), int(green), int(blue))
            unicornhat.show()
            return True
        else:
            return False
    def state(self):
        return unicornhat.get_pixels()
