import json
import urllib2
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.client.client import ClientParameters
from homemonitoring.setup.ssh_apis import Login

class ClientRestURL():
    def __init__(self, jsonconfig, node = "cert"):
        self.jsonconfig = jsonconfig
        self.myx_id = jsonconfig["client_conf"]["Myxid"]
        self.resturl = jsonconfig["debug_url"]
        self.node = node

    def load_client_debugconfig(self, cli_obj):
        """
            Description : Accessing the debug URL and getting the latest Telo & OR info
            http://dtool.cn.ooma.com:8080/fsTeloWebControl/v1/myx_001861223A7A/status
            {
                "online": true,
                "sw_version": "179239",
                "device_type": "boyle",
                "usb_bluetooth": false,
                "usb_wireless": false,
                "openremote_status": "running",
                "openremote_version": "179812"
            }
        """
        if self.node == "cert":
            client_rest_url = self.resturl + self.myx_id + "/status"
            my_response = urllib2.urlopen(client_rest_url)
            json_response = json.load(my_response)
            #Appending the json response dictionary with controller info
            cli_obj.controller_info.update(json_response)
            return cli_obj