from homemonitoring.client.client import ClientParameters
from homemonitoring.client.rest_client import ClientRestURL
from homemonitoring.setup.json_parse import JsonConfig
import logging
import colorlog
import sys, os

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Client_Setup():
    def __init__(self):
        self.jsonobj = JsonConfig()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        cli_f_path = abs_path + "/../client_config.json"
        self.json_cli_obj = self.jsonobj.dump_config(cli_f_path)

    def client_setup_verification(self):
        logger.info("Client_setup_is_good started")
        #Creating the class for client
        cli_obj = ClientParameters(self.json_cli_obj)
        rest_cli = ClientRestURL(self.json_cli_obj)

        #Checking Telo is online with IP Address
        ip_addr = cli_obj.is_telo_online()
        logger.info("IP Address of Client Telo %s" , ip_addr)

        #Checking the HMS Configuration
        controller_info = cli_obj.get_hms_config()
        logger.info("Controller Info %s", controller_info)

        cli_obj = rest_cli.load_client_debugconfig(cli_obj)

        if cli_obj.controller_info["ENABLED"] == "1":
            logger.info("Openremote is running successfully")
        else:
            logger.error("Openremote is Not Running")
