import logging
import colorlog
import sys
import unittest
import time
from homemonitoring.sensor.flask_webclient.door_rest_cli import FlaskClientDoorSensor
from homemonitoring.sensor.flask_webclient.flood_rest_cli import FlaskClientWaterSensor
from homemonitoring.client.client_setup import Client_Setup
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.server.server_status import ServerStatus
from homemonitoring.server.pairing_mode import PairingMode
import logging
import colorlog

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

#Unittest framework for testing the Client Home Security Functionalities

class HMStest(unittest.TestCase):
    def setUp(self):
        logger.info("-Setup for Testcase Started")
        self.jsonobj = JsonConfig()
        self.cli_set = Client_Setup()

        self.json_server_obj = self.jsonobj.dump_config("../server_config.json")
        self.json_rest_obj = self.jsonobj.dump_config("../bb_flask_api.json")
        self.serv_obj = ServerStatus(self.json_server_obj)

    def test_1_hms_server_status(self):

        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info("test_1_hms_server_status - Started")

        self.serv_obj.check_all_server_status()
        logger.info ("test_1_hms_server_status - Completed")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_2_hms_config_in_client(self):
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info("test_hms_config_in_client - Started")
        cli_set.client_setup_verification()
        logger.info("test_hms_config_in_client - Completed")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_3_trigger_pairing_mode(self):
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info ("test_trigger_pairing_mode - Started")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
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
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_4_door_sensor_status(self):
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info ("test_door_sensor_status - Started")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

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

        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info ("test_door_sensor_status - Completed")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_5_flood_sensor_status(self):
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info ("test_door_sensor_status - Started")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

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

        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info("test_door_sensor_status - Completed")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

if __name__ == "__main__":
    unittest.main()
