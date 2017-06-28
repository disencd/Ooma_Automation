import MySQLdb, time
import os, logging
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.setup.mongodb_setup import MongoDBQuery
from homemonitoring.virtual_sensor.hms_sql_query import HMSSqlQuery
from homemonitoring.virtual_sensor.generate_sensor_events import Sensor_Action
from homemonitoring.setup.hms_logging import HmsLogging

logger = logging.getLogger(__name__)


class UpdateTables():
    def __init__(self):
        pass

    def update_credentials(self):
        _mong_obj = MongoDBQuery()
        sql = HMSSqlQuery()

        results = _mong_obj.mongo_return_all("acc_collection")
        for val in results:
            print(val["cust_pk"])
            sql.sql_query_pk(val["cust_pk"])

        _mong_obj.mongo_disconnect()

    def update_sensorcount(self):
        _mong_obj = MongoDBQuery()
        results = _mong_obj.mongo_return_all("acc_collection")

        for val in results:
            print(val["_id"])
            _mong_obj.mongo_reset_sensor_count(val["_id"], val["cust_pk"])

    def initialize_data_points(self):

        sens_obj = Sensor_Action()
        # sens_obj.configure_door_Sensor("virtualaccount20170607170804362249", "VirtualDoorSensor3")

        _mong_obj = MongoDBQuery()
        results = _mong_obj.mongo_return_elements("SensorInterface_collection")
        #logger.info("Mongo Returned %s", results)
        for val in results:
            if  "id" in val["Alert"].keys():
                config_dict = {
                    "no_events": 1,
                    "time_interval": 1,
                    "event": "Alert"
                }

                logger.info("Alert %s Sensor of PK %s" % \
                            (val["sensorname"], val["cust_pk"]))

                config_dict.update(val)
                sens_obj.resetting_sensor_datapoints(config_dict)

                time.sleep(2)

            if  "id" in val["Battery Indicator"].keys():
                config_dict = {
                    "no_events": 1,
                    "time_interval": 1,
                    "event": "Battery Indicator"
                }

                logger.info("Battery Indicator %s Sensor of PK %s" % \
                            (val["sensorname"], val["cust_pk"]))

                config_dict.update(val)
                sens_obj.resetting_sensor_datapoints(config_dict)

                time.sleep(2)

            if  "id" in val["RSSI biased +128"].keys():
                config_dict = {
                    "no_events": 1,
                    "time_interval": 1,
                    "event": "RSSI biased +128"
                }

                logger.info("RSSI128 %s Sensor of PK %s" % \
                            (val["sensorname"], val["cust_pk"]))

                config_dict.update(val)
                sens_obj.resetting_sensor_datapoints(config_dict)

                time.sleep(2)

            if  "id" in val["ActiveDevice"].keys():
                config_dict = {
                    "no_events": 1,
                    "time_interval": 1,
                    "event": "ActiveDevice"
                }

                logger.info("ActiveDevice %s Sensor of PK %s" % \
                            (val["sensorname"], val["cust_pk"]))

                config_dict.update(val)
                sens_obj.resetting_sensor_datapoints(config_dict)

                time.sleep(2)


table_obj = UpdateTables()
#table_obj.update_sensorcount()
#table_obj.update_credentials()
table_obj.initialize_data_points()


