import json

from homemonitoring.server.hms import HMS

DEVICE_ID = None

class SensorStatus(object):
    url = "api/devices"
    status = "status"	
    id = 256
    sensor_names = {}

    def __init__(self):
        data, code = HMS().request(self.url).get()
        assert (code == 200), "Cannot get modes"
        data = json.loads(data)
        self.names = {d['name']: d['id'] for d in data}

    def get(self):
        data, code = HMS().\
                     request("{0}/{1}/{2}".format(self.url, self.id, self.status)).get()
        assert (code == 200), "Cannot get the sensor status"
        data = json.loads(data)
	#print data
        return data

