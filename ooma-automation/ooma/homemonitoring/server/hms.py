import urllib2
import json

class HMS(object):
    def __init__(self, jsonconfig, node="cert"):
        self.node = node
        self._jsonconfig = jsonconfig
        self._hostname_port = jsonconfig[node]["hms-server"]
        self.headers = {'Content-Type': 'application/json'}
        self.__url = None

    def request(self, req_url, cust_pk):
        self.__url = "http://{0}/hms/{1}?username={2}".format(self._hostname_port, req_url, cust_pk)
        print self.__url
        return self

    def post(self, data):
        assert self.__url is not None, "Use 'request' method to specify URL"
        assert isinstance(data, dict)\
                or isinstance(data, list), "Data should be dictionary or list"
        data = json.dumps(data)
        try:
            request = urllib2.Request(self.__url, data, self.headers)
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError, e:
            return e.reason, e.code


    def get(self, data=None):
        assert self.__url is not None, "Use 'request' method to specify URL"

        if data:
            self.__url + data

        try:
            response = urllib2.urlopen(self.__url)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError, e:
            return e.reason, e.code   

    def delete(self):
        assert self.__url is not None, "Use 'request' method to specify URL"
        try:
            request = urllib2.Request(self.__url)
            request.get_method = lambda: "DELETE"
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError, e:
            return e.reason, e.code



