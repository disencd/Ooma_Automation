import urllib2
import time
import logging
import colorlog

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FlaskClientWaterSensor:
    def __init__(self, jsonconfig):
        self.jsonconfig = jsonconfig
        self.__resturl = self.jsonconfig["bb_rest_url"]

    def water_sensor_status(self):
        try:
            __http_response = urllib2.urlopen(self.__resturl)
            logger.info("water_sensor_status -", format(self.__resturl))
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer[code - %s reason %s]" % (e.code, e.read()))
            return e.code

    def water_sensor_paging_enabled(self):
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/on"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("water_sensor_paging_enabling...... - %s",format(_pair_url))
            #return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer[code - %s reason %s]" % (e.code, e.read()))
            return e.code

        time.sleep(2)
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("water_sensor_paging_enabled - %s",format(_pair_url))
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer[code - %s reason %s]" % (e.code, e.read()))
            return e.code

    def water_sensor_pairing_enabled(self):
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/on"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("water_sensor_pairing_enabling ... - %s",format(_pair_url))
            #return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer[code - %s reason %s]" % (e.code, e.read()))
            return e.code

        time.sleep(5)

        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("water_sensor_pairing_enabled - %s",format(_pair_url))
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer[code - %s reason %s]" % (e.code, e.read()))
            return e.code

    def water_sensor_pairing_disabled(self):
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("door_sensor_pairing_enabled - %s", format(_pair_url))
            logger.info('{0}  - {1}', format(_pair_url, __http_response))
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer[code - %s reason %s]" % (e.code, e.read()))
            return e.code

    def water_sensor_tampering_enabled(self):
        try:
            _tamper_url = self.__resturl
            _tamper_url += "/sensor/Water/interface/tamper/switch/on"
            __http_response = urllib2.urlopen(_tamper_url)
            logger.info("water_sensor_tampering_enabled - %s", format(_tamper_url))
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer[code - %s reason %s]" % (e.code, e.read()))
            return e.code

    def water_sensor_tampering_disabled(self):
        try:
            _tamper_url = self.__resturl
            _tamper_url += "/sensor/Water/interface/tamper/switch/off"
            __http_response = urllib2.urlopen(_tamper_url)
            logger.info("water_sensor_tampering_disabled - %s", format(_tamper_url))
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer[code - %s reason %s]" % (e.code, e.read()))
            return e.code

    def water_sensor_detects_water(self):
        try:
            _water_url = self.__resturl
            _water_url += "/sensor/Water/interface/event/switch/on"
            __http_response = urllib2.urlopen(_water_url)
            logger.info("water_sensor_detects_water - %s", format(_water_url))
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer[code - %s reason %s]" % (e.code, e.read()))
            return e.code


    def water_sensor_detects_no_water(self):
        try:
            _water_url = self.__resturl
            _water_url += "/sensor/Water/interface/event/switch/off"
            __http_response = urllib2.urlopen(_water_url)
            logger.info("water_sensor_detects_no_water - %s", format(_water_url))
            return __http_response

        except urllib2.URLError as e:

            logger.error("Error - BBFlaskServer[code - %s reason %s]" % (e.code, e.read()))

            return e.code
