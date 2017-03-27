import json
import sys
import paramiko
import time
import logging
import subprocess
import threading
import re
import os

class JsonConfig():
    #Reading the config file from Json File
    def dump_config(self, filename):
        with open(filename) as json_data_file:
            data = json.load(json_data_file)
            return data

class Login():
    def __init__(self, JsonConfig):
        self.username = JsonConfig["login_cred"]["username"]
        self.password = JsonConfig["login_cred"]["password"]
        self.myx_id = JsonConfig["client_conf"]["myxid"]
        self.showmyx_dict = {}

    def ssh_to_server(self, host):
        """
        Description : Paramiko client is used for SSH in python
        """
        user = self.username
        passwd = self.password

        # logging.info("Auto_Logger: Ssh to server via admin")
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, timeout=20, username=user, password=passwd)
            logging.info("Auto_Logger: Ssh to server %s " % host)
            return ssh

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.error("Auto_Logger: Unable to SSH to server %s(user=%s,pwd=%s). Exception : %s %s %s %s" % (
                            host, user, passwd, e, exc_type, fname, str(exc_tb.tb_lineno)))
            sys.exit(1)

    def get_showmyx_output(self,shell):
        """
            Description : Get Showmyx output of the Telo and capture it in dictionary
        """
        cmd = 'showmyx ' + self.myx_id
        logging.info('Auto_Logger: get showmyx output - %s' % cmd)
        wait_period = 600  # wait period(in secs) for telo to reboot
        while wait_period > 0:
            shell.send(cmd + "\n")
            time.sleep(5)
            op = ''
            while shell.recv_ready():  # read buffer only if data is available
                op += shell.recv(9999)
                if "not registered" in op:
                    logging.warning("The device is not provisioned/resgistered with the provserver server")
                    return "Not registered"
                elif "." in op:
                    # logging.info(op)
                    for lines in op.splitlines():
                        opt = re.search(r'.+[=].+', lines)
                        if opt:
                            #Splitting only the first =, else if multiple = , will cause complexities
                            str = lines.split('=', 1)
                            self.showmyx_dict[str[0]] = str[1]

                    return self.showmyx_dict
                else:
                    pass
                wait_period -= 5
                shell.send('\x03')
                logging.info("Auto Logger: Retrying fetching VPN IP...")
            return None


