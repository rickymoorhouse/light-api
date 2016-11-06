import pilight.web
import unittest
import mock

class weblightTest(unittest.TestCase):

    def test(self):
        self.assertEqual(3, 3)

    def testRGB(self):
        w = pilight.web.WebLight('console')
        response = w.rgb(255,240,230)
        self.assertEqual("red" in response, True)
        self.assertEqual(response['red'], 255)
        self.assertEqual(response['green'], 240)
        self.assertEqual(response['blue'], 230)

    def testLed(self):
        w = pilight.web.WebLight('console')
        response = w.led(1,255,240,230)
        self.assertEqual("OK" in response, True)

    def testOnOff(self):
        w = pilight.web.WebLight('console')
        # First set a colour
        response = w.rgb(30,140,250)
        self.assertEqual(response['red'], 30)
        self.assertEqual(response['green'], 140)
        self.assertEqual(response['blue'], 250)
        self.assertEqual(w.status(), '1')
        # Turn off
        response = w.power_off()
        self.assertEqual(response['red'], 0)
        self.assertEqual(response['green'], 0)
        self.assertEqual(response['blue'], 0)
        self.assertEqual(w.status(), '0')
        # Turn off
        response = w.power_on()
        self.assertEqual(response['red'], 30)
        self.assertEqual(response['green'], 140)
        self.assertEqual(response['blue'], 250)


    def testHSL(self):
        w = pilight.web.WebLight('console')
        response = w.hsl(255,100,100)
        self.assertEqual(response['red'], 255)
        self.assertEqual(response['green'], 255)
        self.assertEqual(response['blue'], 255)

    def testHueSatLum(self):
        w = pilight.web.WebLight('console')
        w.power_on()
        response1 = w.hue(0)
        response2 = w.lum(100)
        response3 = w.sat(100)
        self.assertEqual(response1['red']>0, True)
        self.assertEqual(response1['green'] < response1['red'], True)
        self.assertEqual(response1['blue'] < response1['red'], True)

        self.assertEqual(response2['red'], 255)
        self.assertEqual(response2['green'], 255)
        self.assertEqual(response2['blue'], 255)

        self.assertEqual(response3['red'], 255)
        self.assertEqual(response3['green'], 255)
        self.assertEqual(response3['blue'], 255)
