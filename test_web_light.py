import web_light
import unittest
import mock

class weblightTest(unittest.TestCase):

    def test(self):
        self.assertEqual(3, 3)

    def testRGB(self):
        w = web_light.WebLight()
        response = w.rgb(255,240,230)
        self.assertEqual("red" in response, True)
        self.assertEqual(response['red'], 255)
        self.assertEqual(response['green'], 240)
        self.assertEqual(response['blue'], 230)

    def testOnOff(self):
        w = web_light.WebLight()
        # First set a colour
        response = w.rgb(30,140,250)
        self.assertEqual(response['red'], 30)
        self.assertEqual(response['green'], 140)
        self.assertEqual(response['blue'], 250)
        # Turn off
        response = w.off()
        self.assertEqual(response['red'], 0)
        self.assertEqual(response['green'], 0)
        self.assertEqual(response['blue'], 0)
        # Turn off
        response = w.onn()
        self.assertEqual(response['red'], 30)
        self.assertEqual(response['green'], 140)
        self.assertEqual(response['blue'], 250)


    def testHSL(self):
            w = web_light.WebLight()
            response = w.hsl(255,100,100)
            self.assertEqual(response['red'], 255)
            self.assertEqual(response['green'], 255)
            self.assertEqual(response['blue'], 255)
