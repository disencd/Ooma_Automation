import os
import urllib2
import json
import platform

class Configuration:
    def __init__(self):
        self.hostname_port = "hms1-cert1.cn.ooma.com:8084"
        #self.hostname_port = "hms.pbeta.ooma.com:8083"
        self.hms_path = "/hms/ping"
        self.emulator_path = "emulator_path"

    def http_ping(self, url):
        req = urllib2.Request(url)

        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')

        f = urllib2.urlopen(req)
        response = f.read()
        code = f.getcode()

        return code

    def ping_hms(self, version=None):
        url = "http://%s%s" % (self.hostname_port, self.hms_path)

        return  self.http_ping(url)

        assert (server_version != ""), "Cannot ping hms server %s" % url
        if version and version == server_version:
            return True
        elif server_version:
            return True
        else:
            return False

    def ping_emulator(self, version="0.89"):
        url = "http://%s%s" % (self.hostname_port, self.emulator_path)

        server_version = self.http_ping(url)

        assert (server_version != ""), "Cannot ping emulator  %s" % url
        if version and version == server_version:
            return True

        return False

    def tomcat_is_up(self):
        hostname = self.hostname_port
        if platform.system() == "Darwin":
            response = os.system("nc -z %s %s" % tuple(self.hostname_port.split(":")))
        else:
            print "Windows system: cannot make port check for Tomcat server"
            return True

        if response == 0:
            print hostname, 'is up!'
            return True
        else:
            print hostname, 'is down!'
            return False
