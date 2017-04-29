import urllib2
import json

class HMS(object):
    HMS_URL = "hms1-cert1.cn.ooma.com:8084/hms"
    PK = "9776d3ifxtvx74ejxpsmuxvzq3ijhrmp"
    headers = {'Content-Type' : 'application/json'}
    url = None
    
    def request(self, url):
        self.url = "http://{0}/{1}?username={2}".format(self.HMS_URL, url, self.PK)
        print self.url
        return self

    def post(self, data):
        assert self.url is not None, "Use 'request' method to specify URL"
        assert isinstance(data, dict)\
                or isinstance(data, list), "Data should be dictionary or list"
        data = json.dumps(data)
        try:
            request = urllib2.Request(self.url, data, self.headers)
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError, e:
            return e.reason, e.code


    def get(self, data=None):
        assert self.url is not None, "Use 'request' method to specify URL"

        if data:
            self.url+data

        try:
            response = urllib2.urlopen(self.url)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError, e:
            return e.reason, e.code   

    def delete(self):
        assert self.url is not None, "Use 'request' method to specify URL"
        try:
            request = urllib2.Request(self.url)
            request.get_method = lambda: "DELETE"
            response = urllib2.urlopen(request)
            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError, e:
            return e.reason, e.code



