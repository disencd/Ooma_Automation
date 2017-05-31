import logging
import sys
import unittest
import time, os
from homemonitoring.virtual_sensor.create_oss_hms_acc import HMS_Activation
from homemonitoring.virtual_sensor.pair_sensor import Sensor_Addition
class VStest(unittest.TestCase):
    def setUp(self):
        print("Setting up Virtual Test Automation")
        self.custom_timers = {}

    def abc_test_1_activate_hms(self):
        print "Activating the OSS HMS Account"
        oss_hms = HMS_Activation()
        cnt = 0
        while cnt < 100:
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
        print "Activating the OSS HMS Account"
        oss_hms = HMS_Activation()
        sensor_add = Sensor_Addition()
        cnt = 0
        _id = 0
        while cnt < 1:
            _start_timer = time.time()
            cust_pk,code = oss_hms.activate_hms_account()
            _latency = time.time() - _start_timer
            self.custom_timers['HMS_Activation_Time'] = _latency

            time.sleep(3)

            _start_timer = time.time()
            _id = oss_hms.get_status_hms_account()
            _latency = time.time() - _start_timer
            self.custom_timers['HMS_Information_Get'] = _latency

            print "cust_pk is ", cust_pk
            time.sleep(3)

            # _start_timer = time.time()
            # oss_hms.deactivate_hms_account()
            # _latency = time.time() - _start_timer
            # self.custom_timers['HMS_Deactivation_Time'] = _latency

            sensor_add.pair_door_sensor(str(cust_pk))

            sensor_add.sensor_status(cust_pk)
            cnt += 1
            time.sleep(10)