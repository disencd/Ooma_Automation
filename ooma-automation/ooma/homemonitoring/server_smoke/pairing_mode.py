from homemonitoring.server.hms import HMS

class PairingMode(object):
    url = "api/base/status"
    mode = "pairingMode"
    
    def enable(self):
        data = {self.mode: True}
        response = HMS().request(self.url).post(data)
        print response
        return response

    def disable(self):
        data = {self.mode: False}
        response = HMS().request(self.url).post(data)
        print response
        return response
   

