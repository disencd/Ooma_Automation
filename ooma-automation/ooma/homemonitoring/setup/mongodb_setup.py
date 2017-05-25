import sys, os
import pymongo
from homemonitoring.setup.json_parse import JsonConfig

class MongoDBQuery():
    def __init__(self):
        self.json_obj = JsonConfig()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        server_f_path =  abs_path + "/../database_config.json"
        self.json_server_obj = self.json_obj.dump_config(server_f_path)
        self.mongo_url = self.json_server_obj["url"]
        self.mongo_coll = self.json_server_obj["acc_collection"]

    def mongo_connect(self):
        self.client = pymongo.MongoClient(self.mongo_url)
        m_db = self.client.get_default_database()
        self.vs_account = m_db[self.mongo_coll]

    def mongo_disconnect(self):
        self.client.close()

    def mongo_addition(self, dict):
        print dict
        self.vs_account.insert_one(dict)

    def mongo_find(self, or_id):
        return self.vs_account.find_one({"_id": or_id})

    def mongo_count(self):
        return self.vs_account.count()

    def mongo_update(self, or_id, dict):
        search_query = {"_id": or_id}
        return self.vs_account.update(search_query, dict)

# m = MongoDBQuery()
# m.mongo_connect()
# dict = {"_id" : "1234", "cust_pk" : "virtualaccount20170524165308252333"}
# m.mongo_addition(dict)
# m.mongo_count()