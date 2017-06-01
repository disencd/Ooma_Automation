from homemonitoring.setup.json_parse import JsonConfig
import os, json
from hms_actions import HMSActions

class Register_sensor():
    def __init__(self, node = "cert"):
        self.json_obj = JsonConfig()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        server_f_path =  abs_path + "/../server_config.json"
        self.json_server_obj = self.json_obj.dump_config(server_f_path)
        self.json_server = self.json_server_obj[self.node]["hms-server"]

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
    def register_motion_sensor(self):
        self.get_sensor_register()
        self.post_sensor_register()

    def register_water_sensor(self):
        self.get_sensor_register()
        self.post_sensor_register()

    def register_door_sensor(self):
        self.get_sensor_register()
        self.post_sensor_register()

    def get_sensor_register(self):
        pass

    def post_sensor_register(self):
        pass

    def update_sensor_message(self):
        pass
