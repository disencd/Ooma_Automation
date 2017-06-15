from field_generator import FieldGenerator, DeviceDiscoveryGenerator, SensorNamegenerator
#from pair_sensor import Sensor_Addition
from post_sensor_data import Post_sensor
from homemonitoring.setup.json_parse import JsonConfig
import os, json
import logging
import colorlog

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)
global device_id_dict
device_id_dict = {}

class DDS_data():
    def __init__(self):
        self.dd_gen = DeviceDiscoveryGenerator()
        self.json_obj = JsonConfig()
        self.sensor = Post_sensor()
        self.dds_cnt = 0
        self.sensorname_obj = SensorNamegenerator()

    def fill_dds_windows_data(self, cust_pk):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        dds_f_path =  abs_path + "/dds_config.json"
        self.dd_obj = self.json_obj.dump_config(dds_f_path)
        self.dd_gen.generate_uniqueID_for_sensor()
        self.dds_cnt += 1
        sen_cnt, sensor_name = self.sensorname_obj.generate_sensor_name(cust_pk, "door")

        #Dictionary used for generating events using device ids
        device_id_dict[cust_pk] = {}
        device_id_dict[cust_pk][sensor_name] = {}
        for key, val in self.dd_obj.iteritems():
            if key != "dds_std_header" and \
               key != "model_motion_sensor" and \
               key != "model_flood_sensor":

                deviceidentifier, dd_request = self.construct_dds_header(key)
                logger.info("%s %s" % (deviceidentifier, dd_request))
                device_id_dict[cust_pk][sensor_name][self.dd_obj[key]["deviceName"]] = {}
                device_id_dict[cust_pk][sensor_name][self.dd_obj[key]["deviceName"]] \
                                    ["deviceidentifier"] = deviceidentifier
                response = self.sensor.post_sensor_data(dd_request, deviceidentifier, cust_pk)
                logger.info("response - %s deviceidentifier %s dd_request %s" % (response, deviceidentifier, dd_request))

        logger.info("device_id_dict = %s", device_id_dict)

    def fill_dds_motion_data(self, cust_pk):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        dds_f_path =  abs_path + "/dds_config.json"
        self.dd_obj = self.json_obj.dump_config(dds_f_path)
        self.dd_gen.generate_uniqueID_for_sensor()
        self.dds_cnt += 1
        sen_cnt, sensor_name = self.sensorname_obj.generate_sensor_name(cust_pk, "motion")
        #Dictionary used for generating events using device ids
        device_id_dict[cust_pk] = {}
        device_id_dict[cust_pk][sensor_name] = {}
        for key, val in self.dd_obj.iteritems():
            if key != "dds_std_header" and \
               key != "model_window_sensor" and \
               key != "model_flood_sensor":
                deviceidentifier, dd_request = self.construct_dds_header(key)
                device_id_dict[cust_pk][sensor_name][self.dd_obj[key]["deviceName"]] = {}
                device_id_dict[cust_pk][sensor_name][self.dd_obj[key]["deviceName"]] \
                                    ["deviceidentifier"] = deviceidentifier

                response = self.sensor.post_sensor_data(dd_request, deviceidentifier, cust_pk)
                #logger.info("(response, deviceidentifier,dd_request)

        logger.info("device_id_dict = %s", device_id_dict)

    def fill_dds_flood_data(self, cust_pk):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        dds_f_path =  abs_path + "/dds_config.json"
        self.dd_obj = self.json_obj.dump_config(dds_f_path)
        self.dd_gen.generate_uniqueID_for_sensor()
        self.dds_cnt += 1

        sen_cnt, sensor_name = self.sensorname_obj.generate_sensor_name(cust_pk, "water")
        #Dictionary used for generating events using device ids
        device_id_dict[cust_pk] = {}

        for key, val in self.dd_obj.iteritems():
            if key != "dds_std_header" and \
               key != "model_motion_sensor" and \
               key != "model_window_sensor":
                deviceidentifier, dd_request = self.construct_dds_header(key)
                self.sensor.post_sensor_data(dd_request, deviceidentifier, cust_pk)
                #logger.info("("%s %s %s" % (response, deviceidentifier, dd_request))
                device_id_dict[cust_pk][sensor_name][self.dd_obj[key]["deviceName"]] = {}
                device_id_dict[cust_pk][sensor_name][self.dd_obj[key]["deviceName"]] \
                                    ["deviceidentifier"] = deviceidentifier

        logger.info("device_id_dict = %s", device_id_dict)

    def construct_dds_header(self, key):
        dd_request = {}
        # adding the standard headers in dds
        dd_request = self.dd_obj["dds_std_header"]

        if "rootid" in self.dd_obj[key]["deviceAttributes"].keys():

            self.dd_obj[key]["deviceAttributes"] \
                 ["rootid"] = self.dd_gen.generate_rootid()
            logger.info("rootid - %s", self.dd_obj[key]["deviceAttributes"]["rootid"])
            # self.dd_obj[key]["deviceattributes"]["rootid"] = \
            #     self.dd_gen.generate_deviceid(self.dds_cnt, self.dd_obj \
            #         [key]["deviceattributes"]["rootid"])

        if "rootId" not in self.dd_obj[key]["deviceAttributes"].keys():
            self.dd_obj[key]["deviceAttributes"]["deviceId"] = \
                                        self.dd_gen.generate_rootId()
            logger.info("First time - Root - Device ID  %s", self.dd_obj[key]["deviceAttributes"]["deviceId"])
        else:
            self.dd_obj[key]["deviceAttributes"]["deviceId"] = \
                self.dd_gen.generate_deviceid(self.dds_cnt, self.dd_obj \
                        [key]["deviceAttributes"]["deviceId"])
            logger.info("Next time onwards - Device ID  %s", self.dd_obj[key]["deviceAttributes"]["deviceId"])
            logger.info("Next time onwards - rootId %s", self.dd_obj[key]["deviceAttributes"]["rootId"])

        #device identifier is -flood sensor-root
        deviceidentifier = self.dd_obj[key]["deviceIdentifier"]
        logger.info("Before - deviceidentifier %s", deviceidentifier)
        self.dd_obj[key]["deviceIdentifier"] = \
            self.dd_gen.generate_deviceIdentifier(deviceidentifier)

        #device identifier is updated 4536027208-flood sensor-root
        deviceidentifier = self.dd_obj[key]["deviceIdentifier"]
        logger.info("After - deviceidentifier %s", deviceidentifier)
        # adding the model headers
        dd_request["model"] = \
            self.dd_obj[key]

        return deviceidentifier, dd_request

# obj = dds_data()
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