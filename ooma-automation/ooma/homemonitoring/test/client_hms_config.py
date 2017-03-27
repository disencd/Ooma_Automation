import logging
import unittest
from homemonitoring.client.client import ClientParameters
from homemonitoring.setup.config_app import JsonConfig
from homemonitoring.setup.config_app import Login

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.basicConfig(filename='hms.log',level=logging.DEBUG)
#Unittest framework for testing the Client Home Security Functionalities
class ClientHMStest(unittest.TestCase):
    def setUp(self):
        logging.info("Setting up Client HMS Test Automation")
        #Loading the Json configuration details
        jsonobj = JsonConfig()
        self.jconfig = jsonobj.dump_config("../client_config.json")
        print self.jconfig["login_cred"]["username"]

    def test_hms_config_in_client(self):
        logging.info("test_hms_config_in_client - Started")
        login_obj = Login(self.jconfig)
        ssh = login_obj.ssh_to_server(self.jconfig["cert"]["prv-server"])
        shell = ssh.invoke_shell()
        showmyx_dict = login_obj.get_showmyx_output(shell)
        print showmyx_dict
