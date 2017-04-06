import logging
import sys
import unittest

from homemonitoring.client.client import ClientParameters
from homemonitoring.client.rest_client import ClientRestURL
from homemonitoring.setup.json_parse import JsonConfig

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
#logging.basicConfig(filename='hms.log',level=logging.DEBUG)
#Unittest framework for testing the Client Home Security Functionalities
class HMStest(unittest.TestCase):
    def setUp(self):
        logger.info("Setting up Client HMS Test Automation")
        #Loading the Json configuration details
        jsonobj = JsonConfig()
        self.jconfig = jsonobj.dump_config("../client_config.json")


    def test_hms_config_in_client(self):
        logger.info("test_hms_config_in_client - Started")

        #Creating the class for client
        cli_obj = ClientParameters(self.jconfig, "cert")
        rest_cli = ClientRestURL(self.jconfig, "cert")

        #Checking Telo is online with IP Address
        ip_addr = cli_obj.is_telo_online()
        print ip_addr

        #Checking the HMS Configuration
        controller_info = cli_obj.get_hms_config()
        print controller_info



        cli_obj = rest_cli.load_client_debugconfig(cli_obj)

        if cli_obj.controller_info["or_status"] == "running":
            logger.info("HMS is running successfully")


    def test_hms_server_running(self):
        pass