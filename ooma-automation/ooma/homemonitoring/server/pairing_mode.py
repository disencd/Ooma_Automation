from homemonitoring.server.hms import HMS
import logging
import colorlog
import sys, os
import json
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.ERROR)
logger = logging.getLogger(__name__)

class PairingMode(object):

    def __init__(self, json_obj, node = "cert"):

        self.url = "api/base/status"
        self.mode = "pairingMode"
        self.json_obj = json_obj
        self.node = node
        self.cust_pk = self.json_obj["client_conf"]["cust_pk"]

    def get_cust_pk(self):
        self.cust_pk = self.json_obj["client_conf"]["cust_pk"]


    def enable(self):
        data = {self.mode: True}
        response = HMS(self.json_obj, self.node).request(self.url, self.cust_pk).post(data)
        logger.info("enable %s", response)
        return response

    def disable(self):
        data = {self.mode: False}
        response = HMS(self.json_obj, self.node).request(self.url, self.cust_pk).post(data)
        logger.info("disable %s", response)
        return response



