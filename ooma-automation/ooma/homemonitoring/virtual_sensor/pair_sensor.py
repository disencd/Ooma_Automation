import base64
import time, os
import logging
from collections import OrderedDict
from field_generator import FieldGenerator, DeviceDiscoveryGenerator
from fill_dds_request import DDS_data
from hms_actions import HMSActions
from homemonitoring.setup.json_parse import JsonConfig
from post_sensor_data import Post_sensor
from register_sensor import Register_sensor
from homemonitoring.setup.hms_logging import HmsLogging

logger = logging.getLogger(__name__)

class Sensor_Addition(object):
    def __init__(self, node = "cert"):
        self.custom_timers = {}
        self.node = node
        self.json_obj = JsonConfig()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        server_f_path = abs_path + "/../server_config.json"
        self.json_server_obj = self.json_obj.dump_config(server_f_path)
        self.json_server = self.json_server_obj[self.node]["beehive-server"]


    '''
    POST /dds/rest/rpc/devicediscovery/2/0/0/devicediscovery/disen_sensor_water HTTP/1.1
    Host: beehive-cert.hms.ooma.com:8083
    Authorization: Basic MzlyNXRoOHJyOnVtbTdqNHpheg==
    Content-Type: application/vnd.openremote.device-discovery+json
    Cache-Control: no-cache
    Postman-Token: db7873ac-1889-27de-0089-0b5a71229383  
    '''

    def pair_water_sensor(self, cust_pk):

        dd_req = DDS_data()
        sensor_dict, sensor_name = dd_req.fill_dds_flood_data(cust_pk)

        reg_sensor = Register_sensor(sensor_name, sensor_dict)

        reg_sensor.register_water_sensor(cust_pk)
        #
        # _start_timer = time.time()
        # response = self.post_sensor_data(_sensor_data, device_id, or_id)
        # _latency = time.time() - _start_timer
        # self.custom_timers['pair_water_sensor Time'] = _latency
        # logger.info(" "Pairing the water Sensor - ", device_id
        # logger.info(" response


    def pair_door_sensor(self, cust_pk):

        dd_req = DDS_data()
        sensor_dict, sensor_name = dd_req.fill_dds_windows_data(cust_pk)

        reg_sensor = Register_sensor(sensor_name, sensor_dict)

        reg_sensor.register_door_sensor(cust_pk)

        # _start_timer = time.time()
        # response = self.post_sensor_data(_sensor_data, device_id, or_id)
        # _latency = time.time() - _start_timer
        # self.custom_timers['pair_door_sensor Time'] = _latency
        #
        # logger.info(" "Pairing the door Sensor - ", device_id
        # logger.info(" response


    def pair_motion_sensor(self, cust_pk):

        dd_req = DDS_data()
        sensor_dict, sensor_name = dd_req.fill_dds_motion_data(cust_pk)

        reg_sensor = Register_sensor(sensor_name, sensor_dict)

        reg_sensor.register_motion_sensor(cust_pk)

        # _start_timer = time.time()
        # response = self.post_sensor_data(_sensor_data, device_id, or_id)
        # _latency = time.time() - _start_timer
        # self.custom_timers['pair_motion_sensor Time'] = _latency
        #
        # logger.info(" "Pairing the Motion Sensor - ", device_id
        # logger.info(" response

    def sensor_status(self, cust_pk):
        post_obj = Post_sensor()
        response = post_obj.get_sensor_status(cust_pk)
        logger.info(" response %s", response)

#     def run(self):
#         self.pair_water_sensor("1263")
#
#         time.sleep(1)
#
#         self.pair_door_sensor("1263")
#
#         time.sleep(1)
#
#         self.pair_motion_sensor("1263")
#
#         time.sleep(1)
#
#         self.sensor_status("1263")
#
# if __name__ == "__main__":
#     trans = Sensor_Addition()
#     trans.run()
