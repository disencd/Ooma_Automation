import json
import sys
import paramiko
import time
import logging
import subprocess
import threading
import re
from homemonitoring.setup.config_app import Login

class ClientParameters():
    def __init__(self, JsonConfig):
        # Dictionary for storing the controller info
        self.controller_info = {}
        self.myx_id = JsonConfig["client_conf"]["myxid"]
        self.login_obj = Login()
        self.myx_dict = {}
    def get_hms_config(self, shell):
        login_obj = self.login_obj

        if not bool(self.myx_dict):
            self.myx_dict = login_obj.get_showmyx_output(shell)

        #copying the controller info to controller dictionary
        self.controller_info["ENABLED"] = myx_dict["HMS_ENABLED"]
        self.controller_info["USER_ENABLED"] = myx_dict["HMS_USER_ENABLED"]
        self.controller_info["CONTROLLER_ID"] = myx_dict["HMS_CONTROLLER_ID"]
        self.controller_info["NIMBITS_EMAIL"] = myx_dict["HMS_NIMBITS_EMAIL"]
        self.controller_info["NIMBITS_TOKEN"] = myx_dict["HMS_NIMBITS_TOKEN"]
        self.controller_info["NIMBITS_URL"] = myx_dict["HMS_NIMBITS_URL"]
        self.controller_info["BEEHIVE_USER"] = myx_dict["HMS_BEEHIVE_USER"]
        self.controller_info["BEEHIVE_PASSWORD"] = myx_dict["HMS_BEEHIVE_PASSWORD"]
        self.controller_info["BEEHIVE_URL"] = myx_dict["HMS_BEEHIVE_URL"]


    def get_vpn_ip(self, shell):
        login_obj = self.login_obj

        if not bool(self.myx_dict):
            self.myx_dict = login_obj.get_showmyx_output(shell)
