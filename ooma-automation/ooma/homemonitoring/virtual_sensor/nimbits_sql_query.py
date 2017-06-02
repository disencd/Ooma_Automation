import MySQLdb
from homemonitoring.setup.json_parse import JsonConfig
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NimbitsSqlQuery():
    def __init__(self, node = "cert"):
        self.node = node
        self.json_obj = JsonConfig()
        self.json_server_obj = self.json_obj.dump_config("../server_config.json")
        self.sql_server_dict = self.json_server_obj[self.node]["nimbits-db"]
        self._db = ""

    def sql_connect(self):
        #logger.info(" self.sql_server_dict ", self.sql_server_dict)
        self._db = MySQLdb.connect(host=self.json_server_obj[self.node]["nimbits-db"]["hostname"],  # your host, usually localhost
                             user=self.json_server_obj[self.node]["nimbits-db"]["username"],  # your username
                             db=self.json_server_obj[self.node]["nimbits-db"]["db"])  # name of the data base

        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = self._db.cursor()
        return cur

    def sql_disconnect(self):
        self._db.close()

    def sql_query_pk(self, cust_pk = "c3bw6mu485ea3z67tnjcqws7dhuv5wsv"):
        logger.info("cust_pk = ", cust_pk)
        or_dict = {}
        cur = self.sql_connect()


        '''
            mysql> select * from NIMBITS_USER where ID = '1263'
            +------+-----------+--------------------+
            | ID   | PASSWORD  | USERNAME           |
            +------+-----------+--------------------+
            | 1263 | j8bp9ett2 | ekpdbw7ii@ooma.com |
            +------+-----------+--------------------+

            mysql> select * from BEEHIVE_USER where ID = '1263';
            +------+-----------+--------------+--------------+-----------+-----------+
            | ID   | ACCOUNTID | CONTROLLERID | EMAIL        | PASSWORD  | USERNAME  |
            +------+-----------+--------------+--------------+-----------+-----------+
            | 1263 |      1432 |         1414 | hms@ooma.com | zb66zydtq | n9xr8wvju |
            +------+-----------+--------------+--------------+-----------+-----------+
        '''

        _ooma_userid = "select * from OOMA_USER where PK = '" + str(cust_pk) + "';"
        logger.info(" _ooma_userid ",  _ooma_userid)
        cur.execute(_ooma_userid)

        for _row in cur.fetchall():
            or_dict['BEEHIVEUSER_ID_OID'] = _row[2]
            or_dict['NIMBITSUSER_ID_OID'] = _row[3]
            logger.info(" _row ",  _row)

        _beehives_query = "select * from BEEHIVE_USER where ID = '" + str(or_dict['BEEHIVEUSER_ID_OID']) + "';"
        _nimbits_query = "select * from NIMBITS_USER where ID = '" + str(or_dict['NIMBITSUSER_ID_OID']) + "';"

        cur.execute(_beehives_query)

        for _row in cur.fetchall():
            or_dict['beehive_id'] = _row[5]
            or_dict['beehive_pwd'] = _row[4]
            logger.info(" _row ", _row)

        cur.execute(_nimbits_query)

        for _row in cur.fetchall():
            logger.info(" _row ", _row)
            or_dict['or_id'] = _row[0]
            or_dict['nimbits_id'] = _row[1]
            or_dict['nimbits_pwd'] = _row[2]

        self.sql_disconnect()
        logger.info(" or_dict ", or_dict)
        return or_dict


    #Hack for accessing sql DB
    def sql_query(self, or_id = "1263"):
        logger.info(" or_id = ", or_id)
        or_dict = {}
        cur = self.sql_connect()

        '''
            mysql> select * from NIMBITS_USER where ID = '1263'
            +------+-----------+--------------------+
            | ID   | PASSWORD  | USERNAME           |
            +------+-----------+--------------------+
            | 1263 | j8bp9ett2 | ekpdbw7ii@ooma.com |
            +------+-----------+--------------------+

            mysql> select * from BEEHIVE_USER where ID = '1263';
            +------+-----------+--------------+--------------+-----------+-----------+
            | ID   | ACCOUNTID | CONTROLLERID | EMAIL        | PASSWORD  | USERNAME  |
            +------+-----------+--------------+--------------+-----------+-----------+
            | 1263 |      1432 |         1414 | hms@ooma.com | zb66zydtq | n9xr8wvju |
            +------+-----------+--------------+--------------+-----------+-----------+
        '''

        _beehives_query = "select * from BEEHIVE_USER where ID = " + or_id
        _nimbits_query = "select * from NIMBITS_USER where ID = " + or_id

        cur.execute(_beehives_query)

        for row in cur.fetchall():
            or_dict['beehive_id'] = row[5]
            or_dict['beehive_pwd'] = row[4]
            logger.info(" row ", row)

        cur.execute(_nimbits_query)

        for row in cur.fetchall():
            logger.info(" row ", row)
            or_dict['nimbits_id'] = row[1]
            or_dict['nimbits_pwd'] = row[2]

        self.sql_disconnect()
        logger.info("or_dict ",  or_dict)
        return or_dict

if __name__ == "__main__":
    sql = NimbitsSqlQuery()
    sql.sql_query()
