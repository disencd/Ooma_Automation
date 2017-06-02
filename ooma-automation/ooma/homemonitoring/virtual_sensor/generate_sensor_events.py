import logging
from virtual_sensor.hms_sql_query import HMSSqlQuery
from homemonitoring.setup.json_parse import JsonConfig

from homemonitoring.virtual_sensor.nimbits_actions import NimbitsActions
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Sensor_Action(object):
    def __init__(self, node = "cert"):
        self.nimbits_action = NimbitsActions()

    def configure_door_Sensor(self, cust_pk):
        self.get_sensor_nimbits_request(cust_pk, "door")


    def get_sensor_nimbits_request(self, cust_pk, name):
        logger.info("get_sensor_nimbitsid started")
        response = self.nimbits_action.get_nimbits_events(cust_pk)
        logger.info("get_sensor_nimbitsid ended")

    def post_sensor_events(self):
        pass