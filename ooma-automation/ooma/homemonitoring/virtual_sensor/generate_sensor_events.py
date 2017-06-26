import logging
import json, time
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
        logger.info("Configuring cust_pk %s", cust_pk)
        iface_dict = _mong_obj.mongo_find_one_dictionary("SensorInterface_collection",\
                                                     cust_pk, name)
        logger.info("iface_dict - %s ", iface_dict)

        if "id" not in iface_dict["Announcement"].keys():
            time.sleep(3)
            iface_dict = self.get_sensor_nimbits_request(cust_pk, iface_dict)

            time.sleep(3)
            #update the iface_dict to mongo SensorInterface_collection
            _mong_obj.mongo_update("SensorInterface_collection", iface_dict)
        else:
            logger.info("SensorInterface Dictionary already configured")

        logger.info("configure_door_Sensor ended")
        return iface_dict

    def get_sensor_nimbits_request(self, cust_pk, iface_dict):
        logger.info("get_sensor_nimbitsid started")
        or_dict = {}
        for devicename in iface_dict.keys():
            get_url = self.geturl

            #Removing the cust_pk, sensorname and _id
            if "cust_pk" not in devicename and \
                "sensorname" not in devicename and \
                "_id" not in devicename:

                get_url += iface_dict[devicename]["deviceidentifier"]

                logger.info("%s Geturl %s" %(devicename, get_url))

                response, or_dict = self.nimbits_action.get_nimbits_events(cust_pk, get_url, or_dict)
                time.sleep(3)
                if "404" != str(response):
                    nimbits_data = json.loads(response)
                    #logger.info("ID - %s" , nimbits_data['id'])
                    iface_dict[devicename]["id"] = nimbits_data['id']


        logger.info(iface_dict)

        logger.info("get_sensor_nimbitsid ended")
        return iface_dict

    def trigger_sensor_events(self, config_dict):
        logger.info("Trigger_sensor_events started")
        _mong_obj = MongoDBQuery()
        logger.info("Querying Nimbits Details of cust_pk %s", config_dict["cust_pk"])

        mongo_dict = _mong_obj.mongo_find_one_element("UserCredentials_collection", \
                                config_dict["cust_pk"])

        auth_str = 'basic ' + mongo_dict['nimbits_id'] + ':' + \
                                mongo_dict['nimbits_pwd']

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'

        }
        url = self.posturl + config_dict["TamperDetector"]["id"] \
                            + "/series"

        logger.info("Event Generation Post URL for %s", url)
        sensor_trigger = {}
        sensor_trigger["Authorization"] = auth_str
        sensor_trigger["headers"] = headers
        sensor_trigger["no_events"] = config_dict["no_events"]
        sensor_trigger["time_interval"] = config_dict["time_interval"]
        sensor_trigger["url"] = url

        newpid = os.fork()
        if newpid == 0:
            response = self.nimbits_action.fork_nimbits_events(sensor_trigger)
        else:
            pids = (os.getpid(), newpid)
            print("parent: %d, child: %d\n" % pids)

        logger.info("Trigger_sensor_events Ended")

    def post_sensor_events(self, cust_pk):
        device_id_dict = fill_dds_request.device_id_dict
        posturl = self.posturl + device_id_dict[cust_pk]["TamperDetector"]["id"] \
                            + "/series"


        logger.info("Nimbits Tamper Post URL = %s", posturl)

        data = "[{\"d\":1.0}]"

        response = self.nimbits_action.post_nimbits_events(posturl, cust_pk, data)