import logging
from virtual_sensor.hms_sql_query import HMSSqlQuery
from homemonitoring.setup.json_parse import JsonConfig
import json
import ast

from homemonitoring.virtual_sensor.nimbits_actions import NimbitsActions
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Sensor_Action(object):
    def __init__(self, node = "cert"):
        self.nimbits_action = NimbitsActions()

        #Different Events generated from sensor
        self.nimbits_events_id = {
                                "-TamperDetector-U1" : "",
                                "-BatteryIndicator-U1" :"",
                                "-IdentifyInputDevice-U1" : "",
                                "-Alert-U1" : "",
                                "-RSSI128-U1" : "",
                                "-ActiveDevice-U1" : ""
                            }

    def configure_door_Sensor(self, cust_pk):
        self.get_sensor_nimbits_request(cust_pk, "door")

    def fill_eventids_from_interfaces(self, data):


        #Traverse through the nimbits_events_id keys
        for key in self.nimbits_events_id.keys():
            #traverse through "children" dictionary in nimbits GET
            for i in range(len(data["children"])):
                logger.info("key - %s child key %s " %
                            (key, data["children"][i]["name"]))

                if data["children"][i]["name"] == key and \
                    "pointType" in data["children"][i].keys():

                    self.nimbits_events_id[key] = data["children"][i]["id"]
                    logger.info("id - %s", data["children"][i]["id"])

    def get_sensor_nimbits_request(self, cust_pk, name):
        logger.info("get_sensor_nimbitsid started")
        response = self.nimbits_action.get_nimbits_events(cust_pk)

        self.fill_eventids_from_interfaces(response)
        logger.info("get_sensor_nimbitsid ended")

    def post_sensor_events(self):
        pass