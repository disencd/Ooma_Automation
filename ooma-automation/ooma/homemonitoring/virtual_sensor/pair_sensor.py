import base64
import time, os
from collections import OrderedDict
from field_generator import FieldGenerator, DeviceDiscoveryGenerator
from fill_dds_request import DDS_data
from hms_actions import HMSActions
from homemonitoring.setup.json_parse import JsonConfig
from post_sensor_data import Post_sensor


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

    def pair_water_sensor(self, or_id):

        dd_req = DDS_data()
        _sensor_data = dd_req.fill_dds_flood_data(or_id)
        #
        # _start_timer = time.time()
        # response = self.post_sensor_data(_sensor_data, device_id, or_id)
        # _latency = time.time() - _start_timer
        # self.custom_timers['pair_water_sensor Time'] = _latency
        # print "Pairing the water Sensor - ", device_id
        # print response


    def pair_door_sensor(self, or_id):

        dd_req = DDS_data()
        _sensor_data = dd_req.fill_dds_windows_data(or_id)

        # _start_timer = time.time()
        # response = self.post_sensor_data(_sensor_data, device_id, or_id)
        # _latency = time.time() - _start_timer
        # self.custom_timers['pair_door_sensor Time'] = _latency
        #
        # print "Pairing the door Sensor - ", device_id
        # print response


    def pair_motion_sensor(self, or_id):

        dd_req = DDS_data()
        _sensor_data = dd_req.fill_dds_motion_data(or_id)

        # _start_timer = time.time()
        # response = self.post_sensor_data(_sensor_data, device_id, or_id)
        # _latency = time.time() - _start_timer
        # self.custom_timers['pair_motion_sensor Time'] = _latency
        #
        # print "Pairing the Motion Sensor - ", device_id
        # print response

    def sensor_status(self, or_id):
        post_obj = Post_sensor()
        response = post_obj.get_sensor_status(or_id)
        print response

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
