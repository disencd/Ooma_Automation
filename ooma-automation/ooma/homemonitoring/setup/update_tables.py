import MySQLdb
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.setup.mongodb_setup import MongoDBQuery

class UpdateTables():
    def __init__(self):
        pass

    def update_credentials(self):
        _mong_obj = MongoDBQuery()
        mongo_acc = _mong_obj.mongo_connect("acc_collection")

        cursor = mongo_acc.find({})
        results = [res for res in cursor]
        cursor.close()

        for val in results:
            print("%s", val)

        _mong_obj.mongo_disconnect()

table_obj = UpdateTables()
table_obj.update_credentials()


