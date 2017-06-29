import urllib2
import time
import logging
import colorlog

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/tmp/listener.log')
fh.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

class FlaskClientWaterSensor:
    def __init__(self, jsonconfig):
        self.jsonconfig = jsonconfig
        self.__resturl = self.jsonconfig["bb_rest_url"]

    def water_sensor_status(self):
        try:
            __http_response = urllib2.urlopen(self.__resturl)
            logger.info("water_sensor_status - %s", self.__resturl)
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def water_sensor_paging_enabled(self):
        try:
            logger.info("========> Enabling Water Sensor Paging")
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/on"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("water_sensor_paging_enabling...... - %s",_pair_url)
            #return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

        time.sleep(2)
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("water_sensor_paging_enabled - %s",_pair_url)
            return "is paging"
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def water_sensor_pairing_enabled(self):
        try:
            logger.info("========> Enabling Water Sensor Pairing")
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/on"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("water_sensor_pairing_enabling ... - %s",_pair_url)
            #return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

        time.sleep(5)

        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("water_sensor_pairing_enabled - %s",_pair_url)
            return "successfully configured"
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def water_sensor_pairing_disabled(self):
        try:
            logger.info("========> Enabling Water Sensor Disabling Pairing")
            _pair_url = self.__resturl
            _pair_url += "/sensor/Water/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("door_sensor_pairing_enabled - %s", _pair_url)
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def water_sensor_tampering_disabled(self):
        try:
            logger.info("========> Enabling Water Sensor Armed")
            _tamper_url = self.__resturl
            _tamper_url += "/sensor/Water/interface/tamper/switch/on"
            __http_response = urllib2.urlopen(_tamper_url)
            logger.info("water_sensor_tampering_disabled - %s", _tamper_url)
            return "detects tampering"
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def water_sensor_tampering_enabled(self):
        try:
            logger.info("========> Enabling Water Sensor Tampering ")
            _tamper_url = self.__resturl
            _tamper_url += "/sensor/Water/interface/tamper/switch/off"
            __http_response = urllib2.urlopen(_tamper_url)
            logger.info("water_sensor_tampering_enabled - %s", _tamper_url)
            return "is armed"
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def water_sensor_detects_water(self):
        try:
            logger.info("========> Enabling Water Sensor Detects")
            _water_url = self.__resturl
            _water_url += "/sensor/Water/interface/event/switch/on"
            __http_response = urllib2.urlopen(_water_url)
            logger.info("water_sensor_detects_water - %s", _water_url)
            time.sleep(60)
            return "is wet"
        except urllib2.URLError as e:
            logger.error("BB Error - BBFlaskServer is not running")
            return e.code


    def water_sensor_detects_no_water(self):
        try:
            logger.info("========> Enabling Water Sensor Dry")
            _water_url = self.__resturl
            _water_url += "/sensor/Water/interface/event/switch/off"
            __http_response = urllib2.urlopen(_water_url)
            logger.info("water_sensor_detects_no_water - %s", _water_url)
            time.sleep(60)
            return "is dry"

        except urllib2.URLError as e:

            logger.error("Error - BBFlaskServer is not running")

            return e.code
