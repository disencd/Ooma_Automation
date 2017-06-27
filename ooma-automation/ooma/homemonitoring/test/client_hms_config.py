from homemonitoring.sensor.flask_webclient.door_rest_cli import FlaskClientDoorSensor
from homemonitoring.sensor.flask_webclient.flood_rest_cli import FlaskClientWaterSensor
from homemonitoring.client.client_setup import Client_Setup
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.server.server_status import ServerStatus
from homemonitoring.server.pairing_mode import PairingMode
from homemonitoring.server.validate_logs import Validate_Logs
import sys, os
import unittest
import time
import logging
import colorlog

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/tmp/listener.log')
fh.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

#Unittest framework for testing the Client Home Security Functionalities

class HMStest(unittest.TestCase):
    def setUp(self):
        logger.info("-Setup for Testcase Started")
        self.jsonobj = JsonConfig()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        server_f_path = abs_path + "/../server_config.json"
        bb_f_path = abs_path + "/../bb_flask_api.json"
        cli_f_path = abs_path + "/../client_config.json"
        self.json_server_obj = self.jsonobj.dump_config(server_f_path)
        self.json_rest_obj = self.jsonobj.dump_config(bb_f_path)
        self.json_cli_obj = self.jsonobj.dump_config(cli_f_path)
        self.cust_pk = self.json_cli_obj["client_conf"]["cust_pk"]

    def test_1_hms_server_status(self):

        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info("test_1_hms_server_status - Started")
        serv_obj = ServerStatus(self.json_server_obj)
        serv_obj.check_all_server_status()
        logger.info ("test_1_hms_server_status - Completed")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_2_hms_config_in_client(self):
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info("test_hms_config_in_client - Started")
        cli_set = Client_Setup()
        cli_set.client_setup_verification()
        logger.info("test_hms_config_in_client - Completed")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def sampletest_3_trigger_pairing_mode(self):
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info ("test_trigger_pairing_mode - Started")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        pair = PairingMode(self.json_server_obj)

        logger.info("test_trigger_pairing_mode For Flood Sensor - Started")
        pair.enable()
        time.sleep(20)
        water_obj = FlaskClientWaterSensor(self.json_rest_obj)
        water_obj.water_sensor_status()
        water_obj.water_sensor_pairing_enabled()
        time.sleep(120)
        logger.info("test_trigger_pairing_mode For Flood Sensor - Completed")

        logger.info("test_trigger_pairing_mode For Door Sensor - Started")
        pair.enable()
        time.sleep(20)
        door_obj = FlaskClientDoorSensor(self.json_rest_obj)
        door_obj.door_sensor_status()
        door_obj.door_sensor_pairing_enabled()
        time.sleep(120)
        # print ("test_trigger_pairing_mode For Door Sensor - Completed")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_4_door_sensor_status(self):
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info ("test_door_sensor_status - Started")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        door_obj = FlaskClientDoorSensor(self.json_rest_obj)
        door_obj.door_sensor_status()
        val_log = Validate_Logs(self.cust_pk)
        __cnt  = 0
        __max = 1
        while( __cnt < __max):
            __cnt += 1
            time.sleep(7)
            door_obj.door_sensor_tampering_enabled()
            time.sleep(1)
            val_log.get_latest_logevent()

            time.sleep(7)
            door_obj.door_sensor_tampering_disabled()
            time.sleep(1)
            val_log.get_latest_logevent()

            time.sleep(7)
            door_obj.door_sensor_open()
            time.sleep(1)
            val_log.get_latest_logevent()

            time.sleep(7)
            door_obj.door_sensor_close()
            time.sleep(1)
            val_log.get_latest_logevent()

            time.sleep(7)
            door_obj.door_sensor_paging_enabled()
            time.sleep(1)
            val_log.get_latest_logevent()

            time.sleep(7)

        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info ("test_door_sensor_status - Completed")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_5_flood_sensor_status(self):
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info ("test_door_sensor_status - Started")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        val_log = Validate_Logs(self.cust_pk)
        flood_obj = FlaskClientWaterSensor(self.json_rest_obj)
        flood_obj.water_sensor_status()
        __cnt = 0
        __max = 1
        while( __cnt < __max):
            __cnt += 1
            time.sleep(7)
            flood_obj.water_sensor_tampering_enabled()
            time.sleep(1)
            val_log.get_latest_logevent()

            time.sleep(7)
            flood_obj.water_sensor_tampering_disabled()
            time.sleep(1)
            val_log.get_latest_logevent()

            time.sleep(7)
            flood_obj.water_sensor_detects_water()
            time.sleep(1)
            val_log.get_latest_logevent()

            time.sleep(7)
            flood_obj.water_sensor_detects_no_water()
            time.sleep(1)
            val_log.get_latest_logevent()

            time.sleep(7)
            flood_obj.water_sensor_paging_enabled()
            time.sleep(1)
            val_log.get_latest_logevent()

            time.sleep(7)

        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info("test_door_sensor_status - Completed")
        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

if __name__ == "__main__":
    unittest.main()
