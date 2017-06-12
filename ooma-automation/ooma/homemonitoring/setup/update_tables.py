import MySQLdb
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.setup.mongodb_setup import MongoDBQuery
from homemonitoring.virtual_sensor.hms_sql_query import HMSSqlQuery

class UpdateTables():
    def __init__(self):
        pass

    def update_credentials(self):
        _mong_obj = MongoDBQuery()
        mongo_acc = _mong_obj.mongo_connect("acc_collection")
        sql = HMSSqlQuery()
        cursor = mongo_acc.find({})
        results = [res for res in cursor]
        cursor.close()

        for val in results:
            print(val["cust_pk"])
            sql.sql_query_pk(val["cust_pk"])

        _mong_obj.mongo_disconnect()

    def update_sensorcount(self):
        _mong_obj = MongoDBQuery()
        _mong_obj.mongo_connect("acc_collection")
        cursor = _mong_obj.find({})
        results = [res for res in cursor]
        cursor.close()

        for val in results:
            print(val["_id"])
            _mong_obj.mongo_reset_sensor_count(val["_id"])

# table_obj = UpdateTables()
# table_obj.update_sensorcount()
#table_obj.update_credentials()


