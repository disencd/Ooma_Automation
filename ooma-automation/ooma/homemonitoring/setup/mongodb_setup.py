import sys, os
import logging
import pymongo
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.setup.hms_logging import HmsLogging
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/tmp/listener.log')
fh.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


class MongoDBQuery():

    def __init__(self):
        self.json_obj = JsonConfig()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        server_f_path =  abs_path + "/../database_config.json"
        self.json_server_obj = self.json_obj.dump_config(server_f_path)
        #self.mongo_url = self.json_server_obj["url"]

    url = "mongodb://localhost:27017/VirtualAutomation"
    client = pymongo.MongoClient(url)
    @staticmethod
    def __getInstance():
        client = MongoDBQuery.client
        if client is None:
            client = pymongo.MongoClient(url)
        return client

    def __mongo_connect(self, collection_name):

        client = MongoDBQuery.__getInstance()
        self.mongo_coll = self.json_server_obj[collection_name]
        m_db = client.get_default_database()
        self.vs_account = m_db[self.mongo_coll]
        logger.info("Mongo Connection Established with %s", collection_name)
        return self.vs_account

    def __mongo_disconnect(self):
        MongoDBQuery.__getInstance().close()

    def mongo_insertion(self, collection, dict):
        logger.info("cust_pk %s", dict['cust_pk'])
        #dict['cust_pk'] = "virtualaccount20170620164922089987"
        self.__mongo_connect(collection)
        if not self.vs_account.find_one({'cust_pk' : dict['cust_pk']}):
            self.vs_account.insert_one(dict)
            logger.info("Successfully Inserted to mongo DB - %s", dict)

        else:
            logger.info("Already inserted to mongo DB")

    def MongoSensorIfaceAdd(self, collection, dict):
        self.__mongo_connect(collection)
        logger.info("Inserting to MongoSensorIfaceAdd mongo DB - %s", dict)
        self.vs_account.insert_one(dict)

    def mongo_find(self, or_id):
        return self.vs_account.find_one({"_id": or_id})

    def mongo_return_all(self, collection):
        self.__mongo_connect(collection)
        cursor = self.vs_account.find({})
        results = [res for res in cursor]
        cursor.close()
        return results

    def map_or_id_with_custpk(self, custpk):
        cursor = self.vs_account.find({})
        results = [res for res in cursor]
        cursor.close()
        val = None
        for val in results:
            if val["cust_pk"] is custpk:
                break

        return val["_id"]

    '''
        Find the SensorInterface Collections dictionary from PK and
        Sensor Name
    '''

    def mongo_find_one_dictionary(self, collection, cust_pk, sensor_name):
        self.__mongo_connect(collection)
        cursor = self.vs_account.find({'cust_pk':cust_pk})
        results = [res for res in cursor]
        cursor.close()
        val = None
        for val in results:
            #logger.info("val['cust_pk'] %s cust_pk is %s" %(val['cust_pk'], cust_pk))
            if val['sensorname'] in sensor_name:
                logger.info("cust_pk is %s", cust_pk)
                break

        logger.info("Interface Dictionary is %s", val)
        return val

    def mongo_find_one_element(self, collection, cust_pk):
        self.__mongo_connect(collection)
        cursor = self.vs_account.find({'cust_pk':cust_pk})
        results = [res for res in cursor]
        cursor.close()
        val = None
        for val in results:
            #logger.info("val['cust_pk'] %s cust_pk is %s" %(val['cust_pk'], cust_pk))
            if str(val['cust_pk']) in str(cust_pk):
                logger.info("cust_pk is %s", cust_pk)
                break

        logger.info("val is %s", val)
        return val

    def mongo_return_elements(self, collection):
        self.__mongo_connect(collection)
        cursor = self.vs_account.find({})
        results = [res for res in cursor]
        cursor.close()
        return results

    def mongo_count(self):
        return self.vs_account.count()

    def mongo_update(self, collection, dict):
        self.__mongo_connect(collection)
        search_query = {'cust_pk' : dict['cust_pk']}
        return self.vs_account.update(search_query, dict)

    #Added seperate function if we dont have this table itself
    def mongo_reset_sensor_count(self, id, cust_pk):
        logger.info("mongo_reset_sensor_count started")
        logger.info("user_dict %s cust_pk %s", id, cust_pk)
        user_dict = {}
        user_dict["_id"] = id
        user_dict["cust_pk"] = cust_pk
        user_dict["total"] = 0
        user_dict["motion"] = 0
        user_dict["door"] = 0
        user_dict["water"] = 0

        self.mongo_insertion("SensorCount_collection", user_dict)



# m = MongoDBQuery()
# m.mongo_connect()
# dict = {"_id" : "1234", "cust_pk" : "virtualaccount20170524165308252333"}
# m.mongo_addition(dict)
# m.mongo_count()