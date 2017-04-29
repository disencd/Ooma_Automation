import json
import os
import random, string
from datetime import datetime
import paramiko
import base64


def get_dir_name(length=6):
    date = datetime.now().strftime("%y-%m-%d-%H-%M-%S")

    return date + "-" +  ''.join(random.choice(string.lowercase) for i in range(length))


def ssh_cmd(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname="hms1-cert1.cn.ooma.com", username="root", password="!hello123", port=22)	
    channel = client.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(5)
    print "COMMAND: " , cmd
    channel.exec_command(cmd)
    print channel.recv(1024)

    channel.close()
    client.close()

def put_logs():
    name = get_dir_name()
    dir_name = "/tmp" + name
    get_log_links(name)
    account_no = '4693019883'	
    mk_dir = 'mkdir %s\n' % dir_name
    grep_cmd = 'grep %s /var/log/hms.log > %s/hms.log' % (account_no, dir_name)	
    #cp_file = 'cp -f /var/log/hms.log %s\n' % dir_name

    #for cmd in [mk_dir, cp_file]:
    for cmd in [mk_dir, grep_cmd]:

      
        ssh_cmd(cmd) 


def get_json(data):
    try:
        return json.loads(data)
    except ValueError, e:
        print "data does not contain json"
        raise e


def links_list(build_num):

    log_files = ["hms.log", "controllercommandservice.log"]
    link_template = "http://hms1-cert1.cn.ooma.com:8081/logs/%s/%s"	
    return [link_template % (build_num, log_name) for log_name in log_files]


def get_log_links(build_num="0"):
    try:
        link_list = links_list(int(os.environ["BUILD_NUMBER"]))
    except Exception, e:
        os.environ["BUILD_NUMBER"] = build_num
        link_list = links_list(build_num)

    print "-----------------------------------------------------------"
    print "--------Server logs can be found Links for logs------------"
    for item in link_list:
        print item

def get_http_basic_header(username, password):
    return base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
