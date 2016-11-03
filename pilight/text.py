from pilight import LightBase

class Text(LightBase):
    """ Console sample
    """
    width = 0
    height = 0

    def __init__(self):
        print("Initialised")
        LightBase.__init__()

    def rgb(self, red, green, blue):
        """ Set the hat to this colour
        """
        print("Set RGB: %d, %d, %d" % (int(red), int(green), int(blue)))

    def led(self, red, green, blue, led=0, row=0):
        print("Set LED[%d] to RGB: %d, %d, %d" % (int(led), int(red), int(green), int(blue)))
        return True

    def state(self):
        return "Working"
