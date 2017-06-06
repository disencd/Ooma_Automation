import urllib2
import os
import json, base64
import logging
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.virtual_sensor.hms_sql_query import HMSSqlQuery

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NimbitsActions(object, HMSSqlQuery):
    def __init__(self, node="cert"):
        self.node = node
        self.__url = None
        self.or_dict = {}
        self.node = node
        self.json_obj = JsonConfig()
        abs_path = os.path.dirname(os.path.abspath(__file__))

        server_f_path =  abs_path + "/../server_config.json"
        self.json_server_obj = self.json_obj.dump_config(server_f_path)
        self.json_server = self.json_server_obj[self.node]["nimbits-server"]



    def generate_url(self, req_url):
        return "http://{0}/{1}".format(self.json_server, req_url)

    def construct_nimbits_request_headers(self, cust_pk):
        if "beehive_id" not in self.or_dict.keys():
            # Calling the hms_sql_query class for getting OR credentials
            self.or_dict = super(NimbitsActions, self).sql_query_pk(cust_pk)

        self.auth_str = 'basic ' + self.or_dict['nimbits_id'] + ':' + \
                                self.or_dict['nimbits_pwd']

        self.headers = {
            'Accept': 'application/json',
            'Content-Type':'application/json'
        }
        return self.headers

    def get_nimbits_events(self, cust_pk, geturl):
        logger.debug("get_nimbits_events started")

        self.__url = self.generate_url(geturl)

        self.headers = self.construct_nimbits_request_headers(cust_pk)
        logger.info("Nimbits URL - %s", self.__url)
        logger.info("Nimbits Headers - %s", self.headers)

        assert self.__url is not None, "Use 'request' method to specify URL"
        headers = json.dumps(self.headers)
        try:
            request = urllib2.Request(self.__url)
            request.add_header('Authorization', self.auth_str)
            #request.add_header('Accept', 'application/json')
            response = urllib2.urlopen(request)

            #response = json.load(response)
            data = response.read()
            code = response.getcode()
            response.close()
            logger.info("data %s, code %s" % ( data, code))
            #logger.info("response %s" , response)
            logger.info("get_nimbits_events ended")
            return data
        except urllib2.URLError as e:
            logger.info("e.reason - %s", e.reason)
            return e.reason

    def post_nimbits_events(self, posturl, cust_pk, data):
        self.__url = self.generate_url(posturl)
        self.headers = self.construct_nimbits_request_headers(cust_pk)

        data = json.dumps(data)
        logger.info("Nimbits data %s", data)
        try:
            logger.info("Post Nimbits url %s", self.__url)
            request = urllib2.Request(self.__url, data, self.headers)
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            logger.info(" data %s, code %s "% (data, code))
            return code
        except urllib2.URLError as e:
            return e.reason