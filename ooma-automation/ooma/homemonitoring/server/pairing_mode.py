from homemonitoring.server.hms import HMS

class PairingMode(object):

    def __init__(self, json_obj, node = "cert"):

        self.url = "api/base/status"
        self.mode = "pairingMode"
        self.json_obj = json_obj
        self.node = node

        #Hardcoded - Change it
        self.cust_pk = "c3bw6mu485ea3z67tnjcqws7dhuv5wsv"

    def get_cust_pk(self):
        #self.cust_pk = "u8bep9zdfqnb52sp3mvnbymbbu9sai2a"
        pass

    def enable(self):
        data = {self.mode: True}
        response = HMS(self.json_obj, self.node).request(self.url, self.cust_pk).post(data)
        print response
        return response

    def disable(self):
        data = {self.mode: False}
        response = HMS(self.json_obj, self.node).request(self.url, self.cust_pk).post(data)
        print response
        return response



