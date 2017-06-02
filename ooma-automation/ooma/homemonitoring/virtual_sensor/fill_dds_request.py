from field_generator import FieldGenerator, DeviceDiscoveryGenerator
#from pair_sensor import Sensor_Addition
from post_sensor_data import Post_sensor
from homemonitoring.setup.json_parse import JsonConfig
import os, json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DDS_data():
    def __init__(self):
        self.dd_gen = DeviceDiscoveryGenerator()
        self.json_obj = JsonConfig()
        self.sensor = Post_sensor()
        self.dds_cnt = 0

    def fill_dds_windows_data(self, or_id):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        dds_f_path =  abs_path + "/dds_config.json"
        self.dd_obj = self.json_obj.dump_config(dds_f_path)
        self.dd_gen.generate_uniqueID_for_sensor()
        self.dds_cnt += 1

        for key, val in self.dd_obj.iteritems():
            if key != "dds_std_header" and \
               key != "model_motion_sensor" and \
               key != "model_flood_sensor":

                deviceidentifier, dd_request = self.construct_dds_header(key)
                #logger.info("("%s %s" % (deviceidentifier, dd_request))
                response = self.sensor.post_sensor_data(dd_request, deviceidentifier, or_id)
                #logger.info("("%s %s %s" % (response, deviceidentifier, dd_request))

    def fill_dds_motion_data(self, or_id):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        dds_f_path =  abs_path + "/dds_config.json"
        self.dd_obj = self.json_obj.dump_config(dds_f_path)
        self.dd_gen.generate_uniqueID_for_sensor()
        self.dds_cnt += 1
        for key, val in self.dd_obj.iteritems():
            if key != "dds_std_header" and \
               key != "model_window_sensor" and \
               key != "model_flood_sensor":
                deviceidentifier, dd_request = self.construct_dds_header(key)
                response = self.sensor.post_sensor_data(dd_request, deviceidentifier, or_id)
                #logger.info("(response, deviceidentifier,dd_request)

    def fill_dds_flood_data(self, or_id):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        dds_f_path =  abs_path + "/dds_config.json"
        self.dd_obj = self.json_obj.dump_config(dds_f_path)
        self.dd_gen.generate_uniqueID_for_sensor()
        self.dds_cnt += 1
        for key, val in self.dd_obj.iteritems():
            if key != "dds_std_header" and \
               key != "model_motion_sensor" and \
               key != "model_window_sensor":
                deviceidentifier, dd_request = self.construct_dds_header(key)
                self.sensor.post_sensor_data(dd_request, deviceidentifier, or_id)
                #logger.info("("%s %s %s" % (response, deviceidentifier, dd_request))

    def construct_dds_header(self, key):
        dd_request = {}
        # Adding the standard headers in DDS
        dd_request = self.dd_obj["dds_std_header"]

        if "rootId" in self.dd_obj[key]["deviceAttributes"].keys():

            self.dd_obj[key]["deviceAttributes"] \
                 ["rootId"] = self.dd_gen.generate_rootId()
            # self.dd_obj[key]["deviceAttributes"]["rootId"] = \
            #     self.dd_gen.generate_deviceId(self.dds_cnt, self.dd_obj \
            #         [key]["deviceAttributes"]["rootId"])

        if "rootId" not in self.dd_obj[key]["deviceAttributes"].keys():
            self.dd_obj[key]["deviceAttributes"]["deviceId"] = \
                                        self.dd_gen.generate_rootId()
        else:
            self.dd_obj[key]["deviceAttributes"]["deviceId"] = \
                self.dd_gen.generate_deviceId(self.dds_cnt, self.dd_obj \
                        [key]["deviceAttributes"]["deviceId"])

        #Device Identifier is -Flood Sensor-root
        deviceidentifier = self.dd_obj[key]["deviceIdentifier"]

        self.dd_obj[key]["deviceIdentifier"] = \
            self.dd_gen.generate_deviceIdentifier(deviceidentifier)

        #Device Identifier is Updated 4536027208-Flood Sensor-root
        deviceidentifier = self.dd_obj[key]["deviceIdentifier"]

        # Adding the model headers
        dd_request["model"] = \
            self.dd_obj[key]

        return deviceidentifier, dd_request

# obj = DDS_data()
#
# obj.fill_dds_flood_data()
#
# logger.info(" "__________________________"
#
# obj.fill_dds_motion_data()
#
# logger.info(" "__________________________"
#
# obj.fill_dds_windows_data()
#
# logger.info(" "__________________________"