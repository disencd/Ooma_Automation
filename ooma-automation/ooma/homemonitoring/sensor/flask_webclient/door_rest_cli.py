import urllib2
import json
import time

class FlaskClientDoorSensor:
    def __init__(self, jsonconfig):
        self.jsonconfig = jsonconfig
        self.__resturl = self.jsonconfig["bb_rest_url"]

    def door_sensor_status(self):
        try:
            __http_response = urllib2.urlopen(self.__resturl)
            print ("door_sensor_status -", format(self.__resturl))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason


    def door_sensor_paging_enabled(self):
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Door/interface/pair/switch/on"
            __http_response = urllib2.urlopen(_pair_url)
            print ("door_sensor_paging_enabling...... -",format(_pair_url))
            #return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason
        time.sleep(2)
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Door/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            print ("door_sensor_paging_enabled -",format(_pair_url))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def door_sensor_pairing_enabled(self):
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Door/interface/pair/switch/on"
            __http_response = urllib2.urlopen(_pair_url)
            print ("door_sensor_pairing_enabling...... -",format(_pair_url))
            #return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

        time.sleep(5)

        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Door/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            print ("door_sensor_pairing_enabled -",format(_pair_url))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def door_sensor_pairing_disabled(self):
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Door/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            print ("door_sensor_pairing_disabled -",format(_pair_url))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def door_sensor_tampering_enabled(self):
        try:
            _tamper_url = self.__resturl
            _tamper_url += "/sensor/Door/interface/tamper/switch/on"
            __http_response = urllib2.urlopen(_tamper_url)
            print ("door_sensor_tampering_enabled -",format(_tamper_url))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def door_sensor_tampering_disabled(self):
        try:
            _tamper_url = self.__resturl
            _tamper_url += "/sensor/Door/interface/tamper/switch/off"
            __http_response = urllib2.urlopen(_tamper_url)
            print ("door_sensor_tampering_disabled -",format(_tamper_url))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def door_sensor_open(self):
        try:
            _door_url = self.__resturl
            _door_url += "/sensor/Door/interface/event/switch/off"
            __http_response = urllib2.urlopen(_door_url)
            print ("door_sensor_open -",format(_door_url))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def door_sensor_close(self):
        try:
            _door_url = self.__resturl
            _door_url += "/sensor/Door/interface/event/switch/on"
            __http_response = urllib2.urlopen(_door_url)
            print ("send_door_sensor_close -",format(_door_url))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason