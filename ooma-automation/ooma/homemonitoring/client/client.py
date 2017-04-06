import logging
import re
import time

from homemonitoring.setup.ssh_apis import Login


class ClientParameters():
    def __init__(self, jsonconfig, node):
        # Dictionary for storing the controller info
        self.controller_info = {}
        self.jsonconfig = jsonconfig
        self.myx_id = jsonconfig["client_conf"]["myxid"]
        self.login_obj = Login(self.jsonconfig)
        self.showmyx_dict = {}
        self.node = node

    def is_telo_online(self):
        node = self.node
        ssh = self.login_obj.ssh_to_server(self.jsonconfig[self.node]["prv-server"])
        shell = ssh.invoke_shell()
        cmd = 'showmyx ' + self.myx_id + ' | grep IPADDR='
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
                    ssh.close()
                    return "Not registered"
                elif "." in op:
                    # logging.info(op)
                    self.showmyx_dict["IP"] = re.search("\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}", op).group()
                    ssh.close()
                    return re.search("\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}", op).group()
                else:
                    pass
                wait_period -= 5
                shell.send('\x03')
                logging.info("Auto Logger: Retrying fetching VPN IP...")

            ssh.close()
            return None

    def get_showmyx_output(self, node):
        """
            Description : Get Showmyx output of the Telo and capture it in dictionary
        """
        ssh = self.login_obj.ssh_to_server(self.jsonconfig[node]["prv-server"])
        shell = ssh.invoke_shell()
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
                    ssh.close()
                    return "Not registered"
                elif "." in op:
                    # logging.info(op)
                    for lines in op.splitlines():
                        opt = re.search(r'.+[=].+', lines)
                        if opt:
                            #Splitting only the first =, else if multiple = , will cause complexities
                            str = lines.split('=', 1)
                            self.showmyx_dict[str[0]] = str[1]

                    ssh.close()
                    return None
                else:
                    pass
                wait_period -= 5
                shell.send('\x03')
                logging.info("Auto Logger: Retrying fetching VPN IP...")
            ssh.close()
            return None

    def get_hms_config(self):
        login_obj = self.login_obj

        self.get_showmyx_output(self.node)

        #copying the controller info to controller dictionary
        self.controller_info["ENABLED"] = self.showmyx_dict["HMS_ENABLED"]
        self.controller_info["USER_ENABLED"] = self.showmyx_dict["HMS_USER_ENABLED"]
        self.controller_info["CONTROLLER_ID"] = self.showmyx_dict["HMS_CONTROLLER_ID"]
        self.controller_info["NIMBITS_EMAIL"] = self.showmyx_dict["HMS_NIMBITS_EMAIL"]
        self.controller_info["NIMBITS_TOKEN"] = self.showmyx_dict["HMS_NIMBITS_TOKEN"]
        self.controller_info["NIMBITS_URL"] = self.showmyx_dict["HMS_NIMBITS_URL"]
        self.controller_info["BEEHIVE_USER"] = self.showmyx_dict["HMS_BEEHIVE_USER"]
        self.controller_info["BEEHIVE_PASSWORD"] = self.showmyx_dict["HMS_BEEHIVE_PASSWORD"]
        self.controller_info["BEEHIVE_URL"] = self.showmyx_dict["HMS_BEEHIVE_URL"]
        self.controller_info["IP"] = self.showmyx_dict["IP"]
        return self.controller_info

    def is_openremote_running(self):
        self.login_obj.login_to_DUT_console(self.controller_info["IP"])
        self.login_obj.execute_command_on_DUT_console("pgrep siege")
