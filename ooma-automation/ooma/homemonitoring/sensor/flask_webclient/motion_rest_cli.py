import urllib2
import logging
import colorlog

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.ERROR)
logger = logging.getLogger(__name__)

class FlaskClientMotionSensor:
    def __init__(self, jsonconfig):
        self.jsonconfig = jsonconfig
        self.__resturl = self.jsonconfig["bb_rest_url"]

    def motion_sensor_status(self):
        try:
            __http_response = urllib2.urlopen(self.__resturl)
            print ('{0}  - {1}', format(self.__resturl , __http_response))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def motion_sensor_pairing_enabled(self):
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Motion/interface/pair/switch/on"
            __http_response = urllib2.urlopen(_pair_url)
            print ('{0}  - {1}', format(_pair_url, __http_response))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def motion_sensor_pairing_disabled(self):
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Motion/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            print ('{0}  - {1}', format(_pair_url, __http_response))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def motion_sensor_tampering_enabled(self):
        try:
            _tamper_url = self.__resturl
            _tamper_url += "/sensor/Motion/interface/tamper/switch/on"
            __http_response = urllib2.urlopen(_tamper_url)
            print ('{0}  - {1}', format(_tamper_url, __http_response))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def motion_sensor_tampering_disabled(self):
        try:
            _tamper_url = self.__resturl
            _tamper_url += "/sensor/Motion/interface/tamper/switch/off"
            __http_response = urllib2.urlopen(_tamper_url)
            print ('{0}  - {1}', format(_tamper_url, __http_response))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def motion_sensor_detects_motion(self):
        try:
            _motion_url = self.__resturl
            _motion_url += "/sensor/Motion/interface/event/switch/on"
            __http_response = urllib2.urlopen(_motion_url)
            print ('{0}  - {1}', format(_motion_url, __http_response))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason

    def motion_sensor_detects_no_motion(self):
        try:
            _motion_url = self.__resturl
            _motion_url += "/sensor/Motion/interface/event/switch/off"
            __http_response = urllib2.urlopen(_motion_url)
            print ('{0}  - {1}', format(_motion_url, __http_response))
            return __http_response
        except urllib2.URLError, err:
            print "Error in Beaglebone Flask Server - ", err.reason