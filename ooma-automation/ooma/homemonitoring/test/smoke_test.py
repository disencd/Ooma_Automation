import os
from homemonitoring.server.sensor import Sensor, DeviceDiscovery, Nimbits, BCS
from homemonitoring.server.notification_recipients import RecipientsHandler
from homemonitoring.server.pairing_mode import PairingMode
from homemonitoring.server.controller import Controller

from time import sleep
import unittest
import xmlrunner
import json
from homemonitoring.server.configuration import Configuration
import platform
from homemonitoring.server.devices import Device
from homemonitoring.server.utils import get_json, links_list, put_logs, get_log_links
from datetime import datetime
from itertools import *


class PreConditionCheckMixin:

    def get_time(self):
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def print_log_links(self):

        try:
            link_list = links_list(int(os.environ["BUILD_NUMBER"]))
        except Exception, e:
            os.environ["BUILD_NUMBER"] = "0"
            link_list = links_list(int(os.environ["BUILD_NUMBER"]))

        print "-----------------------------------------------------------"
        print "--------Server logs can be found Links for logs------------"
        for item in link_list:
            print item

        print "-----------------------------------------------------------"

    def check_configuration(self):
        #self.print_log_links()

        print self.get_time()
        print "-----------------Checking configuration--------------------"
        conf_checker = Configuration()
        print "Check Tomcat status"
        assert conf_checker.tomcat_is_up(), "Tomcat server is down"

        print "Check HMS status"
        result = conf_checker.ping_hms()
        print "Result of ping: ", result
        assert result == 200, "Check of HMS is failed"

        print "Check BCS status"
        bcs = BCS()
        res = bcs.get_devices()
        print "Result of ping: ", result
        assert res == 200, "Check of BCS is failed"

        print "Check Device discovery"
        dd = DeviceDiscovery()
        res = dd.device_discovery()
        assert res == 200, "Check of device discovery is failed"

        nim = Nimbits()
        print "Check Nimbits status"
        assert nim.is_run() == 200, "Nimbits is not working properly"


