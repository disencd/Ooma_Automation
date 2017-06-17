import logging
import json
import ast
import fill_dds_request
from homemonitoring.virtual_sensor.hms_sql_query import HMSSqlQuery
from homemonitoring.setup.mongodb_setup import MongoDBQuery
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.virtual_sensor.nimbits_actions import NimbitsActions
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Sensor_Action(object):
    def __init__(self, node = "cert"):
        self.nimbits_action = NimbitsActions()
        self.geturl = "service/v3/rest/me?name="
        self.posturl = "service/v3/rest/"

    def configure_door_Sensor(self, cust_pk, name):
        logger.info("configure_door_Sensor started")
        _mong_obj = MongoDBQuery()
        logger.info("cust_pk %s", cust_pk)
        iface_dict = _mong_obj.mongo_find_one_dictionary("SensorInterface_collection",\
                                                     cust_pk, name)
        logger.info("iface_dict - %s ", iface_dict)

        if "id" not in iface_dict["Announcement"].keys():
            iface_dict = self.get_sensor_nimbits_request(cust_pk, iface_dict)

            #update the iface_dict to mongo
            _mong_obj.mongo_update("SensorInterface_collection", iface_dict)
        else:
            logger.info("Dictionary already configured")

        logger.info("configure_door_Sensor ended")

    def get_sensor_nimbits_request(self, cust_pk, iface_dict):
        logger.info("get_sensor_nimbitsid started")

        for devicename in iface_dict.keys():
            get_url = self.geturl

            #Removing the cust_pk, sensorname and _id
            if "cust_pk" not in devicename and \
                "sensorname" not in devicename and \
                "_id" not in devicename:

                get_url += iface_dict[devicename]["deviceidentifier"]

                logger.info("%s Geturl %s" %(devicename, get_url))

                response = self.nimbits_action.get_nimbits_events(cust_pk, get_url)

                if "404" != str(response):
                    nimbits_data = json.loads(response)
                    #logger.info("ID - %s" , nimbits_data['id'])
                    iface_dict[devicename]["id"] = nimbits_data['id']


        logger.info(iface_dict)

        logger.info("get_sensor_nimbitsid ended")
        return iface_dict

    def post_sensor_events(self, cust_pk):
        device_id_dict = fill_dds_request.device_id_dict
        posturl = self.posturl + device_id_dict[cust_pk]["TamperDetector"]["id"] \
                            + "/series"


        logger.info("Nimbits Tamper Post URL = %s", posturl)

        data = "[{\"d\":1.0}]"

        response = self.nimbits_action.post_nimbits_events(posturl, cust_pk, data)