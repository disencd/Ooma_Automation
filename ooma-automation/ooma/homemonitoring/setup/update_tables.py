import MySQLdb
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.setup.mongodb_setup import MongoDBQuery
from homemonitoring.virtual_sensor.hms_sql_query import HMSSqlQuery

class UpdateTables():
    def __init__(self):
        pass

    def update_credentials(self):
        _mong_obj = MongoDBQuery()
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

table_obj = UpdateTables()
#table_obj.update_sensorcount()
table_obj.update_credentials()