# class SmokeTests(unittest.TestCase, PreConditionCheckMixin):
#
#     def setUp(self):
#         self.check_configuration()
#
#     def test_conroller(self):
#         self.test_name = "Smoke test"
#
#         dd = DeviceDiscovery()
#         self.sensor = Sensor()
#         nim = Nimbits()
#         print "----------------------------------"
#         print "Step 1: Set pairing mode"
#         resp = self.sensor.set_pairing_mode()
#
#         assert (resp == 200), "Cannot set pairing mode"
#         print "Pairing mode is SUCCESSFULLY set"
#         print "----------------------------------"
#         print "Step 2: Add sensor"
#         resp = self.sensor.add(type="MAGNET_CONTACT", mac_address="0000000091")
#
#         assert (resp == 200), "Cannot create new sensor"
#         print "Sensor is SUCCESSFULLY added"
#
#         sleep(5)
#         print "----------------------------------"
#         print "Step 3: Check if sensor is added"
#         dd.device_discovery()
#         assert (dd.find_device(self.sensor.get_mac_address()) != []), "Device was not added"
#
#         print "----------------------------------"
#         print "Step 4: Trying to send event"
#         event = "ALERT"
#         payload = "1"
#         resp = self.sensor.send_event(event, payload)
#         assert (resp == 200), "Cannot send event %s" % event
#         print "Event is sent"
#         '''
#         print "----------------------------------"
#         print "Step 5: Check sensor status"
#         alarm_state = nim.get_alarm_state(self.sensor.get_name())
#         assert (int(alarm_state) == int(payload)), "Sensor alarm state is %s, expected state %s" % (alarm_state, payload)
#         print "Sensor status SUCCESSFULLY checked"
#         '''
#         print "----------------------------------"
#         print "Step 5: Unpair sensor"
#         resp = self.sensor.unpair()
#         assert (resp == 200), "Cannot unpair sensor"
#         print "Sensor is unpaired"
#
#         sleep(5)
#         print "----------------------------------"
#         print "Step 6: Check if sensor is deleted"
#         dd.device_discovery()
#         assert (dd.find_device(self.sensor.get_mac_address()) == []), "Device is not deleted"
#         print "Sensor is deleted"
#         self.TEST_PASSED = True
#
#     def tearDown(self):
#         if not self.TEST_PASSED:
#             resp = self.sensor.unpair()
#             assert (resp == 200), "Cannot unpair sensor"
#             print "Sensor is unpaired"
'''
'''
class HmsNotificationRecipientsTests(unittest.TestCase, PreConditionCheckMixin):
    PHONE1, PHONE2 = "1234567892", "5555567893"
    EMAIL1, EMAIL2 = "mst.sm3ith@moogle.com", "ms2s.sh@sgmoogle.com"
    SMS1, SMS2 = "98765432123", "11223112321"

    def setUp(self):
        self.check_configuration()
        self.r_handler = RecipientsHandler()

    def test_notification_recipients_set_phone(self):
        print "----------------------------------"
        print "Step 1: Set phone number {0}".format(self.PHONE1)
        self.r_handler.phone = self.PHONE1

        print "Step 2: Get phone number"
        msg, code = self.r_handler.phone
        assert code == 200, "Error {0} {1}".format(msg, code)
        msg = json.loads(msg)[0]
        assert msg  == self.PHONE1,  "Error current: {0}, expected: {1}".format(msg, self.PHONE1)
        print "Phone number is SUCCESSFULLY set. current {0} expected {1}".format(msg, self.PHONE1)

        print "Step 3: Change phone number"
        del self.r_handler.phone

        self.r_handler.phone = self.PHONE2

        print "Step 4: Get new phone number"
        msg, code = self.r_handler.phone
        assert code == 200, "Error {0} {1}".format(msg, code)
        msg = json.loads(msg)[0]
        assert msg  == self.PHONE2,  "Error current: {0}, expected: {1}".format(msg, self.PHONE2)
        print "Phone number is SUCCESSFULLY changed. current {0} expected {1}".format(msg, self.PHONE2)
        print "Step 5: Remove data"
        del self.r_handler.phone

    def test_notification_recipients_set_email(self):
        print "----------------------------------"
        print "Step 1: Set email {0}".format(self.EMAIL1)
        self.r_handler.email = self.EMAIL1
        print "Step 2: Get email"
        msg, code = self.r_handler.email
        assert code == 200, "Error {0} {1}".format(msg, code)
        msg = json.loads(msg)[0]
        assert msg  == self.EMAIL1,  "Error current: {0}, expected: {1}".format(msg, self.EMAIL1)
        print "Email is SUCCESSFULLY set. current {0} expected {1}".format(msg, self.EMAIL1)

        print "Step 4: Change email"
        del self.r_handler.email

        self.r_handler.email = self.EMAIL2

        print "Step 4: Get new email"
        msg, code = self.r_handler.email
        assert code == 200, "Error {0} {1}".format(msg, code)
        msg = json.loads(msg)[0]
        assert msg  == self.EMAIL2,  "Error current: {0}, expected: {1}".format(msg, self.EMAIL2)
        print "Email is SUCCESSFULLY changed. current {0} expected {1}".format(msg, self.EMAIL2)
        print "Step 5: Remove data"
        del self.r_handler.email

    def test_notification_recipients_set_sms(self):
        print "----------------------------------"
        print "Step 1: Set sms number {0}".format(self.SMS1)
        self.r_handler.sms = self.SMS1
        print "Step 2: Get sms number"
        msg, code = self.r_handler.sms
        assert code == 200, "Error {0} {1}".format(msg, code)
        msg = json.loads(msg)[0]
        assert msg  == self.SMS1,  "Error current: {0}, expected: {1}".format(msg, self.SMS1)
        print "Sms is SUCCESSFULLY set. current {0} expected {1}".format(msg, self.SMS1)

        print "Step 4: Change sms number"
        del self.r_handler.sms

        self.r_handler.sms = self.SMS2

        print "Step 4: Get new sms number"
        msg, code = self.r_handler.sms
        assert code == 200, "Error {0} {1}".format(msg, code)
        msg = json.loads(msg)[0]
        assert msg  == self.SMS2,  "Error current: {0}, expected: {1}".format(msg, self.SMS2)
        print "Sms number is SUCCESSFULLY changed. current {0} expected {1}".format(msg, self.SMS2)
        print "Step 5: Remove data"
        del self.r_handler.sms

    def tearDown(self):
        del self.r_handler.phone
        del self.r_handler.sms
        del self.r_handler.email

