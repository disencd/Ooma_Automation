import MySQLdb
from homemonitoring.setup.json_parse import JsonConfig


class HMSSqlQuery():
    def __init__(self, node = "cert"):
        self.node = node
        self.json_obj = JsonConfig()
        self.json_server_obj = self.json_obj.dump_config("../../server_config.json")
        self.sql_server_dict = self.json_server_obj[self.node]["hms-db"]
        self._db = ""

    def sql_connect(self):
        self._db = MySQLdb.connect(host=self.sql_server_dict["hostname"],  # your host, usually localhost
                             user=self.sql_server_dict["username"],  # your username
                             passwd=self.sql_server_dict["password"],  # your password
                             #db=self.sql_server_dict["db"])  # name of the data base
                             db = "performance_schema")  # name of the data base

        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = self._db.cursor()
        return cur

    def sql_disconnect(self):
        self._db.close()

    #Hack for accessing sql DB
    def sql_query(self, or_id = "1263"):

        #cur = self.sql_connect()
        or_dict = {
                    'or_id' : '1263',
                    'beehive_id' : 'fc35xy28p',
                    'beehive_pwd': 'a9k237eqy',
                    'nimbits_id': 'pava77xvj@ooma.com',
                    'nimbits_pwd': 'bivecym5n'
        }

        #cur = self.sql_connect()

        _beehives_query = "select * from BEEHIVE_USER where ID = " + or_id
        _nimbits_query = "select * from NIMBITS_USER where ID = " + or_id

        #cur.execute(_beehives_query)

        # print all the first cell of all the rows
        #for row in cur.fetchall():
        #    print row[0]

        #self.sql_disconnect()
        return or_dict

#if __name__ == "__main__":
#    sql = HMSSqlQuery()
#    sql.sql_query()
