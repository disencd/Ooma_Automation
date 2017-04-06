import logging
import sys
import unittest

from homemonitoring.setup.json_parse import JsonConfig

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
#logging.basicConfig(filename='hms.log',level=logging.DEBUG)

#Unittest framework for testing the Sensors in the Home Security Functionalities
class HMStest(unittest.TestCase):
    def setUp(self):
        logger.info("Setting up Sensor for HMS Test Automation")
        #Loading the Json configuration details
        jsonobj = JsonConfig()
        self.jconfig = jsonobj.dump_config("../client_config.json")