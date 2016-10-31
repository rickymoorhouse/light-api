# stevedore/example/simple.py
import lightbase


class pilight.PiGlow(lightbase.LightBase):
    """ PiGlow hat
    """

    def rgb(self, red, green, blue):
        """ Set the hat to this colour
        """
        print red
        return True
    def led(self,red, green, blue, led=0, row=0):
        if int(led) < self.height and int(row) < self.width:
            return True
        else:
            return False
