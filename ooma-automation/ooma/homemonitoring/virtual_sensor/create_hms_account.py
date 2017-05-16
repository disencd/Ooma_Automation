import urllib2
import time
from hms_actions import HMSActions
from field_generator import FieldGenerator
from homemonitoring.setup.json_parse import JsonConfig

class Transaction(object):
    def __init__(self, node = "cert"):
        self.custom_timers = {}
        self.json_obj = ""
        self.json_obj = JsonConfig()
        self.json_server_obj = self.json_obj.dump_config("../server_config.json")
        #self.json_server_obj = "hms1-cert1.cn.ooma.com:8084"
        self.node = node
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Basic b3NzOnd5M1lCYWdANw=='
        }
    '''
        Creating new account
        POST http://hms1-cert1.cn.ooma.com:8084/hms/oss/vn5j9av6ru7hjue7fpzek3r73m4ec8mq
        {
            "orUsername":"ui89dg3p4",
            "orPassword":"YmJoajlqaWJi",
            "nimbitsUsername":"sun2pfbjr@ooma.com",
            "nimbitsPassword":"dmdlZmc3OWV2",
            "spn":"9712732945",
            "timezone":"America/Los_Angeles"
        }
    '''
    def run(self):
        start_timer = time.time()

        field_gen = FieldGenerator()
        self.cust_pk = field_gen.generate_pk()


        self.url = "hms/oss"
        data = {
                    'orUsername' : field_gen.generate_orUsername(),
                    'orPassword' : field_gen.generate_orPassword(),
                    'nimbitsUsername' : field_gen.generate_nimbitsUsername(),
                    'nimbitsPassword' : field_gen.generate_nimbitsPassword(),
                    'spn' : field_gen.generate_SPN(),
                    'timezone' : field_gen.generate_timezone()
                }
        print data
        response = HMSActions(self.json_obj, self.node).vs_request_activate(self.json_server_obj, self.url, self.cust_pk).post(data, self.headers)
        print response
        latency = time.time() - start_timer
        self.custom_timers['HMS_Activation_Time'] = latency
        #assert (response.code == 200), 'Bad Response: HTTP %s' % response.code

if __name__ == "__main__":
    trans = Transaction()
    trans.run()
    print trans.custom_timers
