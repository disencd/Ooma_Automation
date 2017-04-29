import urllib2
import json
import utils

class Controller(object):
    CONTROLLER_URL = "hms-proxy-qa.ooma.com:8688/controller/rest"
    __GET_SENSOR_STATUS = "/status?name="
    __GET_DEVICE_LIST = "/devices"
    PAIRING_STATUS_SENSOR = "0000000000-OomaBaseStationRegistration-U1"

    def request(self, url):
        self.url = "http://" + self.CONTROLLER_URL + url
        return self

    def credentials(self, username, password):
        self.basicAuthHeader = utils.get_http_basic_header(username, password);
        return self

    def get(self, data=None):
        assert self.url is not None, "Use 'request' method to specify URL"
        assert self.basicAuthHeader is not None, "Use 'credentials' method to specify credentials"

        if data:
            self.url+data

        try:
            request = urllib2.Request(self.url)
            request.add_header("Authorization", "Basic %s" % self.basicAuthHeader)
            request.add_header("Accept", "application/json")
            print "Sending GET request to " + self.url
            response = urllib2.urlopen(request)

            data = response.read()
            code = response.getcode()
            response.close()
            return data, code
        except urllib2.URLError, e:
            return e.reason, e.code



    def get_devices_list(self, username, password):
        resp, code = self.request(self.__GET_DEVICE_LIST).credentials(username, password).get()
        return resp

    def get_devices_information(self, username, password, device_name):
        resp, code = self.request("%s/%s"%(self.__GET_DEVICE_LIST, device_name)).credentials(username, password).get()
        return resp

    def get_sensor_status(self, username, password, sensor_name):
        resp, code = self.request("%s%s"%(self.__GET_SENSOR_STATUS, sensor_name)).credentials(username, password).get()
        return utils.get_json(resp)[0]["value"]
