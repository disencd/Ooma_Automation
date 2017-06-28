import urllib2
import json
import time
import logging
import colorlog

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.ERROR)
logger = logging.getLogger(__name__)

class FlaskClientDoorSensor:
    def __init__(self, jsonconfig):
        self.jsonconfig = jsonconfig
        self.__resturl = self.jsonconfig["bb_rest_url"]

    def door_sensor_status(self):
        try:
            __http_response = urllib2.urlopen(self.__resturl)
            logger.info("door_sensor_status - %s", self.__resturl)
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def door_sensor_paging_enabled(self):
        try:
            logger.info("========> Enabling Door Sensor Paging")
            _pair_url = self.__resturl
            _pair_url += "/sensor/Door/interface/pair/switch/on"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("door_sensor_paging_enabling...... - %s", _pair_url)
            #return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

        time.sleep(2)
        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Door/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("door_sensor_paging_enabled - %s",_pair_url)
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def door_sensor_pairing_enabled(self):
        try:
            logger.info("========> Enabling Door Sensor Pairing")
            _pair_url = self.__resturl
            _pair_url += "/sensor/Door/interface/pair/switch/on"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("door_sensor_pairing_enabling...... - %s",_pair_url)
            #return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

        time.sleep(5)

        try:
            _pair_url = self.__resturl
            _pair_url += "/sensor/Door/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("door_sensor_pairing_enabled - %s",_pair_url)
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def door_sensor_pairing_disabled(self):
        try:
            logger.info("========> Enabling Door Sensor Disabling Pairing")
            _pair_url = self.__resturl
            _pair_url += "/sensor/Door/interface/pair/switch/off"
            __http_response = urllib2.urlopen(_pair_url)
            logger.info("door_sensor_pairing_disabled - %s",_pair_url)
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def door_sensor_tampering_enabled(self):
        try:
            logger.info("========> Enabling Door Sensor Tampering")
            _tamper_url = self.__resturl
            _tamper_url += "/sensor/Door/interface/tamper/switch/on"
            __http_response = urllib2.urlopen(_tamper_url)
            logger.info("door_sensor_tampering_enabled - %s",_tamper_url)
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def door_sensor_tampering_disabled(self):
        try:
            logger.info("========> Enabling Door Sensor Armed")
            _tamper_url = self.__resturl
            _tamper_url += "/sensor/Door/interface/tamper/switch/off"
            __http_response = urllib2.urlopen(_tamper_url)
            logger.info("door_sensor_tampering_disabled -%s ",_tamper_url)
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def door_sensor_open(self):
        try:
            logger.info("========> Enabling Door Sensor Open")
            _door_url = self.__resturl
            _door_url += "/sensor/Door/interface/event/switch/off"
            __http_response = urllib2.urlopen(_door_url)
            logger.info("door_sensor_open - %s ",_door_url)
            return __http_response
        except urllib2.URLError as e:
            logger.error("Error - BBFlaskServer is not running")
            return e.code

    def door_sensor_close(self):
        try:
            logger.info("========> Enabling Door Sensor Closed")
            _door_url = self.__resturl
            _door_url += "/sensor/Door/interface/event/switch/on"
            __http_response = urllib2.urlopen(_door_url)
            logger.info("send_door_sensor_close - %s",_door_url)
            return __http_response
        except urllib2.URLError as e:
            logger.info("Error - BBFlaskServer is not running")
            return e.code