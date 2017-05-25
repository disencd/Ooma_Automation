import urllib2
import time, os, json
from hms_actions import HMSActions
from field_generator import FieldGenerator
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.setup.mongodb_setup import MongoDBQuery

class HMS_Activation(object):
    def __init__(self, node = "cert"):

        self.node = node
        self.json_obj = JsonConfig()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        server_f_path =  abs_path + "/../server_config.json"
        print server_f_path
        print os.getcwd()
        self.json_server_obj = self.json_obj.dump_config(server_f_path)
        self.json_server = self.json_server_obj[self.node]["oss-server"]
        self.headers = {
            'Content-Type': 'application/json',
            "X-ooma-oToken": "TrustMe"
        }
        self.field_gen = FieldGenerator()

    '''
        Creating new account
        POST http://oss1-cert1.cn.ooma.com:8001/ems/v1/hms/account/c3bw6mu485ea3z67tnjcqws7dhuv5wsu
        Headers : {'X-ooma-otoken': 'TrustMe', 'Content-type': 'application/json', 'Accept': 'application/json'}
        {
            "timezone": "America/Los_Angeles",
            "spn": "8583973192"
        }
    '''
    def activate_hms_account(self):

        self.mongodb_dict = {}
        self.cust_pk = self.field_gen.generate_pk()
        self.url = "ems/v1/hms/account"


        self.act_data = {
            'spn': self.field_gen.generate_SPN(),
            'timezone': self.field_gen.generate_timezone()
        }

        #Updating the Data to the mongo DB dict
        self.mongodb_dict["spn"] = self.act_data['spn']
        self.mongodb_dict["cust_pk"] = self.cust_pk

        self.headers = {
            'Content-Type': 'application/json',
            "X-ooma-oToken": "TrustMe"
        }

        response, code = HMSActions(self.json_obj, self.node).vs_request_activate(self.json_server, self.url, self.cust_pk). \
            post(self.headers, self.act_data)

        self.mongodb_dict["activation_status"] = code

        print "Activating the HMS Account - ", self.act_data['spn']
        return self.cust_pk, code

    '''
    GET http://oss1-cert1.cn.ooma.com:8001/ems/v1/hms/account/virtualsensors000000000000000395
    Headers : {'X-ooma-otoken': 'TrustMe', 'Content-type': 'application/json', 'Accept': 'application/json'}
    Result:  ('[{"id":2236,"status":"DISABLED","service":\
        {"timezone":"America/Los_Angeles","spn":"1000000395"},"sensors":[]}]', 200)
    '''
    def get_status_hms_account(self):
        _mong_obj = MongoDBQuery()

        response, code = HMSActions(self.json_obj, self.node).vs_request_activate(self.json_server, self.url, self.cust_pk). \
            get(self.headers, self.act_data)

        mongo_resp = json.loads(response)
        self.mongodb_dict["_id"] = mongo_resp[0]["id"]
        self.mongodb_dict["status"] = mongo_resp[0]["status"]

        if self.mongodb_dict["activation_status"]:
            _mong_obj.mongo_connect()
            _mong_obj.mongo_addition(self.mongodb_dict)
            _mong_obj.mongo_disconnect()

        print "Getting Info of The HMS Account ", response
        return self.mongodb_dict["_id"]
    '''
    PATCH http://oss1-cert1.cn.ooma.com:8001/ems/v1/hms/account/virtualsensors000000000000000395
    Headers : {'X-ooma-otoken': 'TrustMe', 'Content-type': 'application/json', 'Accept': 'application/json'}
    Payload : {"enable": "False"}
    '''
    def deactivate_hms_account(self):

        deac_data = {'enable': "False"}
        self.headers = {'Content-Type': 'application/json'}
        response, code = HMSActions(self.json_obj, self.node).vs_request_activate(self.json_server, self.url, self.cust_pk). \
            patch(self.headers, deac_data)

        print "Deactivating The HMS Account ", response
        return response, code

#     def run(self):
#         cnt = 0
#         while cnt < 1000:
#             self.activate_hms_account()
#
#             time.sleep(3)
#             self.get_status_hms_account()
#
#             time.sleep(3)
#
#             self.deactivate_hms_account()
#             cnt += 1
#
# if __name__ == "__main__":
#     trans = HMS_Activation()
#     trans.run()
#     print trans.custom_timers
