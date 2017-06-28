import urllib2
import requests
import logging
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.virtual_sensor.hms_sql_query import HMSSqlQuery
import json, base64
import time
from homemonitoring.setup.hms_logging import HmsLogging
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/tmp/listener.log')
fh.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


class HMSActions(HMSSqlQuery):
    def __init__(self, jsonconfig, node="cert"):
        self.node = node
        self._jsonconfig = jsonconfig
        self.__url = None

    '''
     Creating new account
     POST https://hms1-cert1.cn.ooma.com:8084/hms/oss/vn5j9av6ru7hjue7fpzek3r73m4ec8mq
     {
        "orUsername":"ui89dg3p4",
        "orPassword":"YmJoajlqaWJi",
        "nimbitsUsername":"sun2pfbjr@ooma.com",
        "nimbitsPassword":"dmdlZmc3OWV2",
        "spn":"9712732945",
        "timezone":"America/Los_Angeles"
     }
    '''
    def vs_request_activate(self, hostname_port, req_url, cust_pk):
        self.__url = "https://{0}/{1}/{2}".format(hostname_port, req_url, cust_pk)
        return self

    '''
    Creating new account
     POST http://hms1-cert1.cn.ooma.com:8084/hms/oss/vn5j9av6ru7hjue7fpzek3r73m4ec8mq
     {
        "orUsername":"ui89dg3p4",
        "orPassword":"YmJoajlqaWJi",
        "nimbitsUsername":"sun2pfbjr@ooma.com",
        "nimbitsPassword":"dmdlZmc3OWV2",
        "spn":"9712732945",
        "timezone":"America/Los_Angeles"
     }
    '''
    def vs_oss_request_activate(self, hostname_port, req_url, cust_pk):
        self.__url = "http://{0}/{1}/{2}".format(hostname_port, req_url, cust_pk)
        return self

    '''
    Adding sensor
    Post : http://hms1-cert1.cn.ooma.com:8083/dds/rest/rpc/devicediscovery/2/0/0/devicediscovery/124
    '''
    def vs_request_add_sensor(self, hostname_port, req_url):
        logger.info("hostname_port - %s", hostname_port)
        self.__url = "http://{0}/{1}".format(hostname_port, req_url)
        return self


    def post(self, headers, data):
        assert self.__url is not None, "Use 'request' method to specify URL"
        assert isinstance(data, dict)\
                or isinstance(data, list), "Data should be dictionary or list"
        data = json.dumps(data)
        logger.info("post ")
        try:
            logger.info(" __url %s" , self.__url)
            request = urllib2.Request(self.__url, data, headers)
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            logger.info("data %s code %s" % (data, code))
            return code
        except urllib2.URLError as e:
            logger.info("code - %s reason %s" % (e.code, e.read()))
            assert "HMS Activation Failed"
            return e.reason


    def get(self, headers = None, data = None):
        assert self.__url is not None, "Use 'request' method to specify URL"
        data = json.dumps(data)
        headers = json.dumps(headers)
        try:
            request = urllib2.Request(self.__url)
            request.add_header('Content-Type', 'application/json')
            #Not needed for all the get messages
            request.add_header("X-ooma-oToken", "TrustMe")
            response = urllib2.urlopen(request)
            #data = response.read()
            data = json.load(response)
            logger.info(" data =  %s" , data)
            response.close()
            return data
        except urllib2.URLError as e:
            logger.info("Activation Failure - Reason %s", e.reason)
            assert "HMS Activation Failed"
            return e.reason

    def sensor_get(self, or_dict):
        assert self.__url is not None, "Use 'request' method to specify URL"

        # Basic Authentication Algorithm
        b64_str = or_dict['beehive_id'] + ":" + or_dict['beehive_pwd']
        base64string = base64.b64encode(b64_str)
        auth_str = "Basic " + base64string
        logger.info(" auth_str - %s", auth_str)
        try:
            request = urllib2.Request(self.__url)
            request.add_header('Authorization', auth_str)
            request.add_header('Content-Type', "application/vnd.openremote.device-discovery+json")
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError as e:
            return e.reason


    def delete(self, headers, data):
        assert self.__url is not None, "Use 'request' method to specify URL"
        try:
            request = urllib2.Request(self.__url, data, headers)
            request.get_method = lambda: "DELETE"
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError as e:
            return e.reason

    def patch(self, headers, data):
        assert self.__url is not None, "Use 'request' method to specify URL"
        data = json.dumps(data)
        headers = json.dumps(headers)

        try:
            logger.info(" PATCH ")
            request = urllib2.Request(self.__url, data)
            request.get_method = lambda: "PATCH"
            request.add_header('Content-Type', 'application/json')
            request.add_header("X-ooma-oToken", "TrustMe")
            request.add_header('Accept', 'application/json')
            logger.info("request.headers - ", request.headers)
            logger.info("request.data - ", request.data)
            #request.add_data(json.dumps(data))
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError as e:
            return e.reason

    def get_register_sensor(self, url):
        logger.info("get_register_sensor started")
        assert url is not None, "Use 'request' method to specify URL"
        try:
            time.sleep(5)
            response = requests.get(url)
            resp = response.json()
            #logger.info("response = %s", resp)
            return resp
        except urllib2.URLError as e:
            logger.info(e.reason)
            return e.reason

    def post_register_sensor(self, url, data):
        # logger.info(" url
        headers = {
            'Accept': 'application/json'
        }
        # assert url is not None, "Use 'request' method to specify URL"
        # assert isinstance(data, dict) \
        #        or isinstance(data, list), "Data should be dictionary or list"
        data = json.dumps(data)
        #logger.info("data - %s", data)
        headers = {
            "Content-Type": "application/json"
        }
        try:

            logger.info(" url - %s", url)
            request = urllib2.Request(url, data, headers)
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            logger.info("data %s, code %s" % (data, code))
            response.close()

            return code
        except urllib2.URLError as e:
            logger.info("code - %s reason %s" % (e.code, e.read()))
            return e.code


# json_obj = JsonConfig()
# hms = HMSActions(json_obj)
# res = hms.get_register_sensor("http://hms1-cert1.cn.ooma.com:8084/hms/api/base/status?username=virtualaccount20170603150648554833")
# print res