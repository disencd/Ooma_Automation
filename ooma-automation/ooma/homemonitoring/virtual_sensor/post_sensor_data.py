from field_generator import FieldGenerator, DeviceDiscoveryGenerator
#from pair_sensor import Sensor_Addition
from homemonitoring.setup.json_parse import JsonConfig
#from fill_dds_request import DDS_data
import os, json
from virtual_sensor.hms_sql_query import HMSSqlQuery
import base64
import time
import urllib2
from collections import OrderedDict
#from fill_dds_request import DDS_data
from hms_actions import HMSActions


class Post_sensor(object, HMSSqlQuery):
    def __init__(self, node="cert"):
        self.custom_timers = {}
        self.node = node
        self.json_obj = JsonConfig()
        self.json_server_obj = self.json_obj.dump_config("../server_config.json")
        self.json_server = self.json_server_obj[self.node]["beehive-server"]
        self.dd_gen = DeviceDiscoveryGenerator()
        self.url = "dds/rest/rpc/devicediscovery/2/0/0/devicediscovery"

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

    def construct_sensor_headers(self, or_id):

        # Calling the hms_sql_query class for getting OR credentials
        self.or_dict = super(Post_sensor, self).sql_query(or_id)

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
