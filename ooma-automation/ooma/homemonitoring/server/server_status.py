import os
import urllib2
import json
import platform
import logging
import colorlog

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.ERROR)
logger = logging.getLogger(__name__)

class ServerStatus():
    def __init__(self, jsonconfig, node="cert"):
        self.node = node
        self._jsonconfig = jsonconfig
        self._hostname_port = jsonconfig[node]["hms-server"]
        self.__hms_path = "/hms/ping"
        self._nimbits_server = self._jsonconfig[self.node]["nimbits-server"]
        self._beehive_server = self._jsonconfig[self.node]["beehive-server"]

    def check_all_server_status(self):
        logger.info("Check_all_server_status Started")
        __hms_status = self.ping_hms()
        logger.info('HMS Status is %s', __hms_status)

        __beehive_status = self.ping_beehive()
        logger.info('Beehive Server Status is %s', __beehive_status)

        __nimbits_status = self.ping_nimbits()
        logger.info("Nimbits Server Status is %s", __nimbits_status)
        logger.info("Check_all_server_status Ended")

    def http_ping(self, url):
        '''
        Send the HTTP Req to the server and waiting for the response
        :param url: hms server urls
        :return: code - 1XX, 2XX, 3XX 4XX, 5XX responses
        '''
        req = urllib2.Request(url)

        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')

        f = urllib2.urlopen(req)
        response = f.read()
        code = f.getcode()

        return code

    def tomcat_is_up(self, __hostname):
        '''
        Check Tomcat server is running on the host machine
        $ nc -z hms1-cert1.cn.ooma.com 8084
        Connection to hms1-cert1.cn.ooma.com port 8084 [tcp/*] succeeded!
        :param __hostname: 
        :return: TRUE/FALSE
        '''
        response = os.system("nc -z %s %s" % tuple(__hostname.split(":")))

        if response == 0:
            logger.info("%s is up!!!!!!" , __hostname)
            return True
        else:
            logger.exception("%s is Down!!!!!!", __hostname)
            return False

    def ping_hms(self, version=None):
        '''
        Pinging the HMS Server with URL - 'http://hms1-cert1.cn.ooma.com:8084/hms/ping'
        :param version: 
        :return: TRUE or FALSE
        '''
        self._url = "http://%s%s" % (self._hostname_port, self.__hms_path)
        logger.info("ping_hms - %s", format(self._url))
        try:
            self.server_version = self.http_ping(self._url)

        except urllib2.URLError as e:
            logger.exception("Error in Pinging HMS Server - %s", e.reason)

        tomcat_status = self.tomcat_is_up(self._hostname_port)

        if version and version == self.server_version and tomcat_status:
            return True
        elif self.server_version:
            return True
        else:
            return False

    def ping_nimbits(self):
        '''
        Pinging the nimbits Server with nc command'
        :param version: 
        :return: TRUE or FALSE
        '''
        __nimbits_status = self.tomcat_is_up(self._nimbits_server)
        if __nimbits_status:
            return True
        else:
            return False

    def ping_beehive(self):
        '''
        Pinging the Beehive Server with nc command'
        :param version: 
        :return: TRUE or FALSE
        '''
        __beehive_status = self.tomcat_is_up(self._beehive_server)
        if __beehive_status:
            return True
        else:
            return False