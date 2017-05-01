import urllib2
import time
from hms_actions import HMSActions
from field_generator import FieldGenerator
from setup.json_parse import JsonConfig


class Transaction1(object):
    def __init__(self, node = "cert"):
        self.custom_timers = {}
        self.node = node
        self.json_obj = JsonConfig()
        self.json_server_obj = self.json_obj.dump_config("../../server_config.json")
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
        self.cust_pk = self.field_gen.generate_pk()
        self.url = "ems/v1/hms/account"

        self.act_data = {
            'spn': self.field_gen.generate_SPN(),
            'timezone': self.field_gen.generate_timezone()
        }
        self.headers = {
            'Content-Type': 'application/json',
            "X-ooma-oToken": "TrustMe"
        }
        _start_timer = time.time()
        response = HMSActions(self.json_obj, self.node).vs_request_activate(self.json_server, self.url, self.cust_pk). \
            post(self.headers, self.act_data)

        _latency = time.time() - _start_timer
        self.custom_timers['HMS_Activation_Time'] = _latency
        print "Activating the HMS Account - ", self.act_data['spn']
        return response

    '''
    GET http://oss1-cert1.cn.ooma.com:8001/ems/v1/hms/account/virtualsensors000000000000000395
    Headers : {'X-ooma-otoken': 'TrustMe', 'Content-type': 'application/json', 'Accept': 'application/json'}
    Result:  ('[{"id":2236,"status":"DISABLED","service":\
        {"timezone":"America/Los_Angeles","spn":"1000000395"},"sensors":[]}]', 200)
    '''
    def get_status_hms_account(self):
        _start_timer = time.time()
        response = HMSActions(self.json_obj, self.node).vs_request_activate(self.json_server, self.url, self.cust_pk). \
            get(self.headers, self.act_data)
        _latency = time.time() - _start_timer
        self.custom_timers['HMS_Information_Get'] = _latency
        print "Getting Info of The HMS Account ", response
        return response
    '''
    PATCH http://oss1-cert1.cn.ooma.com:8001/ems/v1/hms/account/virtualsensors000000000000000395
    Headers : {'X-ooma-otoken': 'TrustMe', 'Content-type': 'application/json', 'Accept': 'application/json'}
    Payload : {"enable": "False"}
    '''
    def deactivate_hms_account(self):
        _start_timer = time.time()
        deac_data = {'enable': "False"}
        self.headers = {'Content-Type': 'application/json'}
        response = HMSActions(self.json_obj, self.node).vs_request_activate(self.json_server, self.url, self.cust_pk). \
            patch(self.headers, deac_data)
        _latency = time.time() - _start_timer
        self.custom_timers['HMS_Deactivation_Time'] = _latency
        print "Deactivating The HMS Account ", response
        return response

    def run(self):
        cnt = 0
        while cnt < 1000:
            self.activate_hms_account()

            self.get_status_hms_account()

            self.deactivate_hms_account()
            cnt += 1

if __name__ == "__main__":
    trans = Transaction1()
    trans.run()
    print trans.custom_timers
