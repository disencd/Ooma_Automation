import logging
from virtual_sensor.hms_sql_query import HMSSqlQuery
from homemonitoring.setup.json_parse import JsonConfig
import fill_dds_request
import json
import ast
from homemonitoring.virtual_sensor.nimbits_actions import NimbitsActions
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Sensor_Action(object):
    def __init__(self, node = "cert"):
        self.nimbits_action = NimbitsActions()
        self.geturl = "service/v3/rest/me?name="
        self.posturl = "service/v3/rest/"

    def configure_door_Sensor(self, cust_pk):
        self.get_sensor_nimbits_request(cust_pk, "door")

    def get_sensor_nimbits_request(self, cust_pk, name):
        logger.info("get_sensor_nimbitsid started")

        device_id_dict = fill_dds_request.device_id_dict

        for devicename in device_id_dict[cust_pk].keys():
            get_url = self.geturl

            if "Sensor" not in devicename:

                get_url += device_id_dict[cust_pk][devicename]["deviceidentifier"]

                #logger.info("%s Geturl %s" %(devicename, get_url))

                response = self.nimbits_action.get_nimbits_events(cust_pk, get_url)

                if "Not" not in response:
                    nimbits_data = json.loads(response)
                    #logger.info("ID - %s" , nimbits_data['id'])
                    device_id_dict[cust_pk][devicename]["id"] = nimbits_data['id']


        logger.info(device_id_dict)

        logger.info("get_sensor_nimbitsid ended")
        fill_dds_request.device_id_dict = device_id_dict

    def post_sensor_events(self, cust_pk):
        device_id_dict = fill_dds_request.device_id_dict
        posturl = self.posturl + device_id_dict[cust_pk]["TamperDetector"]["id"] \
                            + "/series"


        logger.info("Nimbits Teamper Post URL = %s", posturl)

        data = "[{\"d\":1.0}]"

        response = self.nimbits_action.post_nimbits_events(posturl, cust_pk, data)