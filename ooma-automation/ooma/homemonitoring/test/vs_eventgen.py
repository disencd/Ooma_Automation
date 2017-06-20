import sys
import unittest
import time, os
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

    def config_test_sensor_generation(self):
        logger.info("test_sensor_generation Started")
        sens_obj = Sensor_Action()
        # sens_obj.configure_door_Sensor("virtualaccount20170607170804362249", "VirtualDoorSensor3")

        _mong_obj = MongoDBQuery()
        results = _mong_obj.mongo_return_elements("SensorInterface_collection")


        for val in results:

            logger.info("Configuring the Sensor %s of PK %s"%\
                            (val["sensorname"], val["cust_pk"]))
            sens_obj.configure_door_Sensor(val["cust_pk"], \
                                            val["sensorname"])
            time.sleep(2)

        #sens_obj.post_sensor_events(cust_pk)

    def test_sensor_generation(self):
        logger.info("test_sensor_generation Started")
        sens_obj = Sensor_Action()
        # sens_obj.configure_door_Sensor("virtualaccount20170607170804362249", "VirtualDoorSensor3")

        _mong_obj = MongoDBQuery()
        results = _mong_obj.mongo_return_elements("SensorInterface_collection")
        logger.info("Mongo Returned %s", results)
        cnt = 0
        for val in results:

            if val["TamperDetector"]["id"] and cnt == 0:
                cnt+= 1
                config_dict = {
                    "no_events": 1,
                    "time_interval": 5,
                    "event": "TamperDetector"
                }

                logger.info("Tampering %s Sensor of PK %s" % \
                            (val["sensorname"], val["cust_pk"]))

                config_dict.update(val)
                sens_obj.trigger_sensor_events(config_dict)

                time.sleep(2)


if __name__ == "__main__":
    unittest.main()
