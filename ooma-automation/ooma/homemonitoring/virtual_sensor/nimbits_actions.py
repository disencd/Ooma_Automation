import urllib2
import json, base64

class NimbitsActions():
    def __init__(self, jsonconfig, node="cert"):
        self.node = node
        self._jsonconfig = jsonconfig
        self.__url = None

    def generate_url(self, hostname_port, req_url):
        self.__url = "http://{0}/{1}".format(hostname_port, req_url)
        return self

    def get_nimbits_events(self, headers, data = None):
        assert self.__url is not None, "Use 'request' method to specify URL"
        data = json.dumps(data)
        headers = json.dumps(headers)
        try:
            request = urllib2.Request(self.__url)
            request.add_header('Content-Type', 'application/json')
            request.add_header("X-ooma-oToken", "TrustMe")
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError, e:
            return e.reason

    def post_nimbits_events(self, headers, data):
        assert self.__url is not None, "Use 'request' method to specify URL"
        assert isinstance(data, dict) \
               or isinstance(data, list), "Data should be dictionary or list"
        data = json.dumps(data)
        print data
        try:
            print self.__url
            request = urllib2.Request(self.__url, data, headers)
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            print data, code
            return data, code
        except urllib2.URLError, e:
            return e.reason