#
# class HmsPairingModeTests(unittest.TestCase, PreConditionCheckMixin):
#
#     def setUp(self):
#         self.check_configuration()
#         self.pairing_mode = PairingMode()
#         self.controller = Controller()
#         self.beehive_user = "gsamarin2"
#         self.beehive_password = "gsamarin2"
#
#     def test_pairing_mode_enable_disable(self):
#         print "----------------------------------"
#         print "-     Verifying pairing mode     -"
#         print "----------------------------------"
#
#         pairing_sensor_value = 0;
#
#         print "Step 1: Enabling pairing mode"
#         print "Sending request to HMS to enable pairing mode..."
#         msg, code = self.pairing_mode.enable()
#         assert code == 200, "Cannot start pairing mode. Got response from HMS: {0} {1}".format(code, msg)
#         print "Success"
#
#         print "Waiting for Controller to enter pairing mode..."
#
#         for i in islice(count(), 3):
#             sleep(10)
#             print "Checking Controller status..."
#             pairing_sensor_value = int(Controller.get_sensor_status(self.beehive_user, self.beehive_password, self.controller.PAIRING_STATUS_SENSOR))
#             if pairing_sensor_value == 1: break
#             else: print "Not yet started. Retry at 10 seconds"
#
#         assert pairing_sensor_value == 1, "Failed to enable pairing mode on Controller"
#         print "Success! Controller has pairing mode enabled"
#
#         print "Step 2: Disabling pairing mode"
#         print "Sending request to HMS to disable pairing mode..."
#         msg, code = self.pairing_mode.enable()
#         assert code == 200, "Cannot stop pairing mode. Got response from HMS: {0} {1}".format(code, msg)
#         print "Success"
#
#         print "Waiting for Controller to stop pairing mode..."
#
#         for i in islice(count(), 3):
#             sleep(10)
#             print "Checking Controller status..."
#             pairing_sensor_value = int(controller.get_sensor_status(self.beehive_user, self.beehive_password, self.controller.PAIRING_STATUS_SENSOR))
#             if pairing_sensor_value == 0: break
#             else: print "Not yet stopped. Retry at 10 seconds"
#
#         assert pairing_sensor_value == 0, "Failed to stop pairing mode on Controller"
#         print "Success! Controller has pairing mode stopped"
#
#
#
# class HmsNotificationSettingsTests(unittest.TestCase, PreConditionCheckMixin):
#     defaults_notification_settings = {
#           "push": "off",
#           "telo": "on",
#           "phone": "off",
#           "email": "on",
#           "sms": "off",
#           "conditionRaised": 1,
#           "conditionCeased": 0
#     }
#
#     new_notification_settings = {
#               "push": "on",
#               "telo": "off",
#               "phone": "on",
#               "email": "off",
#               "sms": "on",
#               "conditionRaised": 10,
#               "conditionCeased": 1
#     }
#
#     def setUp(self):
#         #self.check_configuration()
#
#
#         self.sensor = Sensor()
#         self.device = Device()
#         '''
#         print "----------------------------------"
#
#         print "Step 1: Set pairing mode"
#         resp = self.sensor.set_pairing_mode()
#
#         assert (resp == 200), "Cannot set pairing mode"
#         print "Pairing mode is SUCCESSFULLY set"
#         print "----------------------------------"
#
#         print "Trying to get new devices"
#
#         json_data = self.device.get_new_devices()
#         before_addition = set([device["id"] for device in json_data["newDevices"]])
#
#         print "Step 2: Add sensor"
#         resp = self.sensor.add(type="MAGNET_CONTACT", mac_address="0000000091")
#         assert (resp == 200), "Cannot create new sensor"
#         print "Sensor is SUCCESSFULLY added"
#         print "----------------------------------"
#
#
#         sleep(15)
#         print "Trying to get new devices"
#         json_data2 = self.device.get_new_devices()
#         print "----------------------------------"
#         after_addition = set([device["id"] for device in json_data2["newDevices"]])
#
#         print "AFTER SET: ", after_addition
#         print
#         print "BEFORE SET: ", before_addition
#         difference_set = after_addition - before_addition
#         assert len(difference_set) == 1, "Expected count of new devises is 1, actual [%s]" % len(difference_set)
#
#
#
#         device_id = difference_set.pop()
#         print "new_device_id: ", device_id
#
#         data = self.device.register_device(device_id)
#         print "TEST TEST TEST data:", data
#         print "aspvncdoasnv[odasnv[odnasva[sdv[asv[asvasvsvdso[iasndov[inasdvno[asndvoiadnsov[indasvnoidnas"
#         #sleep(60)
#         #json_data3 = self.device.get_new_devices()
#         #after_registration = set([device["id"] for device in json_data3["newDevices"]])
#
#         #assert after_registration == before_addition, "Device was not removed from new devices list"
#         '''
#         mod = __import__("py_frame.notification_settings")
#
#         mod.notification_settings.DEVICE_ID = 249
#         self.ns_handler = mod.notification_settings.NotificationSettingsHandler()
#
#     def test_configure_and_update_away_mode_notification_settings(self):
#         print "----------------------------------"
#         print "Step 1: Get current away mode settings"
#         msg, code = self.ns_handler.away_mode
#         assert code == 200, "Error {0} {1}".format(msg, code)
#         msg = json.loads(msg)
#         assert msg == self.defaults_notification_settings, "Error {0} {1}".format(msg, code)
#
#         print "Step 2: Set new away mode settings %s" % self.new_notification_settings
#         self.ns_handler.away_mode = self.new_notification_settings
#
#         print "Step 3: Check new settings"
#         msg, code = self.ns_handler.away_mode
#         assert code == 200, "Error {0} {1}".format(msg, code)
#
#         msg = json.loads(msg)
#         assert msg == self.new_notification_settings, "Error {0} {1}".format(msg, code)
#
#         print "Step 4: Set default settings %s" % self.defaults_notification_settings
#         self.ns_handler.away_mode = self.defaults_notification_settings
#         msg, code = self.ns_handler.away_mode
#         assert code == 200, "Error {0} {1}".format(msg, code)
#         msg = json.loads(msg)
#         assert msg == self.defaults_notification_settings, "Error {0} {1}".format(msg, code)
#
#     def test_configure_and_update_home_mode_notification_settings(self):
#         print "----------------------------------"
#         print "Step 1: Get current home mode settings"
#         msg, code = self.ns_handler.home_mode
#         assert code == 200, "Error {0} {1}".format(msg, code)
#         msg = json.loads(msg)
#         assert msg == self.defaults_notification_settings, "Error {0} {1}".format(msg, code)
#
#         print "Step 2: Set new home mode settings %s" % self.new_notification_settings
#         self.ns_handler.home_mode = self.new_notification_settings
#
#         print "Step 3: Check new settings"
#         msg, code = self.ns_handler.home_mode
#         assert code == 200, "Error {0} {1}".format(msg, code)
#
#         msg = json.loads(msg)
#         assert msg == self.new_notification_settings, "Error {0} {1}".format(msg, code)
#
#         print "Step 4: Set default settings %s" % self.defaults_notification_settings
#         self.ns_handler.home_mode = self.defaults_notification_settings
#         msg, code = self.ns_handler.home_mode
#         assert code == 200, "Error {0} {1}".format(msg, code)
#         msg = json.loads(msg)
#         assert msg == self.defaults_notification_settings, "Error {0} {1}".format(msg, code)
#
#     def test_configure_and_update_night_mode_notification_settings(self):
#         print "----------------------------------"
#         print "Step 1: Get current night mode settings"
#         msg, code = self.ns_handler.night_mode
#         assert code == 200, "Error {0} {1}".format(msg, code)
#         msg = json.loads(msg)
#         assert msg == self.defaults_notification_settings, "Error {0} {1}".format(msg, code)
#
#         print "Step 2: Set new night mode settings %s" % self.new_notification_settings
#         self.ns_handler.night_mode = self.new_notification_settings
#
#         print "Step 3: Check new settings"
#         msg, code = self.ns_handler.night_mode
#         assert code == 200, "Error {0} {1}".format(msg, code)
#
#         msg = json.loads(msg)
#         assert msg == self.new_notification_settings, "Error {0} {1}".format(msg, code)
#
#         print "Step 4: Set default settings %s" % self.defaults_notification_settings
#         self.ns_handler.night_mode = self.defaults_notification_settings
#         msg, code = self.ns_handler.night_mode
#         assert code == 200, "Error {0} {1}".format(msg, code)
#         msg = json.loads(msg)
#         assert msg == self.defaults_notification_settings, "Error {0} {1}".format(msg, code)
#
#     def test_configure_and_update_all_modes_notification_settings(self):
#         print "----------------------------------"
#         print "Step 1: Get current all modes settings"
#         msg, code = self.ns_handler.all_modes
#         assert code == 200, "Error {0} {1}".format(msg, code)
#         msg = json.loads(msg)
#         assert msg == self.defaults_notification_settings, "Error {0} {1}".format(msg, code)
#
#         print "Step 2: Set new all modes settings %s" % self.new_notification_settings
#         self.ns_handler.all_modes = self.new_notification_settings
#
#         print "Step 3: Check new settings"
#         msg, code = self.ns_handler.all_modes
#         assert code == 200, "Error {0} {1}".format(msg, code)
#
#         msg = json.loads(msg)
#         assert msg == self.new_notification_settings, "Error {0} {1}".format(msg, code)
#
#         print "Step 4: Set default settings %s" % self.defaults_notification_settings
#         self.ns_handler.all_modes = self.defaults_notification_settings
#         msg, code = self.ns_handler.all_modes
#         assert code == 200, "Error {0} {1}".format(msg, code)
#         msg = json.loads(msg)
#         assert msg == self.defaults_notification_settings, "Error {0} {1}".format(msg, code)
#
#     def tearDown(self):
#         #self.sensor.unpair()
#         self.ns_handler.all_modes = self.defaults_notification_settings
#
#
# import string
# import random
#
# class HmsCustomModesTests(unittest.TestCase, PreConditionCheckMixin):
#     name = "NewCustomMode" + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(0, 9))
#
#     default_mode_settings = {
#       "runSettings": {
#           'current': False,
#           'paused': False,
#           'modeSchedules': [{'startTime': '11:00 AM', 'days': 127}]
#       }
#     }
#
#     expected_response = {
#       "runSettings": {
#           'current': False,
#           'paused': False,
#           'modeSchedules': [{'startTime': '11:00', 'days': 127}]
#       }
#     }
#
#     new_mode_settings = {
#       "runSettings": {
#           'current': False,
#           'paused': True,
#           'modeSchedules': [{'startTime': '11:00 AM', 'days': 127}]
#       }
#     }
#
#     def setUp(self):
#         self.check_configuration()
#         mod = __import__("py_frame.notification_settings")
#         self.mode = mod.notification_settings.CustomMode()
#
#     def test_create_get_update_delete_custom_mode(self):
#         print "----------------------------------"
#         print "----------Custom Modes------------"
#         print "----------------------------------"
#         print "Step 1: Create custom mode"
#         self.mode.create(self.name)
#
#         self.default_mode_settings["id"] = self.mode.id
#         self.default_mode_settings["name"] = self.name
#
#         self.new_mode_settings["id"] = self.mode.id
#         self.new_mode_settings["name"] = self.name
#
#         print "Step 2: Get custom mode"
#         data = self.mode.get()
#
#         data["runSettings"]["modeSchedules"][0].pop("id", 0)
#         assert data == self.expected_response, "Current {0}, Expected {1}".format(data, self.expected_response)
#
#         print "Step 3: Update custom mode"
#         data = self.mode.update(self.new_mode_settings)
#         data["runSettings"]["modeSchedules"][0].pop("id", 0)
#         assert data == self.new_mode_settings, "Current {0}, Expected {1}".format(data, self.new_mode_settings)
#
#         print "Step 4: Delete custom mode"
#         self.mode.delete()
#
#     def tearDown(self):
#         self.mode.delete()
#
#
# '''
#
# This functionality is not used anymore
#
# class HmsCurrentModeTests(unittest.TestCase, PreConditionCheckMixin):
#     def setUp(self):
#         self.check_configuration()
#         mod = __import__("py_frame.notification_settings")
#         self.mode = mod.notification_settings.CurrentMode()
#
#     def test_get_set_current_mode(self):
#         print "----------------------------------"
#         print "Step 1: Get current mode"
#         data = self.mode.get()
#         print "Current mode is {0}".format(data.keys()[0])
#         print "Step 2: Set Night mode"
#         data = self.mode.set('Night')
#         print "Step 3: Check new current mode"
#         assert data['name'] == "Night", "Mode was not set correctly. Current %s , Expected 'Night'" %data['name']
#
#     def tearDown(self):
#         data = self.mode.set('Home')
#         assert data['name'] == "Home", "Mode was not set correctly. Current %s , Expected 'Home'" %data['name']
#
# '''
#
# class DevicesTest(unittest.TestCase, PreConditionCheckMixin):
#     def setUp(self):
#         self.check_configuration()
#         self.sensor = Sensor()
#         self.device = Device()
#
#     def test_get_all_devices(self):
#         print "----------------------------------"
#         print "--------Test Pairing modes--------"
#         print "----------------------------------"
#
#         print "Step 1: Set pairing mode"
#         resp = self.sensor.set_pairing_mode()
#
#         assert (resp == 200), "Cannot set pairing mode"
#         print "Pairing mode is SUCCESSFULLY set"
#         print "----------------------------------"
#
#         print "Trying to get new devices"
#
#         json_data = self.device.get_new_devices()
#         before_addition = set([device["id"] for device in json_data["newDevices"]])
#
#         print "Step 2: Add sensor"
#         resp = self.sensor.add(type="MAGNET_CONTACT", mac_address="0000000091")
#         assert (resp == 200), "Cannot create new sensor"
#         print "Sensor is SUCCESSFULLY added"
#         print "----------------------------------"
#
#
#         sleep(35)
#         print "Trying to get new devices"
#         json_data2 = self.device.get_new_devices()
#         print "----------------------------------"
#         after_addition = set([device["id"] for device in json_data2["newDevices"]])
#
#         print "AFTER SET: ", after_addition
#         print
#         print "BEFORE SET: ", before_addition
#         difference_set = after_addition - before_addition
#         assert len(difference_set) == 1, "Expected count of new devises is 1, actual [%s]" % len(difference_set)
#
#
#         device_id = difference_set.pop()
#         print "new_device_id: ", device_id
#
#         resp = self.device.register_device(device_id)
#         print "Registed device responce: ", resp
#         sleep(35)
#         json_data3 = self.device.get_new_devices()
#         after_registration = set([device["id"] for device in json_data3["newDevices"]])
#
#         assert after_registration == before_addition, "Device was not removed from new devices list"
#
#         print "----------------------------------"
#         print "Step 5: Unpair sensor"
#         resp = self.sensor.unpair()
#         assert (resp == 200), "Cannot unpair sensor"
#         print "Sensor is unpaired"
#
#
#     def tearDown(self):
#         resp = self.sensor.unpair()
#         assert (resp == 200), "Cannot unpair sensor"
#         print "Sensor is unpaired"
#



if __name__ == "__main__":

    if platform.system() == "Darwin":
        sleep(20)
        result_file = "/tmp/results.xml"
    else:
        result_file = "results.xml"

    with open(result_file, 'wb') as output:
        unittest.main(
                    testRunner=xmlrunner.XMLTestRunner(output=output),
                    failfast=False, buffer=False, catchbreak=False, exit=False
                    )


    try:
        os.environ["BUILD_NUMBER"]
        get_log_links()
    except Exception, e:
        put_logs()

