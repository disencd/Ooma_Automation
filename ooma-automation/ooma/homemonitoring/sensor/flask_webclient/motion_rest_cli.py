import urllib2
import json

class FlaskClientMotionSensor:
    def __init__(self, jsonconfig):
        self.jsonconfig = jsonconfig
        self.resturl = self.jsonconfig["bb_rest_url"]

    def motion_sensor_status(self):
        _pair_url = self.resturl
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def motion_sensor_pairing_enabled(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Motion/interface/pair/switch/on"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def motion_sensor_pairing_disabled(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Motion/interface/pair/switch/off"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def motion_sensor_tampering_enabled(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Motion/interface/tamper/switch/on"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def motion_sensor_tampering_disabled(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Motion/interface/tamper/switch/off"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def motion_sensor_detects_motion(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Motion/interface/event/switch/on"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def motion_sensor_detects_no_motion(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Motion/interface/event/switch/off"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response