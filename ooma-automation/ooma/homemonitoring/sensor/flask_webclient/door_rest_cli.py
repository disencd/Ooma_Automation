import urllib2
import json

class FlaskClientDoorSensor:
    def __init__(self, jsonconfig):
        self.jsonconfig = jsonconfig
        self.resturl = self.jsonconfig["bb_rest_url"]

    def door_sensor_status(self):
        _pair_url = self.resturl
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def door_sensor_pairing_enabled(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Door/interface/pair/switch/on"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def door_sensor_pairing_disabled(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Door/interface/pair/switch/off"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def door_sensor_tampering_enabled(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Door/interface/tamper/switch/on"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def door_sensor_tampering_disabled(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Door/interface/tamper/switch/off"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def door_sensor_open(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Door/interface/event/switch/on"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def send_door_sensor_close(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Door/interface/event/switch/off"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response