import urllib2
import json, base64

class HMSActions(object):
    def __init__(self, jsonconfig, node="cert"):
        self.node = node
        self._jsonconfig = jsonconfig
        self.__url = None

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
    def vs_request_activate(self, hostname_port, req_url, cust_pk):
        self.__url = "http://{0}/{1}/{2}".format(hostname_port, req_url, cust_pk)
        print self.__url
        return self

    '''
        Adding sensor
            Post : http://hms1-cert1.cn.ooma.com:8083/dds/rest/rpc/devicediscovery/2/0/0/devicediscovery/124
    '''
    def vs_request_add_sensor(self, hostname_port, req_url):
        self.__url = "http://{0}/{1}".format(hostname_port, req_url)
        print self.__url
        return self


    def post(self, headers, data):
        assert self.__url is not None, "Use 'request' method to specify URL"
        assert isinstance(data, dict)\
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


    def get(self, headers, data = None):
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

    def sensor_get(self, or_dict):
        assert self.__url is not None, "Use 'request' method to specify URL"

        # Basic Authentication Algorithm
        b64_str = or_dict['beehive_id'] + ":" + or_dict['beehive_pwd']
        base64string = base64.b64encode(b64_str)
        auth_str = "Basic " + base64string
        print auth_str
        try:
            request = urllib2.Request(self.__url)
            request.add_header('Authorization', auth_str)
            request.add_header('Content-Type', "application/vnd.openremote.device-discovery+json")
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError, e:
            return e.reason


    def delete(self, headers, data):
        assert self.__url is not None, "Use 'request' method to specify URL"
        try:
            request = urllib2.Request(self.__url, data, headers)
            request.get_method = lambda: "DELETE"
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError, e:
            return e.reason

    def patch(self, headers, data):
        assert self.__url is not None, "Use 'request' method to specify URL"
        data = json.dumps(data)
        headers = json.dumps(headers)

        try:
            print "PATCH"
            request = urllib2.Request(self.__url, data)
            request.get_method = lambda: "PATCH"
            request.add_header('Content-Type', 'application/json')
            request.add_header("X-ooma-oToken", "TrustMe")
            request.add_header('Accept', 'application/json')
            print request.headers
            print request.data
            #request.add_data(json.dumps(data))
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError, e:
            return e.reason

