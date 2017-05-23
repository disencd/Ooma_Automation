import MySQLdb
from homemonitoring.setup.json_parse import JsonConfig


class HMSSqlQuery():
    def __init__(self, node = "cert"):
        self.node = node
        self.json_obj = JsonConfig()
        self.json_server_obj = self.json_obj.dump_config("../server_config.json")
        self.sql_server_dict = self.json_server_obj[self.node]["hms-db"]
        self._db = ""

    def sql_connect(self):
        #print self.sql_server_dict
        self._db = MySQLdb.connect(host=self.json_server_obj[self.node]["hms-db"]["hostname"],  # your host, usually localhost
                             user=self.json_server_obj[self.node]["hms-db"]["username"],  # your username
                             db=self.json_server_obj[self.node]["hms-db"]["db"])  # name of the data base

        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = self._db.cursor()
        return cur

    def sql_disconnect(self):
        self._db.close()

    #Hack for accessing sql DB
    def sql_query(self, or_id = "1263"):

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
            print row

        cur.execute(_nimbits_query)

        for row in cur.fetchall():
            print row
            or_dict['or_id'] = row[0]
            or_dict['nimbits_id'] = row[1]
            or_dict['nimbits_pwd'] = row[2]

        self.sql_disconnect()
        print or_dict
        return or_dict

# if __name__ == "__main__":
#     sql = HMSSqlQuery()
#     sql.sql_query()
