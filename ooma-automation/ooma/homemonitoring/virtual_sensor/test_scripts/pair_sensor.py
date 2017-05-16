import urllib2
import time
from collections import OrderedDict
from hms_actions import HMSActions
from field_generator import FieldGenerator, DeviceDiscoveryGenerator
from fill_dds_request import DDS_data
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.virtual_sensor.test_scripts.hms_sql_query import HMSSqlQuery
import base64

class Transaction2(object, HMSSqlQuery):
    def __init__(self, node = "cert"):
        self.custom_timers = {}
        self.node = node
        self.json_obj = JsonConfig()
        self.json_server_obj = self.json_obj.dump_config("../../server_config.json")
        self.json_server = self.json_server_obj[self.node]["beehive-server"]
        self.dd_gen = DeviceDiscoveryGenerator()
        self.url = "dds/rest/rpc/devicediscovery/2/0/0/devicediscovery"

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
        _sensor_data = dd_req.fill_dds_data("water")
        device_id = dd_req.fill_deviceidentifier("water", "BatteryIndicator-U1")
        _start_timer = time.time()
        response = self.post_sensor_data(_sensor_data, device_id, or_id)
        _latency = time.time() - _start_timer
        self.custom_timers['pair_water_sensor Time'] = _latency
        print "Pairing the water Sensor - ", device_id
        print response


    def pair_door_sensor(self, or_id):

        dd_req = DDS_data()
        _sensor_data = dd_req.fill_dds_data("door")
        device_id = dd_req.fill_deviceidentifier("door", "BatteryIndicator-U1")

        _start_timer = time.time()
        response = self.post_sensor_data(_sensor_data, device_id, or_id)
        _latency = time.time() - _start_timer
        self.custom_timers['pair_door_sensor Time'] = _latency

        print "Pairing the door Sensor - ", device_id
        print response


    def pair_motion_sensor(self, or_id):

        dd_req = DDS_data()
        _sensor_data = dd_req.fill_dds_data("motion")
        device_id = dd_req.fill_deviceidentifier("motion", "BatteryIndicator-U1")

        _start_timer = time.time()
        response = self.post_sensor_data(_sensor_data, device_id, or_id)
        _latency = time.time() - _start_timer
        self.custom_timers['pair_motion_sensor Time'] = _latency

        print "Pairing the Motion Sensor - ", device_id
        print response

    def construct_sensor_headers(self, or_id):

        # Calling the hms_sql_query class for getting OR credentials
        self.or_dict = super(Transaction2, self).sql_query(or_id)

        # Basic Authentication Algorithm
        b64_str = self.or_dict['beehive_id'] + ":" + self.or_dict['beehive_pwd']
        base64string = base64.b64encode(b64_str)
        auth_str = "Basic " + base64string
        print auth_str
        _headers = {
            'Content-Type': 'application/vnd.openremote.device-discovery+json',
            'Authorization': auth_str
        }
        return _headers

    def post_sensor_data(self, sensor_data, device_id, or_id):

        _headers = self.construct_sensor_headers(or_id)
        print sensor_data

        #Posting the urls
        response = HMSActions(self.json_obj, self.node).vs_request_activate(self.json_server, self.url, device_id). \
             post(_headers, sensor_data)
        print response

        return response

    def get_sensor_status(self, or_id):

        _headers = self.construct_sensor_headers(or_id)
        # Posting the urls
        response = HMSActions(self.json_obj, self.node).vs_request_add_sensor(self.json_server, self.url). \
            sensor_get(self.or_dict)
        print response
        return response

    def run(self):
        self.pair_water_sensor("1263")

        time.sleep(1)

        self.get_sensor_status("1263")

if __name__ == "__main__":
    trans = Transaction2()
    trans.run()
