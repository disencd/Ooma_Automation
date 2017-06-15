from homemonitoring.setup.json_parse import JsonConfig
import os, json
from hms_actions import HMSActions
import fill_dds_request
import time
import logging
import colorlog

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)
'''
    1.       Get new devices list:
>>> request
GET /hms/api/base/status?username=virtualaccount20170530154419399235 HTTP/1.1
Host: hms1-cert1.cn.ooma.com:8084
Content-Type: application/json
Cache-Control: no-cache
Postman-Token: b001a484-a090-66d7-b3b7-fa4a9460df41
>>> response
{
  "pairingMode": false,
  "notificationPause": false,
  "controllerConnection": false,
  "controllerConfigureMode": true,
  "controllerConfigurationStatus": -1,
  "newDevices": [
    {
      "id": 4101,
      "name": "4441018989",
      "beehiveName": "4441018989",
      "type": "MAGNET_CONTACT",
      "model": "Window Sensor",
      "vendor": null,
      "status": {
        "state": -1,
        "batteryStatus": -1,
        "connectionStatus": 1,
        "tamperStatus": null
      }
    }
  ]
}


2.       Register device:
POST /hms/hms/api/devices/register?username=virtualaccount20170530154419399235 HTTP/1.1
Host: hms1-cert1.cn.ooma.com:8084
Content-Type: application/json
Cache-Control: no-cache
Postman-Token: d06ff2a0-06d4-467e-ca76-cfb787ad2204

{
  "device": {
    "id": 4101,
    "name": "Your device name",
    "type": "MAGNET_CONTACT"
  },
  "deviceNotification": [
    {
      "modeId": 0,
      "push": "on",
      "telo": "off",
      "phone": "off",
      "email": "off",
      "sms": "off",
      "conditionRaised": 0,        <-- 0 means notify about alert state immediately
      "conditionCeased": 0
    }
  ]
}
'''
class Register_sensor():
    def __init__(self, sensorname, node = "cert"):
        self.node = node
        self.json_obj = JsonConfig()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        self.sensorname = sensorname
        server_f_path =  abs_path + "/../server_config.json"
        self.json_server_obj = self.json_obj.dump_config(server_f_path)
        self.json_server = self.json_server_obj[self.node]["hms-server"]
        self.geturl = "hms/api/base/status?username="
        self.posturl = "hms/api/devices/register?username="

        #json file for the Sensor Registration
        reg_config_path = abs_path + "/register_config.json"
        self.reg_config_obj = self.json_obj.dump_config(reg_config_path)
        self.reg_header = self.reg_config_obj["post-register-door"]

        self.hms_action = HMSActions(self.json_obj, self.node)


    def register_motion_sensor(self, cust_pk):
        logger.debug("register_motion_sensor started")
        time.sleep(2)
        response = self.get_sensor_register(cust_pk)

        response = self.update_motion_sensor_message(cust_pk, response)

        code = self.post_sensor_register(cust_pk, response)
        logger.info("Code - ", code)
        assert code is not "200", "Sensor Registration Failed"

        response = self.get_sensor_register(cust_pk)
        logger.info("Get response - ", response)
        logger.debug("register_motion_sensor Ended")

    def register_water_sensor(self, cust_pk):
        logger.debug("register_water_sensor started")
        time.sleep(2)
        repsonse = self.get_sensor_register(cust_pk)
        logger.info("response %s", response)

        response = self.update_water_sensor_message(cust_pk, response)
        code = self.post_sensor_register(cust_pk, response)
        logger.info("Code - ", code)
        assert code is not "200", "Sensor Registration Failed"

        response = self.get_sensor_register(cust_pk)
        logger.info("Get response - ", response)
        logger.debug("register_water_sensor Ended")

    def register_door_sensor(self, cust_pk):
        logger.debug("register_door_sensor started")
        time.sleep(2)
        response = self.get_sensor_register(cust_pk)
        logger.info("response %s", response)

        response = self.update_door_sensor_message(cust_pk, response)
        code = self.post_sensor_register(cust_pk, response)
        logger.info("Code - %s", code)
        assert code is not "200", "Sensor Registration Failed"

        response = self.get_sensor_register(cust_pk)
        logger.info("Get response - ", response)
        logger.debug("register_door_sensor Ended")

    def get_sensor_register(self, cust_pk):

        logger.info(" self.json_server - %s", self.json_server)
        url = "http://{0}/{1}{2}".format(self.json_server, \
                                        self.geturl, cust_pk)

        logger.info("url %s", url)

        response = self.hms_action.get_register_sensor(url)
        _cnt = 0
        while(_cnt < 3):
            _cnt +=1
            if not response["newDevices"]:
                time.sleep(3)
                response = self.hms_action.get_register_sensor(url)
            else:
                break

        return response

    def post_sensor_register(self, cust_pk, response):
        logger.info("self.json_server - %s", self.json_server)
        url = "http://{0}/{1}{2}".format(self.json_server, \
                                        self.posturl, cust_pk)

        logger.info("url %s, response %s" % (url, response))
        response = self.hms_action.post_register_sensor(url, response)

    def update_motion_sensor_message(self, cust_pk, response):
        sensor_post = self.reg_header.copy()
        device_id_dict = fill_dds_request.device_id_dict
        sensor_dict = device_id_dict[cust_pk][self.sensorname]

        logger.info("Updating the Motion Sensor Message")
        #urllib2 is unable to access the list in GET message
        if response["newDevices"]:

            for index in range(len(response["newDevices"])):
                if response["newDevices"][index]["name"] in sensor_dict["Announcement"]["deviceidentifier"]:
                    sensor_post["device"]["id"] = response["newDevices"][index]["id"]
                    sensor_post["device"]["type"] = response["newDevices"][index]["type"]
                    sensor_post["device"]["name"] = self.sensorname
                    logger.info("id - %s, type - %s, name %s" % (sensor_post["device"]["id"], \
                                                             sensor_post["device"]["type"],\
                                                             sensor_post["device"]["name"]))
        else:
            sensor_post["device"]["id"] = "4323"
            sensor_post["device"]["type"] = "MOTION_DETECTOR"
            sensor_post["device"]["name"] = self.sensorname
            logger.info("id - %s, type - %s, name %s" % (sensor_post["device"]["id"], \
                                                         sensor_post["device"]["type"],\
                                                         sensor_post["device"]["name"]))

        return sensor_post

    def update_water_sensor_message(self, cust_pk, response):
        sensor_post = self.reg_header.copy()
        device_id_dict = fill_dds_request.device_id_dict
        sensor_dict = device_id_dict[cust_pk][self.sensorname]
        logger.info("Updating the Water Sensor Message")
        # urllib2 is unable to access the list in GET message
        if response["newDevices"]:

            for index in range(len(response["newDevices"])):
                if response["newDevices"][index]["name"] in sensor_dict["Announcement"]["deviceidentifier"]:
                    sensor_post["device"]["id"] = response["newDevices"][index]["id"]
                    sensor_post["device"]["type"] = response["newDevices"][index]["type"]
                    sensor_post["device"]["name"] = self.sensorname
                    logger.info("id - %s, type - %s, name %s" % (sensor_post["device"]["id"], \
                                                             sensor_post["device"]["type"],\
                                                             sensor_post["device"]["name"]))
        else:
            sensor_post["device"]["id"] = "4323"
            sensor_post["device"]["type"] = "WATER_SENSOR"
            sensor_post["device"]["name"] = "Disen Water Sensor"

        return sensor_post

    def update_door_sensor_message(self, cust_pk, response):
        sensor_post = self.reg_header.copy()
        device_id_dict = fill_dds_request.device_id_dict
        sensor_dict = device_id_dict[cust_pk][self.sensorname]
        logger.info("sensor_post - %s", device_id_dict)
        logger.info("Updating the Door Sensor Message")
        # urllib2 is unable to access the list in GET message
        if response["newDevices"]:
            #logger.info("List - %s", response["newDevices"])
            for index in range(len(response["newDevices"])):
                logger.info("name = %s device id %s" % (response["newDevices"][index]["name"], sensor_dict["Announcement"]["deviceidentifier"]))
                if response["newDevices"][index]["name"] in sensor_dict["Announcement"]["deviceidentifier"]:
                    sensor_post["device"]["id"] = response["newDevices"][index]["id"]
                    sensor_post["device"]["type"] = response["newDevices"][index]["type"]
                    sensor_post["device"]["name"] = self.sensorname
                    logger.info("id - %s, type - %s, name %s" % (sensor_post["device"]["id"], \
                                                             sensor_post["device"]["type"],\
                                                             sensor_post["device"]["name"]))
        else:
            sensor_post["device"]["id"] = "4323"
            sensor_post["device"]["type"] = "DOOR_SENSOR"
            sensor_post["device"]["name"] = "Disen Door Sensor"

        return sensor_post