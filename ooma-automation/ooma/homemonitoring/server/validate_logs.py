import urllib2
import requests
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.server.nimbits_server_id import NimbitsServerIDs
from homemonitoring.server.nimbits_sql_query import NimbitsSqlQuery

import json, base64
import time
import logging
import colorlog

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.ERROR)
logger = logging.getLogger(__name__)

class Validate_Logs():
    def __init__(self, custpk):
        self.custpk = custpk

    def get_latest_logevent(self):
        logger.info("get_latest_logevent Started")
        nim_id = NimbitsServerIDs()
        log_id = nim_id.get_nimbits_logeventid(self.custpk)
        logger.info("Nimbits ID = %s", log_id)

        log_obj = NimbitsSqlQuery()
        log_obj.sql_query_pk(log_id)

        logger.info("get_latest_logevent Ended")

# obj = Validate_Logs("c3bw6mu485ea3z67tnjcqws7dhuv5wsv")
# obj.get_latest_logevent()