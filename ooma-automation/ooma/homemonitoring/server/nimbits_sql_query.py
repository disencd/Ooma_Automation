import MySQLdb
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.setup.mongodb_setup import MongoDBQuery
import logging
import colorlog
import time
import sys, os
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.ERROR)
logger = logging.getLogger(__name__)

class NimbitsSqlQuery():

    def __init__(self, node = "cert"):
        self.node = node
        self.json_obj = JsonConfig()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        server_f_path = abs_path + "/../server_config.json"
        self.json_server_obj = self.json_obj.dump_config(server_f_path)
        self.sql_server_dict = self.json_server_obj[self.node]["nimbits-db"]

    def sql_connect(self):
        _host = self.json_server_obj[self.node]["nimbits-db"]["hostname"]
        _username = self.json_server_obj[self.node]["nimbits-db"]["username"]
        _dbname = self.json_server_obj[self.node]["nimbits-db"]["db"]
        #logger.info(" self.sql_server_dict
        self._db = MySQLdb.connect(host=_host,  # your host, usually localhost
                             user=_username,  # your username
                             db=_dbname)  # name of the data base

        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = self._db.cursor()
        return cur

    def sql_disconnect(self):
        self._db.close()

    def sql_query_pk(self, id = "1238c34b-33d7-444f-87d5-5f6acd03e66d"):
        logger.info("id = %s", id)
        or_dict = {}
        cur = self.sql_connect()

        _ooma_userid = "select  * from  VALUESTORE WHERE ENTITYID LIKE '" + str(id) + "'" \
                        " ORDER BY DATA  DESC limit 1;"
        cur.execute(_ooma_userid)


        for _row in cur.fetchall():
            logger.info(" ===========> %s", _row[2])

        self.sql_disconnect()
        time.sleep(1)

        return or_dict


# if __name__ == "__main__":
#     sql = NimbitsSqlQuery()
#     sql.sql_query_pk()
