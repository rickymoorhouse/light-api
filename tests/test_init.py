import os
import pilight
import unittest
import mock

class initTest(unittest.TestCase):

    @mock.patch.dict(os.environ, {}, clear=True)
    def testConfigDefault(self):
        config = pilight.configure()
        self.assertEqual("device" in config, True)
        self.assertEqual(config["device"], "console")
        self.assertEqual("global" in config, True)
        self.assertEqual("server.socket_host" in config["global"], True)
        self.assertEqual("server.socket_port" in config["global"], True)
        self.assertEqual(config["global"]["server.socket_port"], 8004)


    @mock.patch.dict(os.environ, {'PORT':'9000','PILIGHT_DEVICE':'testdevice'})
    def testConfigEnv(self):
        config = pilight.configure()
        self.assertEqual("device" in config, True)
        self.assertEqual(config["device"], "testdevice")
        self.assertEqual("global" in config, True)
        self.assertEqual("server.socket_host" in config["global"], True)
        self.assertEqual("server.socket_port" in config["global"], True)
        self.assertEqual(config["global"]["server.socket_port"], 9000)
