import urllib2
import json

class FlaskClientFloodSensor:
    def __init__(self, jsonconfig):
        self.jsonconfig = jsonconfig
        self.resturl = self.jsonconfig["bb_rest_url"]

    def flood_sensor_status(self):
        _pair_url = self.resturl
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def water_sensor_pairing_enabled(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Water/interface/pair/switch/on"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def water_sensor_pairing_disabled(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Water/interface/pair/switch/off"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def water_sensor_tampering_enabled(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Water/interface/tamper/switch/on"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def water_sensor_tampering_disabled(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Water/interface/tamper/switch/off"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def water_sensor_detects_water(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Water/interface/event/switch/on"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response

    def water_sensor_detects_no_water(self):
        _pair_url = self.resturl
        _pair_url += "/sensor/Water/interface/event/switch/off"
        my_response = urllib2.urlopen(_pair_url)
        print my_response
        return my_response