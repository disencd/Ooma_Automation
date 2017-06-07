import logging
import colorlog
import sys
import unittest
import time
from homemonitoring.sensor.flask_webclient.door_rest_cli import FlaskClientDoorSensor
from homemonitoring.sensor.flask_webclient.flood_rest_cli import FlaskClientWaterSensor
from homemonitoring.client.client import ClientParameters
from homemonitoring.client.rest_client import ClientRestURL
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.server.server_status import ServerStatus
from homemonitoring.server.pairing_mode import PairingMode

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
#logging.basicConfig(filename='hms.log',level=logging.DEBUG)
#Unittest framework for testing the Client Home Security Functionalities

class HMStest(unittest.TestCase):
    def setUp(self):
        print("Setting up Client HMS Test Automation")
        self.jsonobj = JsonConfig()
        self.json_server_obj = self.jsonobj.dump_config("../server_config.json")
        self.json_cli_obj = self.jsonobj.dump_config("../client_config.json")
        self.json_rest_obj = self.jsonobj.dump_config("../bb_flask_api.json")

    def test_1_hms_server_status(self):

        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("test_1_hms_server_status - Started")
        self.serv_obj = ServerStatus(self.json_server_obj)

        __hms_status = self.serv_obj.ping_hms()
        print('HMS Status is ', __hms_status)

        __beehive_status = self.serv_obj.ping_beehive()
        print('Beehive Server Status is ', __beehive_status)

        __nimbits_status = self.serv_obj.ping_nimbits()
        print("Nimbits Server Status is ", __nimbits_status)

        print ("test_1_hms_server_status - Completed")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_2_hms_config_in_client(self):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("test_hms_config_in_client - Started")

        #Creating the class for client
        cli_obj = ClientParameters(self.json_cli_obj)
        rest_cli = ClientRestURL(self.json_cli_obj)

        #Checking Telo is online with IP Address
        ip_addr = cli_obj.is_telo_online()
        print("IP Address of Client Telo " , ip_addr)

        #Checking the HMS Configuration
        controller_info = cli_obj.get_hms_config()
        print("Controller Info ", controller_info)

        cli_obj = rest_cli.load_client_debugconfig(cli_obj)

        if cli_obj.controller_info["ENABLED"] == "1":
            print("HMS is running successfully")

        print ("test_hms_config_in_client - Completed")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_3_trigger_pairing_mode(self):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print ("test_trigger_pairing_mode - Started")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        pair = PairingMode(self.json_server_obj)

        # print ("test_trigger_pairing_mode For Flood Sensor - Started")
        # pair.enable()
        # time.sleep(20)
        # water_obj = FlaskClientWaterSensor(self.json_rest_obj)
        # water_obj.water_sensor_status()
        # water_obj.water_sensor_pairing_enabled()
        # time.sleep(120)
        # print ("test_trigger_pairing_mode For Flood Sensor - Completed")
        #
        # print ("test_trigger_pairing_mode For Door Sensor - Started")
        # pair.enable()
        # time.sleep(20)
        # door_obj = FlaskClientDoorSensor(self.json_rest_obj)
        # door_obj.door_sensor_status()
        # door_obj.door_sensor_pairing_enabled()
        # time.sleep(120)
        # print ("test_trigger_pairing_mode For Door Sensor - Completed")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_4_door_sensor_status(self):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print ("test_door_sensor_status - Started")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        door_obj = FlaskClientDoorSensor(self.json_rest_obj)
        door_obj.door_sensor_status()
        __cnt  = 0
        __max = 1000
        while( __cnt < __max):
            __cnt += 1
            time.sleep(7)
            door_obj.door_sensor_tampering_enabled()
            time.sleep(7)
            door_obj.door_sensor_tampering_disabled()
            time.sleep(7)
            door_obj.door_sensor_open()
            time.sleep(7)
            door_obj.door_sensor_close()
            time.sleep(7)
            door_obj.door_sensor_paging_enabled()
            time.sleep(7)

        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print ("test_door_sensor_status - Completed")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_5_flood_sensor_status(self):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print ("test_door_sensor_status - Started")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        flood_obj = FlaskClientWaterSensor(self.json_rest_obj)
        flood_obj.water_sensor_status()
        __cnt = 0
        __max = 1000
        while( __cnt < __max):
            __cnt += 1
            time.sleep(7)
            flood_obj.water_sensor_tampering_enabled()
            time.sleep(7)
            flood_obj.water_sensor_tampering_disabled()
            time.sleep(7)
            flood_obj.water_sensor_detects_water()
            time.sleep(7)
            flood_obj.water_sensor_detects_no_water()
            time.sleep(7)
            flood_obj.water_sensor_paging_enabled()
            time.sleep(7)

        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print ("test_door_sensor_status - Completed")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

if __name__ == "__main__":
    unittest.main()
