from pilight import LightBase
import piglow

class PiGlow(LightBase):
    """ PiGlow
    """

    def rgb(self, red, green, blue):
        """ Set the hat to this colour
        """
        piglow.red(int(red))
        piglow.green(int(green))
        piglow.blue(int(blue))
        piglow.show()
        return True

    def led(self, red, green, blue, led=0, row=0):
        """ As piglow doesn't have RGB leds - use each leg for this -> 0, 1, 2 """

        if int(led) < 2:
            arm = led * 6
            piglow.set(arm + 5, red)
            piglow.set(arm + 2, green)
            piglow.set(arm + 1, blue)
            return True
        else:
            return False

    def state(self):
        return "unimplemented"
