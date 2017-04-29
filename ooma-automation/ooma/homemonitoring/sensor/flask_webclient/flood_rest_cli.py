import urllib2
import time

class FlaskClientWaterSensor:
    def __init__(self, jsonconfig):
        self.jsonconfig = jsonconfig
        self.__resturl = self.jsonconfig["bb_rest_url"]

    def water_sensor_status(self):
        try:
            __http_response = urllib2.urlopen(self.__resturl)
            print ("water_sensor_status -", format(self.__resturl))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def water_sensor_paging_enabled(self):
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/on"
            __http_response = urllib2.urlopen(_pair_url)
            print ("water_sensor_paging_enabling...... -",format(_pair_url))
            #return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

        time.sleep(2)
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            print ("water_sensor_paging_enabled -",format(_pair_url))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def water_sensor_pairing_enabled(self):
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/on"
            __http_response = urllib2.urlopen(_pair_url)
            print ("water_sensor_pairing_enabling ...... -",format(_pair_url))
            #return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

        time.sleep(5)

        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            print ("water_sensor_pairing_enabled -",format(_pair_url))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def water_sensor_pairing_disabled(self):
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            print ("door_sensor_pairing_enabled -", format(_pair_url))
            print ('{0}  - {1}', format(_pair_url, __http_response))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def water_sensor_tampering_enabled(self):
        try:
            _tamper_url = self.__resturl
            _tamper_url += "/sensor/Water/interface/tamper/switch/on"
            __http_response = urllib2.urlopen(_tamper_url)
            print ("water_sensor_tampering_enabled -", format(_tamper_url))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def water_sensor_tampering_disabled(self):
        try:
            _tamper_url = self.__resturl
            _tamper_url += "/sensor/Water/interface/tamper/switch/off"
            __http_response = urllib2.urlopen(_tamper_url)
            print ("water_sensor_tampering_disabled -", format(_tamper_url))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def water_sensor_detects_water(self):
        try:
            _water_url = self.__resturl
            _water_url += "/sensor/Water/interface/event/switch/on"
            __http_response = urllib2.urlopen(_water_url)
            print ("water_sensor_detects_water -", format(_water_url))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason


    def water_sensor_detects_no_water(self):
        try:
            _water_url = self.__resturl
            _water_url += "/sensor/Water/interface/event/switch/off"
            __http_response = urllib2.urlopen(_water_url)
            print ("water_sensor_detects_no_water -", format(_water_url))
            return __http_response

        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason
