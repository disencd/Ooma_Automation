import urllib2
import json
import base64


class Sensor:
    SERVER_IP_PORT = "hms1-cert1.cn.ooma.com:8084"
    SERVER_PORT = "8084"
    PATH = "/SensorEmulator"
    __API_NEW_SENSOR = "/rest/sensors"
    __API_UNPAIR_SENSOR = "/rest/sensors/%s"
    __API_NEW_EVENT = "/rest/sensors/%s/event"
    __API_PAIRING_MODE = "/rest/base"

    def __init__(self, sensor_id=None):
        self.url_new_sensor = "http://%s%s%s" % (self.SERVER_IP_PORT, self.PATH, self.__API_NEW_SENSOR)
        self.uri_pairing_mode = "http://%s%s%s" %(self.SERVER_IP_PORT, self.PATH, self.__API_PAIRING_MODE)

        self.sensor_id = sensor_id
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        self.url_unpair_sensor = ""
        self.url_new_event = ""
        self.is_added = 0
        self.mac_address = ""
        self.name = ''

    def set_sensor_id(self, id):
        self.sensor_id = id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        assert (self.name != ''), "Device is still not created, no name value"
        return self.name

    def get_mac_address(self):
        assert (self.mac_address != ""), "No mac address!"
        return self.mac_address

    def set_urls(self, ):
        assert self.sensor_id, "Please set sensor_id or create new one"
        self.url_unpair_sensor = "http://%s%s%s" % (self.SERVER_IP_PORT,
                                                    self.PATH,
                                                    self.__API_UNPAIR_SENSOR % (self.sensor_id,))

        self.url_new_event = "http://%s%s%s" % (self.SERVER_IP_PORT,
                                                self.PATH,
                                                self.__API_NEW_EVENT % (self.sensor_id,))

    def add(self, type, protocol="OOMA_ULE", mac_address=None):

        print "Create new controller"
        data = json.dumps({
                           "protocol": protocol,
                           "type": type})

        print "url: ", self.url_new_sensor
        req = urllib2.Request(self.url_new_sensor, data, self.headers)
        f = urllib2.urlopen(req)
        response = f.read()
        code = f.getcode()

        if code == 200:
            data = json.loads(response)

            self.sensor_id = data["id"]
            self.mac_address = data["macAddress"]
            self.set_name(data["deviceId"] + data["interfaces"]["U1S1I256"]["id"])

            print "Contoller is created. Sensor id [%s], macAddress [%s], device name [%s]" % (self.sensor_id, self.mac_address, self.get_name())
            self.is_added = 1

        f.close()

        return code

    def unpair(self, sensor_id=None):
        if self.is_added == 0 and sensor_id == None:
            print "No need to unpair sensor"
            return 200

        print "Unpair sensor"

        if sensor_id:
            self.sensor_id = sensor_id

        self.set_urls()
        print "URL: ", self.url_unpair_sensor
        req = urllib2.Request(self.url_unpair_sensor)
        req.get_method = lambda: "DELETE"
        f = urllib2.urlopen(req)
        response = f.read()
        code = f.getcode()
        f.close()
        self.is_added = 0
        return code

    def send_event(self, type_, payload):
        self.set_urls()
        data = json.dumps({"type": type_,
                           "payload": payload})
        req = urllib2.Request(self.url_new_event, data, self.headers)
        f = urllib2.urlopen(req)
        response = f.read()
        code = f.getcode()
        f.close()
        return code

    def set_pairing_mode(self):
        print "Set pairing mode TRUE"
        print "URL: ", self.uri_pairing_mode
        data = json.dumps({"pairing":"true"})

        req = urllib2.Request(self.uri_pairing_mode, data, self.headers)
        f = urllib2.urlopen(req)
        response = f.read()
        code = f.getcode()
        if code == 200:
            print "Pairing mode is set"

        f.close()
        return code


class DeviceDiscovery:
    SERVER_IP_PORT = "hms1-cert1.cn.ooma.com:8084"
    SERVER_PORT = "8084"
    PATH = "/dds"
    __API_DEVICE_DISCOVERY = "/rest/rpc/devicediscovery/2/0/0/devicediscovery"

    # Auth credentials:
    USER = "bn88k8b45"
    PASSWD = "nns879r4f"

    def __init__(self, sensor_id=None):
        self.url_device_discovery = "http://%s%s%s" % (self.SERVER_IP_PORT, self.PATH, self.__API_DEVICE_DISCOVERY)
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.data = None

    def device_discovery(self):

        print "Trying to get device info"

        print "URL: ", self.url_device_discovery
        req = urllib2.Request(self.url_device_discovery)
        base64string = base64.encodestring('%s:%s' % (self.USER, self.PASSWD)).replace('\n', '')
        req.add_header("Authorization", "Basic %s" % base64string)
        f = urllib2.urlopen(req)
        response = f.read()
        code = f.getcode()

        if code == 200:
            self.data = json.loads(response)

        #    print "DATA: ", self.data

        f.close()
        return code

    def find_device(self, mac):
        # list of devices
        devices = self.data["model"]["devices"]

        device_info = filter(lambda x: mac in x["deviceIdentifier"], devices)

        return device_info


class Nimbits:
    SERVER_IP_PORT = "hms1-cert1.cn.ooma.com:8084"
    SERVER_PORT = "8084"
    PATH = "/service/v3"
    __API_DEVICE_DISCOVERY = "/rest/me?children=true"


    # Auth credentials:
    USER = "tachi2s86@ooma.com"
    PASSWD = "9c9v5ujau"
    
    def __init__(self, sensor_id=None):
        self.url_device_discovery = "http://%s%s%s" % (self.SERVER_IP_PORT, self.PATH, self.__API_DEVICE_DISCOVERY)
        self.url_alarm_state = ""

        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json',
			            'Authorization': 'Basic tachi2s86@ooma.com:9c9v5ujau'}
        self.data = None
        self.uuid = ""

    def is_run(self):

        print "URL: ", self.url_device_discovery
        req = urllib2.Request(self.url_device_discovery)

        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')
        req.add_header('Authorization', 'Basic tachi2s86@ooma.com:9c9v5ujau')
        f = urllib2.urlopen(req)

        code = f.getcode()

        return code

    def get_uid(self, device_name):

        print "Trying to get device info"

        print "URL: ", self.url_device_discovery
        req = urllib2.Request(self.url_device_discovery)

        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')
        req.add_header('Authorization', 'Basic tachi2s86@ooma.com:9c9v5ujau')
        f = urllib2.urlopen(req)
        response = f.read()
        code = f.getcode()

        if code == 200:
            self.data = json.loads(response)

            children_list = self.data["children"]
            children_data = filter(lambda x: device_name in x["name"], children_list)
            print "CHILDREN DATA: ", children_list
            if children_data:
                self.uuid = children_data[0]["uuid"]
                f.close()
                return self.uuid
            else:
                f.close()
                raise Exception("uuid is not found")

        f.close()
        return 0

    def __get_d_link(self):
        assert self.uuid, "uuid is not set"
        self.url_alarm_state = "http://%s%s/rest/%s/snapshot" % (self.SERVER_IP_PORT, self.PATH, self.uuid)

    def get_alarm_state(self, device_name):


        print "device_name: ", device_name
        self.get_uid(device_name)
        self.__get_d_link()
        print "URL: ", self.url_alarm_state

        req = urllib2.Request(self.url_alarm_state)

        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')
        req.add_header('Authorization', 'Basic tachi2s86@ooma.com:9c9v5ujau')

        f = urllib2.urlopen(req)
        response = f.read()
        code = f.getcode()

        if code == 200:
            self.data = json.loads(response)
            return self.data["snapshot"]["d"]

        f.close()
        return code


class BCS:
    SERVER_IP_PORT = "hms1-cert1.cn.ooma.com:8084"
    SERVER_PORT = "8084"
    PATH = "/bcs"
    __API_DEVICE_DISCOVERY = "/accounts/1259/devices"

    # Auth credentials:
    USER = "bn88k8b45"
    PASSWD = "nns879r4f"
	
    def __init__(self, sensor_id=None):
        self.url_device_discovery = "http://%s%s%s" % (self.SERVER_IP_PORT, self.PATH, self.__API_DEVICE_DISCOVERY)
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.data = None

    def get_devices(self):

        print "URL: ", self.url_device_discovery
        req = urllib2.Request(self.url_device_discovery)
        base64string = base64.encodestring('%s:%s' % (self.USER, self.PASSWD)).replace('\n', '')
        req.add_header("Authorization", "Basic {0}".format(base64string))
        req.add_header("Accept", 'application/json')
        f = urllib2.urlopen(req)
        response = f.read()
        code = f.getcode()

        if code == 200:
            self.data = json.loads(response)

        #    print "DATA: ", self.data

        f.close()
        return code
