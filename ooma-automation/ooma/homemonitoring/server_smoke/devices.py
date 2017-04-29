from hms import HMS
from utils import get_json


class Device:

    #__GET_NEW_DEVICES__ = "api/devices/new"
    __GET_NEW_DEVICES__ = "api/base/status"
    __REGISTER_DEVICE__ = "api/devices/register"

    def __init__(self):
        self.hms = HMS()
        self.device_id = ""

    def get_new_devices(self):
        resp, code = self.hms.request(self.__GET_NEW_DEVICES__).get()

        if code != 200:
            raise Exception("Cannot det new devices; response code [%s]" % code)


        return get_json(resp)

    def register_device(self, device_id):
        print "REGISTER DEVICE"
        data = {
                  "device": {
                    "id": device_id,
                    "name": "door-14",
                    "type": "DOOR_SENSOR"
                  },
                  "deviceNotification": [
                    {
                      "modeId": 0,
                      "push": "on",
                      "email": "on",
                      "sms": "on",
                      "phone": "on",
                      "base": "on",
                      "conditionRaised": 1
                    }
                  ]
                }


        return self.hms.request(self.__REGISTER_DEVICE__).post(data)
