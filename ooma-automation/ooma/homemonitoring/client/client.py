import logging
import re
import time
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

from homemonitoring.setup.ssh_apis import Login


class clientException(Exception):
    '''
    Description: Class For handling Exceptions
    '''
    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return self.__msg

class ClientParameters():
    def __init__(self, jsonconfig, node = "cert"):
        # Dictionary for storing the controller info
        self.controller_info = {}
        self.jsonconfig = jsonconfig
        self._myx_id = jsonconfig["client_conf"]["myxid"]
        self.login_obj = Login(self.jsonconfig)
        self._client_dict = {}
        self._node = node

    def is_telo_online(self):
        __ssh = self.login_obj.ssh_to_server(self.jsonconfig[self._node]["prv-server"])
        __shell = __ssh.invoke_shell()
        cmd = 'showmyx ' + self._myx_id + ' | grep IPADDR='
        logging.info('Auto_Logger: get showmyx output - %s' % cmd)
        wait_period = 600  # wait period(in secs) for telo to reboot
        while wait_period > 0:
            __shell.send(cmd + "\n")
            time.sleep(5)
            __op = ''
            while __shell.recv_ready():  # read buffer only if data is available
                __op += __shell.recv(9999)
                if "not registered" in __op:
                    logging.warning("The device is not provisioned/resgistered with the provserver server")
                    __ssh.close()
                    return "Not registered"
                elif "." in __op:

                    __ip_addr_pattern = re.search("\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}", __op)

                    if not __ip_addr_pattern:
                        raise clientException("Telo is OFFLINE... Check Internet Connection")


                    #logging.info(op)
                    self._client_dict["IP"] = __ip_addr_pattern.group()
                    __ssh.close()

                    return re.search("\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}", __op).group()
                else:
                    pass
                wait_period -= 5
                __shell.send('\x03')
                logging.info("Auto Logger: Retrying fetching VPN IP...")

            __ssh.close()
            return None

    def __get_showmyx_output(self, node):
        """
            Description : Get Showmyx output of the Telo and capture it in dictionary
        """
        __ssh = self.login_obj.ssh_to_server(self.jsonconfig[node]["prv-server"])
        __shell = __ssh.invoke_shell()
        __cmd = 'showmyx ' + self._myx_id
        logging.info('Auto_Logger: get showmyx output - %s' % __cmd)
        wait_period = 600  # wait period(in secs) for telo to reboot
        while wait_period > 0:
            __shell.send(__cmd + "\n")
            time.sleep(5)
            __op = ''
            while __shell.recv_ready():  # read buffer only if data is available
                __op += __shell.recv(9999)
                if "not registered" in __op:
                    logging.warning("The device is not provisioned/resgistered with the provserver server")
                    __ssh.close()
                    return "Not registered"
                elif "." in __op:

                    if not __op:
                        raise clientException("Telo is OFFLINE... Check Internet Connection")

                    # logging.info(op)
                    for __lines in __op.splitlines():
                        __opt = re.search(r'.+[=].+', __lines)
                        if __opt:
                            #Splitting only the first =, else if multiple = , will cause complexities
                            str = __lines.split('=', 1)
                            self._client_dict[str[0]] = str[1]

                    __ssh.close()
                    return None
                else:
                    pass
                wait_period -= 5
                __shell.send('\x03')
                logging.info("Auto Logger: Retrying fetching VPN IP...")
            __ssh.close()
            return None

    def get_hms_config(self):
        '''
        :Description: Extracting the HMS Specefic information to Controller Dict
        :return: Controller Dictionary with HMS Specefic Credentials
        '''

        #Running the showmyx <myxid> command and store in client Dictionary
        self.__get_showmyx_output(self._node)

        #copying the controller info to controller dictionary
        self.controller_info["ENABLED"] = self._client_dict["HMS_ENABLED"]
        self.controller_info["USER_ENABLED"] = self._client_dict["HMS_USER_ENABLED"]
        self.controller_info["CONTROLLER_ID"] = self._client_dict["HMS_CONTROLLER_ID"]
        self.controller_info["NIMBITS_EMAIL"] = self._client_dict["HMS_NIMBITS_EMAIL"]
        self.controller_info["NIMBITS_TOKEN"] = self._client_dict["HMS_NIMBITS_TOKEN"]
        self.controller_info["NIMBITS_URL"] = self._client_dict["HMS_NIMBITS_URL"]
        self.controller_info["BEEHIVE_USER"] = self._client_dict["HMS_BEEHIVE_USER"]
        self.controller_info["BEEHIVE_PASSWORD"] = self._client_dict["HMS_BEEHIVE_PASSWORD"]
        self.controller_info["BEEHIVE_URL"] = self._client_dict["HMS_BEEHIVE_URL"]
        self.controller_info["IP"] = self._client_dict["IP"]
        return self.controller_info

    def is_openremote_running(self):
        '''
        :Description: Check HMS is UP or Not. 
        1) DUT is ONLINE
        2) HMS OR is RUNNNING or Not
        :return: Client is Ready or Not Ready
        '''

        __ip_flag = self.login_obj.login_to_DUT_console(self.controller_info["IP"])
        __or_flag = self.login_obj.execute_command_on_DUT_console("pgrep siege")

        if not __ip_flag and not __or_flag: raise clientException("Client is not Ready")