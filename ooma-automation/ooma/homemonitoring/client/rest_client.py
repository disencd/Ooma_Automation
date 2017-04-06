import json
import urllib2
from homemonitoring.setup.json_parse import JsonConfig
from homemonitoring.client.client import ClientParameters
from homemonitoring.setup.ssh_apis import Login

class ClientRestURL():
    def __init__(self, jsonconfig, node):
        self.jsonconfig = jsonconfig
        self.myx_id = jsonconfig["client_conf"]["Myxid"]
        self.resturl = jsonconfig["debug_url"]

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
        client_rest_url = self.resturl + self.myx_id + "/status"
        my_response = urllib2.urlopen(client_rest_url)
        json_response = json.load(my_response)
        cli_obj.controller_info["online"] = json_response["online"]
        cli_obj.controller_info["cli_sw_version"] = json_response["sw_version"]
        cli_obj.controller_info["device_type"] = json_response["device_type"]
        cli_obj.controller_info["or_status"] = json_response["openremote_status"]
        cli_obj.controller_info["openremote_version"] = json_response["openremote_version"]
        return cli_obj