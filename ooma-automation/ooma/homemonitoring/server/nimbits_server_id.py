import urllib2
import colorlog
import os, time
import json, base64
import logging
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.virtual_sensor.hms_sql_query import HMSSqlQuery
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NimbitsServerIDs(object, HMSSqlQuery):
    def __init__(self, node="cert"):
        self.node = node
        self.__url = "/service/v3/rest/me?name=logPoint"
        self.node = node
        self.or_dict = {}
        self.json_obj = JsonConfig()
        abs_path = os.path.dirname(os.path.abspath(__file__))

        server_f_path =  abs_path + "/../server_config.json"
        self.json_server_obj = self.json_obj.dump_config(server_f_path)
        self.json_server = self.json_server_obj[self.node]["nimbits-server"]

    def generate_url(self, req_url):
        return "https://{0}/{1}".format(self.json_server, req_url)

    def generate_http_url(self, req_url):
        return "http://{0}/{1}".format(self.json_server, req_url)

    def construct_nimbits_request_headers(self, cust_pk, or_dict):
        logger.info("construct_nimbits_request_headers started")
        logger.info("OR Dict - %s", or_dict)

        if "beehive_id" not in or_dict.keys():
            # Calling the hms_sql_query class for getting OR credentials
            or_dict = super(NimbitsServerIDs, self).sql_query_pk(cust_pk)

        self.auth_str = 'basic ' + or_dict['nimbits_id'] + ':' + \
                                or_dict['nimbits_pwd']

        self.headers = {
            'Accept': 'application/json',
            'Content-Type':'application/json'
        }


        logger.info("construct_nimbits_request_headers ended")
        return self.headers, or_dict

    def get_nimbits_logeventid(self, cust_pk):
        logger.debug("get_nimbits_events started")
        geturl = "service/v3/rest/me?name=logPoint"
        self.__url = self.generate_http_url(geturl)
        logger.info("__url %s ", self.__url)
        self.headers, self.or_dict = self.construct_nimbits_request_headers(cust_pk, \
                                                                        self.or_dict)

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
            id_data = json.loads(data)
            logger.info("data %s, code %s" % (data, code))
            #logger.info("response %s" , response)
            logger.info("get_nimbits_events ended")
            return id_data["id"]
        except urllib2.URLError as e:
            logger.info("code - %s reasone %s" % (e.code, e.read()))
            return e.code