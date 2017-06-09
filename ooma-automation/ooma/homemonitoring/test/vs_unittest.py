import sys
import unittest
import time, os
from homemonitoring.virtual_sensor.create_oss_hms_acc import HMS_Activation
from homemonitoring.virtual_sensor.pair_sensor import Sensor_Addition
from homemonitoring.virtual_sensor.generate_sensor_events import Sensor_Action
import logging

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VStest(unittest.TestCase):
    def setUp(self):

        logger.info("Setting up Virtual Test Automation")
        self.custom_timers = {}

    def abc_test_1_activate_hms(self):
        logger.info("Activating the OSS HMS Account")
        oss_hms = HMS_Activation()
        cnt = 0
        while cnt < 1000:
            _start_timer = time.time()
            cust_pk,code = oss_hms.activate_hms_account()
            _latency = time.time() - _start_timer
            self.custom_timers['HMS_Activation_Time'] = _latency

            time.sleep(3)

            _start_timer = time.time()
            oss_hms.get_status_hms_account()
            _latency = time.time() - _start_timer
            self.custom_timers['HMS_Information_Get'] = _latency

            time.sleep(3)

            # _start_timer = time.time()
            # oss_hms.deactivate_hms_account()
            # _latency = time.time() - _start_timer
            # self.custom_timers['HMS_Deactivation_Time'] = _latency
            cnt += 1

    def test_2_activate_addsensor_hms(self):
        logger.info("Activating the OSS HMS Account")
        oss_hms = HMS_Activation()
        sensor_add = Sensor_Addition()
        cnt = 0
        _id = 0
        while cnt < 1:
            _start_timer = time.time()
            cust_pk,code = oss_hms.activate_hms_account()
            _latency = time.time() - _start_timer
            self.custom_timers['HMS_Activation_Time'] = _latency

            time.sleep(1)

            _start_timer = time.time()
            _id = oss_hms.get_status_hms_account()
            _latency = time.time() - _start_timer
            self.custom_timers['HMS_Information_Get'] = _latency

            logger.info("cust_pk is %s", cust_pk)
            time.sleep(1)

            # _start_timer = time.time()
            # oss_hms.deactivate_hms_account()
            # _latency = time.time() - _start_timer
            # self.custom_timers['HMS_Deactivation_Time'] = _latency

            sensor_add.pair_door_sensor(str(cust_pk))

            # time.sleep(10)
            #
            # sensor_add.pair_motion_sensor(str(cust_pk))
            #
            # time.sleep(10)

            sensor_add.sensor_status(cust_pk)

            sens_obj = Sensor_Action()
            sens_obj.configure_door_Sensor(cust_pk)
            sens_obj.post_sensor_events(cust_pk)
            cnt += 1
            time.sleep(1)


if __name__ == "__main__":
    unittest.main()
