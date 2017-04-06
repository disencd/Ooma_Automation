
import sys
import paramiko
import time
import logging
import subprocess
import threading
import re
import os

class Login():
    def __init__(self, JsonConfig):
        self.jsonconfig = JsonConfig
        self.username = JsonConfig["login_cred"]["username"]
        self.password = JsonConfig["login_cred"]["password"]
        self.myx_id = JsonConfig["client_conf"]["myxid"]
        self.node = "cert"
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

    def execute_command_on_DUT_console(self, command):
        """
            Description : execute_command_on_DUT_console
        """
        try:
            logging.info('Auto_Logger: Sending command : %s' % command)
            self.shell.send(command + '\n')
            buff = ''
            while not buff.endswith(' ; '):
                resp = self.shell.recv(9999)
                buff += resp

            return buff
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.error("Auto_Logger: Unable to run command on DUT. Exception : %s %s %s %s" % (
                e, exc_type, fname, str(exc_tb.tb_lineno)))

    def login_to_DUT_console(self, vpnIP):
        """
            Description : ssh to vpn ip of Telo in Any Node
        """

        ssh = self.ssh_to_server(self.jsonconfig[self.node]["prv-server"])
        self.shell = ssh.invoke_shell()

        if vpnIP != None and vpnIP != 'Not registered':
            ssh_command = 'ssh ' + str(vpnIP)
            wait_period = 300  # wait period(in secs) for ssh timeout
            while wait_period > 0:
                logging.info('Auto_Logger: Sending command : %s' % ssh_command)
                self.shell.send(ssh_command + '\n')
                time.sleep(8)
                buff = ''
                while self.shell.recv_ready():  # read buffer only if data is available
                    buff += self.shell.recv(9999)
                    if " ; " in buff:
                        break
                    wait_period -= 5
                    if ")?" in buff:
                        self.shell.send('yes' + '\n')
                        time.sleep(2)
                        break
                    self.shell.send('\x03')
                    logging.info("Auto Logger: Retrying ssh...")

                    if wait_period == 0:
                        logging.error('Auto_Logger: DUT %s not reachable!!' % str(vpnIP))
                        sys.exit(1)
            else:
                if vpnIP == 'Not registered':
                    logging.error('Auto_Logger: Device not registered!')
                else:
                    logging.error('Auto_Logger: DUT not reachable!')
                sys.exit(1)