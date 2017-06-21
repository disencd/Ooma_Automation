import sys
import unittest
import time, os
from homemonitoring.virtual_sensor.create_oss_hms_acc import HMS_Activation
from homemonitoring.virtual_sensor.pair_sensor import Sensor_Addition
from homemonitoring.virtual_sensor.generate_sensor_events import Sensor_Action
from homemonitoring.setup.mongodb_setup import MongoDBQuery
import logging

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VStest(unittest.TestCase):
    def setUp(self):

        logger.info("Setting up Virtual Test Automation")
        self.custom_timers = {}

    def test_add_sensor_to_activated_accounts(self):
        logger.info("Add Sensor to Activated Accounts")
        sensor_add = Sensor_Addition()

        _mong_obj = MongoDBQuery()
        results = _mong_obj.mongo_return_elements("acc_collection")

        # id = "virtualaccount20170614175103394885"
        # sensor_add.pair_door_sensor(id)

        for val in results:
            logger.info("pairing the PK with %s", val["cust_pk"])
            sensor_add.pair_motion_sensor(val["cust_pk"])

            sensor_add.pair_water_sensor(val["cust_pk"])
        #id = "virtualaccount20170607170607296891"

if __name__ == "__main__":
    unittest.main()
