import sys, os
import pymongo
from homemonitoring.setup.json_parse import JsonConfig

import logging
import colorlog
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MongoDBQuery():
    def __init__(self):
        self.json_obj = JsonConfig()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        server_f_path =  abs_path + "/../database_config.json"
        self.json_server_obj = self.json_obj.dump_config(server_f_path)
        self.mongo_url = self.json_server_obj["url"]


    def mongo_connect(self, collection_name):
        logger.info("Mongo Connection Established")
        self.client = pymongo.MongoClient(self.mongo_url)
        self.mongo_coll = self.json_server_obj[collection_name]
        m_db = self.client.get_default_database()
        self.vs_account = m_db[self.mongo_coll]
        return self.vs_account

    def mongo_disconnect(self):
        self.client.close()

    def mongo_addition(self, dict):
        logger.info("Inserting to mongo DB - %s", dict)
        self.vs_account.insert_one(dict)

    def mongo_find(self, or_id):
        return self.vs_account.find_one({"_id": or_id})

    def mongo_count(self):
        return self.vs_account.count()

    def mongo_update(self, or_id, dict):
        search_query = {"_id": or_id}
        return self.vs_account.update(search_query, dict)

    #Added seperate function if we dont have this table itself
    def mongo_reset_sensor_count(self, id):
        user_dict = {}
        user_dict["_id"] = id
        user_dict["total"] = 0
        user_dict["motion"] = 0
        user_dict["door"] = 0
        user_dict["water"] = 0

        self.mongo_connect("SensorCount_collection")
        self.mongo_addition(user_dict)
        self.mongo_disconnect()


# m = MongoDBQuery()
# m.mongo_connect()
# dict = {"_id" : "1234", "cust_pk" : "virtualaccount20170524165308252333"}
# m.mongo_addition(dict)
# m.mongo_count()