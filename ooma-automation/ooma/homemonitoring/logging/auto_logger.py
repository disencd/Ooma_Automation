import json
import sys
import paramiko
import time
import logging
import requests
import subprocess
import threading
import re
import os
get_abs_file_path = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))
file_path = get_abs_file_path('../../../continuous_integration/client/')
sys.path.append(file_path)
file_path = get_abs_file_path('../../client/client_utilities')
sys.path.append(file_path)
import TestBedHealthCheckup
import ConfigOperations
import Wps_Control
from datetime import datetime, timedelta
from time import strftime
import time

class auto_logger(object):

	def start_client_logging(self, tc_name, flag=0): # flag used for reboot case to call start_client_logging more than once.
		logging.info('Auto_Logger: Fetching Log Details..')
		self.admin_server, self.pro_server = TestBedHealthCheckup.get_server_details()
		self.device = TestBedHealthCheckup.get_DUT_details()			
		self.tc_name = tc_name
		self.logger_intialization()
		start = self.enable_syslog()
		self.log_file_name = self.tc_name + '.log'
		if start == 0:
			if flag == 0:
				buff = self.execute_command_on_DUT_console('pkill tail;logread -f > /opt/%s &' % self.log_file_name)
			elif flag > 0:	# when start_client_logging called more than once, logs will be appended to old log file. 
				buff = self.execute_command_on_DUT_console('pkill tail;logread -f >> /opt/%s &' % self.log_file_name)
			logging.info('Auto_Logger: Started syslog capture for test case : %s' % self.tc_name)
		else:
			logging.error('Auto_Logger: Failed to start syslog!')
		return self


	################################################################################################

	def stop_client_logging(self, reboot_flag=0, voxweaver=0):
		print 'Auto_Logger: Stopping syslog capture'
		time.sleep(5)
		logging.info('Auto_Logger: Stopping syslog capture for test case : %s' % self.tc_name)
		#login_to_DUT_Console to handle VPN ip fluctuation.
		
		self.login_to_DUT_console()
		kill = 0
		if int(reboot_flag) == 1:
			kill = 1
			logging.info('Reboot Flag is set. Hence copying locallog file to log directory!')
			buff = self.execute_command_on_DUT_console('cp /var/log/locallog /opt/%s_1.log;cat /opt/%s_1.log >> /opt/%s; rm -fr /opt/%s_1.log' % (self.tc_name,self.tc_name,self.log_file_name,self.tc_name))
		else:
			buff = self.execute_command_on_DUT_console('pkill logread -f;pkill tail')
			i = 1		
			while i < 5:
				buff = self.execute_command_on_DUT_console('ps | grep logread | grep -v grep')
				for line in buff.split('\n'):
					logging.info(line)
					if line.find('logread -f') < 0:
						logging.info('Auto_Logger: logread -f process killed successfully!')
						kill = 1
						break
				if kill == 0:
					logging.info('Auto_Logger: Unable to kill logread -f process. Killing again!')
					buff = self.execute_command_on_DUT_console('pkill logread -f;pkill tail')
					i += 1
				else:
					break

		if kill == 1:
			self.set_log_path()			
			success = self.save_syslog_file(voxweaver)
			if success == 0:			
				logging.info('Auto_Logger: Logs saved at %s/%s on server %s' % (self.log_path, self.log_file_name, self.log_server))
				logging.info('Auto_Logger: Deleting logs from DUT...')
			else:
				logging.error('Auto_Logger: Unable to save logs!')
			buff = self.execute_command_on_DUT_console('rm -f /opt/%s;rm -rf /var/log/locallog.0;> locallog' % self.log_file_name)
			
	


	################################################################################################

	def set_log_path(self):
		if str(os.environ.get('BuildID')) != 'None' and len(str(os.environ.get('BuildID'))) > 0:
			logging.info('Test Case is running in CI!')
			self.BuildID = str(os.environ.get('BuildID'))
			self.testrun_id = str(os.environ.get('TEST_RUN_ID'))
			self.job_name = str(os.environ.get('JOB_NAME'))
			self.log_path = '/var/www/html/Automation_logs/' + self.job_name + '/' + self.testrun_id + '/' + self.BuildID
			self.ci = 1
		else:
			try:
				self.job_name = str(os.environ.get('JOB_NAME'))
				self.testrun_id = str(os.environ.get('TEST_RUN_ID'))
				if 'Core' in self.job_name:
					self.ci = 1
					timestamp = ('').join(str(datetime.now()).split(' ')[0].split('-'))
					self.log_path = '/var/www/html/Automation_logs/' + self.job_name + '/' + self.testrun_id + '/' + timestamp
					return
			except:
				logging.info("Test Case not running in CI!")

			self.ci = 0
			self.log_path = '/tmp/Automation_logs'
			logging.info('Auto_Logger: Test Case not running in CI! Logs will saved on Log server only!')



	################################################################################################

	def logger_intialization(self):
		logging.info('Auto_Logger: In logger_initialization')
		self.SPN = self.device['spn']
		self.myx_id = self.device['myx_id']
		self.type = self.device['product_type']
		self.node = self.device['node']
		self.admin_ip = self.admin_server['admin_ip']
		self.user = self.admin_server['server_user']
		self.pwd = self.admin_server['server_pwd']
		self.log_server_ip = self.admin_server['log_server_ip']
		self.pro_server = self.pro_server['provision1_dc1_ip']

		#Workaround for ssh to szeto/chen node devices 
		self.workaround = ""
		if self.node.lower().strip() == "szeto" or self.node.lower().strip() == "chen":
			self.workaround = " -i telokey.ssh"


	################################################################################################

	def enable_syslog(self):
		logging.info('Auto_Logger: In enable_syslog')

		self.login_to_DUT_console()
		buff = self.execute_command_on_DUT_console('ps | grep syslog | grep -v grep')		
		
		for line in buff.split('\n'):
			if line.find('rsyslog.conf') >= 0:
				logging.info(line)
				buff = self.execute_command_on_DUT_console('touch /var/log/locallog')
				logging.info('Auto_Logger: Logging is enabled')
				return 0

		logging.info('Auto_Logger: Logging is disabled.Enabling syslog!')
		buff = self.execute_command_on_DUT_console('cd /opt/log;rm -f rsyslog.conf; ln -s /etc/rsyslog.conf.spool rsyslog.conf; monit restart rsyslogd')
		for line in buff.split('\n'):
			if line.find('rsyslog.conf') >= 0:
				logging.info(line)
				logging.info('Auto_Logger: Enabled syslog!')
				return 0		

		logging.error('Auto_Logger: Unable to enable syslog!')
		return 1


	################################################################################################

	def login_to_DUT_console(self, node='Cert'):
		self.ssh = self.ssh_to_server(self.admin_ip, self.user, self.pwd)
		self.chan = self.ssh.invoke_shell()
			
	
		ssh_command = 'ssh ' + self.user + '@' + self.pro_server
		wait_period = 30        # wait period(in secs) for ssh timeout
		while wait_period > 0:          
			logging.info('Auto_Logger: Sending command : %s' % ssh_command)
			self.chan.send(ssh_command + '\n')  
        		time.sleep(8)
			buff = ''
        		while self.chan.recv_ready():   #read buffer only if data is available
        			buff += self.chan.recv(9999)
			if ")?" in buff:
				self.chan.send('yes' + '\n')
				time.sleep(2)
				break
        		if "password:" in buff:
				break
			wait_period -= 5
			self.chan.send('\x03')
			logging.info("Auto Logger: Retrying ssh...")
			if wait_period == 0:
				logging.error('Auto_Logger: Proserver %s not reachable!!' % self.pro_server)
				sys.exit(1)

		self.chan.send(self.pwd + '\n')                                   
		buff = ''
		while not buff.endswith('# '):
    			resp = self.chan.recv(9999)
    			buff += resp

		vpnIP = self.get_vpn_ip()
		if vpnIP != None and vpnIP !='Not registered':
			ssh_command = 'ssh ' + str(vpnIP) + self.workaround
			wait_period = 300        # wait period(in secs) for ssh timeout
			while wait_period > 0:          
				logging.info('Auto_Logger: Sending command : %s' % ssh_command)
				self.chan.send(ssh_command + '\n')  
        			time.sleep(8)
				buff = ''
        			while self.chan.recv_ready():   #read buffer only if data is available
        				buff += self.chan.recv(9999) 
        			if " ; " in buff:
					break
				wait_period -= 5
				if ")?" in buff:
					self.chan.send('yes' + '\n')
					time.sleep(2)
					break
				self.chan.send('\x03')
				logging.info("Auto Logger: Retrying ssh...")
				vpnIP = self.get_vpn_ip()
				ssh_command = 'ssh ' + str(vpnIP) + self.workaround
				if wait_period == 0:
					logging.error('Auto_Logger: DUT %s not reachable!!' % str(vpnIP))
					sys.exit(1)
		else:		
			if vpnIP == 'Not registered':
				logging.error('Auto_Logger: Device not registered!')			
			else:			
				logging.error('Auto_Logger: DUT not reachable!')
			sys.exit(1)	



	################################################################################################

	def save_syslog_file(self, voxweaver=0):

		if self.ci == 1:
			self.log_server = str(os.environ.get('SSH_CLIENT')).split()[0]
			self.log_server_user = 'root'
			if '10.66' in self.log_server:
				self.log_server_pwd = '!hello123' 	#temp changing to prod pwd
			else:			
				self.log_server_pwd = 'ooma@123'           
			logging.info('Auto_Logger: Checking for log folder on Jenkins Master...')
			self.check_log_path()
			logging.info('Auto_Logger: Fetching log file to Jenkins Master...')
		else:
			self.log_server = self.log_server_ip
			self.log_server_user = self.user
			self.log_server_pwd = self.pwd
			logging.info('Auto_Logger: Checking for log folder on Log server...')
			self.check_log_path()
			logging.info('Auto_Logger: Fetching log file to Log server...')

		if voxweaver == 1:
			self.log_path = self.log_path + '/' + self.tc_name + '.log'
			self.check_log_path()

		cmd  = 'scp /opt/' + self.log_file_name + ' ' + self.log_server_user + '@' + self.log_server  + ':' + self.log_path
		try:
			logging.info('Auto_Logger: Sending command %s' % cmd)
			self.chan.send(cmd + '\n')
			buff = ''
			while not buff.endswith('password: '):
    				resp = self.chan.recv(9999)
    				buff += resp
				if resp.find('connecting? (y/n)') >= 0:
					break
				if resp.find('No such file or directory') >= 0:
					logging.info('Auto_Logger: No log file %s found in /opt/ dir of DUT!' % self.log_file_name)
					return 1	
			
			# Handling rsa key scenario 
			if buff.split('\n')[-1].find('(y/n)') >= 0:
				self.chan.send('y' + '\n')
				buff = ''
				while not buff.endswith('password: '):
    					resp = self.chan.recv(9999)
    					buff += resp		
		
			self.chan.send(self.log_server_pwd + '\n')                                   
			buff = ''
			while not buff.endswith(' ; '):
    				resp = self.chan.recv(9999)
    				buff += resp		
		
			logging.info(buff)
			return 0

		except Exception as e :
        		exc_type, exc_obj, exc_tb = sys.exc_info()
        		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        		logging.error("Auto_Logger: scp to Log server failed!. Exception : %s %s %s %s"% (e, exc_type, fname, str(exc_tb.tb_lineno)))
			return 1


	################################################################################################

	def get_vpn_ip(self) :
		"""
		Description : 
		Input : 
		"""
		cmd = 'showmyx ' + str(self.myx_id) + '| grep IPADDR | awk \'{print $2}\''
		logging.info('Auto_Logger: Fetching VPN IP with command %s ...' % cmd)
		wait_period = 600        # wait period(in secs) for telo to reboot 
		while wait_period > 0:          
        		self.chan.send(cmd + "\n")
        		time.sleep(5)
			op = ''
        		while self.chan.recv_ready():   #read buffer only if data is available
        			op += self.chan.recv(9999)
        		if "not registered" in op:
        			logging.warning( "The device is not provisioned/resgistered with the provserver server")
				return "Not registered"  
        		elif "." in op:
				#logging.info(op)
				return re.search('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',op).group()
			else:
				pass   
			wait_period -= 5
			self.chan.send('\x03')
			logging.info("Auto Logger: Retrying fetching VPN IP...")
		return None	


	################################################################################################

	def execute_command_on_DUT_console(self, command):
		try:		
			logging.info('Auto_Logger: Sending command : %s' % command)
			self.chan.send(command + '\n')                                   
			buff = ''
			while not buff.endswith(' ; '):
    				resp = self.chan.recv(9999)
    				buff += resp

			return buff
		except Exception as e :
        		exc_type, exc_obj, exc_tb = sys.exc_info()
        		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        		logging.error("Auto_Logger: Unable to run command on DUT. Exception : %s %s %s %s"% (e, exc_type, fname, str(exc_tb.tb_lineno)))



	################################################################################################

	def check_log_path(self):
		try:
			ssh = self.ssh_to_server(self.log_server, self.log_server_user, self.log_server_pwd)
			ssh.exec_command('mkdir -p %s' % self.log_path)
			ssh.close()
		except Exception as e :
        		exc_type, exc_obj, exc_tb = sys.exc_info()
        		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        		logging.error("Auto_Logger: Unable to SSH to server. Check log path failure. Exception : %s %s %s %s"% (e, exc_type, fname, str(exc_tb.tb_lineno)))
			sys.exit(1)



	################################################################################################

	def ssh_to_server(self, host, user, passwd):
		#logging.info("Auto_Logger: Ssh to server via admin")
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(host, timeout=20, username=user, password=passwd)
			logging.info("Auto_Logger: We are in %s " % host)
			return ssh
		except Exception as e :
        		exc_type, exc_obj, exc_tb = sys.exc_info()
        		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        		logging.error("Auto_Logger: Unable to SSH to server %s(user=%s,pwd=%s). Exception : %s %s %s %s"% (host, user, passwd, e, exc_type, fname, str(exc_tb.tb_lineno)))
			sys.exit(1)



	################################################################################################

	def init_voxweaver_test(self):
		try:
        		file_path = get_abs_file_path('../../../test_automation/global/config/')
			file_path += '/voxweaver_config.cfg'
			#os.environ['SETUP'] = '1' #added for core testing loaclly from ride
			#logging.info("SETUP : %s " % os.environ.get('SETUP'))
			if os.environ.get('SETUP') == '1':
				section = 'Voxweaver_Core'
			else:
				Device_info = TestBedHealthCheckup.get_DUT_details()
				section = Device_info['vox_section']
				logging.info("Auto_Logger: Section selected : %s" % section)							
		except:
			logging.info('Auto_Logger: No enviroment variable SETUP found!!')
			Device_info = TestBedHealthCheckup.get_DUT_details()
			section = Device_info['vox_section']
			logging.info("Auto_Logger: Section selected : %s" % section)

		self.ServerSection = ConfigOperations.return_section(file_path, section)
		#logging.info(self.ServerSection)	
		self.dataserver = self.ServerSection['voxweaver_dataserver']
		self.network = self.ServerSection['voxweaver_network']
		self.binding_path = self.ServerSection['voxweaver_binging_path']
		self.network_path = self.ServerSection['voxweaver_network_path']
		self.exec_path = self.ServerSection['voxweaver_exec_path']
		self.log_path = self.ServerSection['voxweaver_log_path']
		self.vox_server = self.ServerSection['voxweaver_server']
		self.vox_user = self.ServerSection['voxweaver_user']
		self.vox_pwd = self.ServerSection['voxweaver_password']
		self.device_myx_mapping = self.ServerSection['device_myx_mapping']
		self.admin_ip = self.ServerSection['admin_ip']
		self.user = self.ServerSection['user']
		self.pwd = self.ServerSection['pwd']
		self.log_server_ip = self.ServerSection['log_server_ip']
		logging.info(self.device_myx_mapping)
		self.device_myx_mapping = self.device_myx_mapping.replace(',','\n')


	################################################################################################

	def start_voxweaver_logs(self, tc_name, binding):
		'''
		   Description	: This function starts capturing syslogs on the devices identified from the bindings.
		   Arguments 	: Test case name, binding
		   Returns	: None
		'''
		self.binding = binding.split(' ')
		self.tc_name = tc_name
		self.init_voxweaver_test()
		self.get_device_list_from_binding()
		logging.info(self.devices)
		#self.admin_server, self.pro_server = TestBedHealthCheckup.get_server_details()
		for key in self.devices.keys():
			for device in self.devices[key]:
				logging.info("Auto_Logger: Enabling syslog on %s" % device.split(' ')[0])
				self.log_file_name = self.tc_name + '_' + key + '.log'
				self.myx_id = device.split(' ')[1]
				self.workaround = ""
				if device.split(' ')[0].startswith('sbox'):
					self.pro_server = '172.16.0.110'
				elif device.split(' ')[0].startswith('cert'):
					self.pro_server = '10.5.0.150'
                                elif device.split(' ')[0].startswith('chen'):
					self.workaround = " -i telokey.ssh"
                                        self.pro_server = self.ServerSection['chen_pro_server']	
                                elif device.split(' ')[0].startswith('szeto'):
					self.workaround = " -i telokey.ssh"
                                        self.pro_server = self.ServerSection['szeto_pro_server']
				start = self.enable_syslog()

				if start == 0:
					buff = self.execute_command_on_DUT_console('pkill tail;logread -f > /opt/%s &' % self.log_file_name)
					logging.info('Auto_Logger: Started syslog capture for test case : %s' % self.tc_name)
				else:
					logging.error('Auto_Logger: Failed to start syslog!')			


		
	
	################################################################################################

	def stop_voxweaver_logs(self, binding):
		'''
		   Description	: This function stops capturing syslogs on the devices identified from the bindings.
		   Arguments 	: binding
		   Returns	: None
		'''
		for key in self.devices.keys():
			for device in self.devices[key]:
				logging.info("Auto_Logger: Stopping logging on %s" % device.split(' ')[0])
				self.log_file_name = self.tc_name + '_' + key + '.log'
				self.myx_id = device.split(' ')[1]
				self.workaround = ""
				if device.split(' ')[0].startswith('sbox'):
					self.pro_server = '172.16.0.110'
				elif device.split(' ')[0].startswith('cert'):
					self.pro_server = '10.5.0.150'
                                elif device.split(' ')[0].startswith('chen'):
					self.workaround = " -i telokey.ssh"
                                        self.pro_server = self.ServerSection['chen_pro_server']	
                                elif device.split(' ')[0].startswith('szeto'):
					self.workaround = " -i telokey.ssh"
                                        self.pro_server = self.ServerSection['szeto_pro_server']	
				self.stop_client_logging(0,1)



	################################################################################################

	def get_device_list_from_binding(self):
		'''
		   Description	: This function derives origin, destination and remote devices under test from the bindings.
		   Arguments 	: None
		   Returns	: It saves the origin , destination and remote devices in class variables.  
		'''
		self.devices = {}
		device_dict = {}
		device_dict['origin'] = []
		device_dict['destination'] = []
		device_dict['remote'] = []
		temp = -1
		temp_dict = {}
		temp_dict['origin'] = []
		temp_dict['destination'] = []
		temp_dict['remote'] = []
		for binding in self.binding:		
			ssh = self.ssh_to_server(self.vox_server,self.vox_user,self.vox_pwd)
			stdin,stdout,stderr = ssh.exec_command('cat ' + self.binding_path + binding + '.json')		
			for line in stdout.readlines():
				if line.find('subject') > 0:
					if line.find('origin') > 0:						
						temp = 0
					if line.find('destination') > 0:						
						temp = 1
					if line.find('remote') > 0:						
						temp = 2
				if line.find('predicate') > 0:
					regex = line.split(':')[1].strip().strip(',').strip('"')
					regex = ".*" + regex + ".*"
					#logging.info(regex) add try catch.
					matches = re.findall(regex, self.device_myx_mapping)
					#logging.info(matches)
					if len(matches) > 0:
						for device in matches:
							if temp == 0 :
								device_dict['origin'].append(device)
							if temp == 1 :
								device_dict['destination'].append(device)
							if temp == 2 :
								device_dict['remote'].append(device)
					else:
						logging.info("Auto_Logger: No matches found for binding %s" % binding)			
			if len(self.binding) == 1:
				if len(device_dict['origin']) > 0:
					self.devices['origin'] = device_dict['origin']
				elif len(device_dict['destination']) > 0:
					self.devices['destination'] = device_dict['destination']
			else: 
				self.devices['origin'] = list(set(temp_dict['origin']).intersection(set(device_dict['origin'])))
				self.devices['destination'] = list(set(temp_dict['destination']).intersection(set(device_dict['destination'])))
				self.devices['remote'] = list(set(temp_dict['remote']).intersection(set(device_dict['remote'])))

			for key in device_dict.keys():
				temp_dict[key] = list(device_dict[key])
			device_dict['origin'] = []
			device_dict['destination'] = []
			device_dict['remote'] = []			



	################################################################################################

	def fetch_SPN_for_devices(self):
		'''
		   Description	: This function fetched SPN for origin, destination and remote devices.
		   Arguments 	: None
		   Returns	: List of SPN per device.  
		'''		
		ssh = self.ssh_to_server(self.vox_server,self.vox_user,self.vox_pwd)
		stdin,stdout,stderr = ssh.exec_command('cat ' + self.network_path + self.network + '.json')   
    		data = json.loads(stdout.read())
		index = 0
		#logging.info(data['servers'][0]['clients'][2]['arguments']['did'])
		spn_list = []
		for item in data['servers'][0]['clients']:
			#logging.info(item['arguments']['subclients'][0]['name'])
			for key in self.devices.keys():
				for device in self.devices[key]:
					#logging.info(device.split(' ')[0])
            				if str(item['arguments']['subclients'][0]['name']) == device.split(' ')[0]:
						spn_list.append(data['servers'][0]['clients'][index]['arguments']['did'])				
						break
			index += 1
		logging.info(spn_list)
		return spn_list

	#####################################################################

	def login_to_XC(self,XC_IP):
		'''
		   Description	: This function logs in to Xcoder.
		   Arguments 	: Xcoder IP
		   Returns	: SSH channel
		'''
		self.ssh = self.ssh_to_server(self.admin_ip, self.user, self.pwd)
		chan_xc = self.ssh.invoke_shell()	
		try:
			ssh_command = 'ssh ' + self.user + '@' + str(XC_IP)
			wait_period = 30        # wait period(in secs) for ssh timeout
			while wait_period > 0:          
				logging.info('Auto_Logger: Sending command : %s' % ssh_command)
				chan_xc.send(ssh_command + '\n')  
				time.sleep(8)
				buff = ''
				while chan_xc.recv_ready():   #read buffer only if data is available
					buff += chan_xc.recv(9999)
				if ")?" in buff:
					chan_xc.send('yes' + '\n')
					time.sleep(2)
					break
				if "password:" in buff:
					break
				wait_period -= 5
				chan_xc.send('\x03')
				logging.info("Auto Logger: Retrying ssh...")
				if wait_period == 0:
					logging.error('Auto_Logger: XC %s not reachable!!' % XC_IP)
					sys.exit(1)

			chan_xc.send(self.pwd + '\n')                                   
			buff = ''
			while not buff.endswith('# '):
	    			resp = chan_xc.recv(9999)
	    			buff += resp

			logging.info('Auto_Logger: Successfully logged in to XC!')
			return chan_xc
		except Exception as e :
        		exc_type, exc_obj, exc_tb = sys.exc_info()
        		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        		logging.error("Auto_Logger: Unable to ssh to XC1. Exception : %s %s %s %s"% (e, exc_type, fname, str(exc_tb.tb_lineno)))
			sys.exit(1)


	################################################################################################

	def start_thread(self, channel, t=1):
		timestamp = str(datetime.now()).split(' ')[0] + '-' + ('-').join(str(datetime.now()).split(' ')[1].split(':')[:2]) + '-' + str(datetime.now()).split(' ')[1].split(':')[2].split('.')[0]
		self.xc_log_file = '/tmp/XC-' + self.tc_name + '-' + timestamp + '.log'		
		channel.send('pwd ; nohup ./fs_cli -P 8027 -p Switchfreecon > ' +  self.xc_log_file  + ' &' + '\n')
    		#resp = channel.recv(9999)
		#logging.info('Response : ' + resp)



	################################################################################################

	def start_logs_on_XC(self):
		'''
		   Description	: This function captures logs on Xcoder.
		   Arguments 	: None
		   Returns	: None
		'''
		chan_xc = self.login_to_XC('172.19.15.165')
		chan_xc.send('cd /etc/init.d/' + '\n')
		resp = chan_xc.recv(9999)
		chan_xc.send("ls -lrt | grep ooma_freeswitch-xcoder | awk '{print $NF}'" + '\n')
		time.sleep(2)
		resp = chan_xc.recv(9999)
		build = re.search('.*[0-9]{6}',str(resp))
		fs_path = build.group() + '/usr/local/freeswitch/bin/'
		chan_xc.send("cd " + fs_path + '\n')
		self.thread1 = threading.Thread(target = self.start_thread, args = (chan_xc,1))
		self.thread1.start()
		time.sleep(5)
		self.thread1.join()
		chan_xc.send('ps -ef | grep fs_cli | grep -v grep' + '\n')
		time.sleep(3)
		resp = chan_xc.recv(9999)
		logging.info('Response : ' + resp)
		logging.info("Auto_Logger: Started logger on XC!")


	################################################################################################

	def stop_logs_on_XC(self):
		'''
		   Description	: This function stops logging on Xcoder.
		   Arguments 	: None
		   Returns	: None
		'''
		logging.info('Auto_Logger: Stopping logs on XC...')
		chan_xc = self.login_to_XC('172.19.15.165')
		counter = 1
		while counter < 3:
			chan_xc.send('ps -ef | grep fs_cli | grep -v grep' + '\n')
			time.sleep(1)
			resp = chan_xc.recv(9999)
			logging.info(resp)
			try:
				pid = re.search('root.*[0-9]{2,6}',str(resp))
				#logging.info("Auto_Logger: PID to kill is " + pid.group().split()[1])
				chan_xc.send('kill -9 ' + pid.group().split()[1] + '\n')
			except:
				logging.info('No logger process running on XC!')
				return
			chan_xc.send('ps -ef | grep fs_cli | grep -v grep' + '\n')
			time.sleep(1)
			resp = chan_xc.recv(9999)
			if str(resp).find('8027') > 0:
				counter = counter + 1
			else:
				logging.info("Auto_Logger: XC logger process killed successfully!")
				break
			logging.info("Auto_Logger: Retrying to kill XC logger process...")
		
		success = self.transfer_log_file(chan_xc, self.xc_log_file)
		if success == 0:
			#self.verify_XC_logs(spn)
			logging.info('XC log file %s transferred successfully to /tmp/ dir of admin server!' % self.xc_log_file)
		else:
			logging.error('Failed to scp xc logs. Please manually check XC logs in ' + self.xc_log_file)



	################################################################################################

	def verify_XC_logs(self, spn_origin, spn_dest):
		'''
		   Description	: This function verifies Xcoder logs.
		   Arguments 	: None
		   Returns	: None
		'''
		logging.info('Verification of XC logs initiated...')
		self.spn_origin = spn_origin
		self.spn_dest = spn_dest
		ssh = self.ssh_to_server(self.admin_ip, self.user, self.pwd)
		try:
			search_str = "cat " + self.xc_log_file + " | grep -E 'INVITE sip:" + self.spn_origin + "@|BYE sip:" + self.spn_dest + "@|ACK sip:" + self.spn_origin + "@'"
			#search_str = "cat " + self.xc_log_file + " | grep -E 'INVITE sip:|BYE sip:|ACK sip:'"
			logging.info('Sending command %s' % search_str)
			stdin,stdout,stderr = ssh.exec_command(search_str)
			dict_call = {'INVITE':0,'ACK':0,'BYE':0}
			for line in stdout.readlines():
				#logging.info(line)
				if line.find('INVITE') > 0 :
					logging.info(line)
					dict_call['INVITE'] = 1
					continue
				if line.find('ACK') > 0 :
					logging.info(line)
					dict_call['ACK'] = 1
					continue					
				if line.find('BYE') > 0 :
					logging.info(line)
					dict_call['BYE'] = 1

			for key in dict_call:
				if dict_call[key] == 1 :
					logging.info("Auto_Logger: %s Verified in XC logs" % key)		
				else:
					logging.error("Auto_Logger: %s not present in XC logs!" % key)
		
		except Exception as e :
        		exc_type, exc_obj, exc_tb = sys.exc_info()
       			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        		logging.error("Auto_Logger: Verification of XC logs failed!. Exception : %s %s %s %s"% (e, exc_type, fname, str(exc_tb.tb_lineno)))
			sys.exit(1)



	################################################################################################

	def transfer_log_file(self, chan, log_file):
		'''
		   Description	: This function transfers logs to Admin server using scp.
		   Arguments 	: ssh channel
		   Returns	: 0 on success. -1 on failure
		'''
		logging.info('Transferring log file...')	
		cmd  = 'scp ' + log_file + ' ' + self.user + '@' + self.admin_ip  + ':/tmp/' 
		try:
			logging.info('Auto_Logger: Sending command %s' % cmd)
			chan.send(cmd + '\n')
			buff = ''
			while not buff.endswith('password: '):
    				resp = chan.recv(9999)
    				buff += resp
				logging.info(resp)
				if 'connecting' in resp:
					#chan.send('yes' + '\n')
					#time.sleep(1)
					break

			# Handling rsa key scenario 
			logging.info(buff)
			logging.info(buff.split('\n')[-1])
			if buff.split('\n')[-1].find('(y') >= 0:
				chan.send('yes' + '\n')
				buff = ''
			
				while not buff.endswith('password: '):
    					resp = chan.recv(9999)
    					buff += resp
			
			logging.info("Sending password ##############")
			chan.send(self.pwd + '\n')  
			time.sleep(3)
			resp = chan.recv(9999)
			logging.info(resp) 
			'''                              
			buff = ''			
			if 'XC' in log_file:
				logging.info('In xc...')
				while not buff.endswith('# '):
    					resp = chan.recv(9999)
    					buff += resp
			else:
				logging.info('In sawmill...')
				while not buff.endswith('$ '):
    					resp = chan.recv(9999)
    					buff += resp					
			logging.info(buff)
			'''
			return 0			
		except Exception as e :
        		exc_type, exc_obj, exc_tb = sys.exc_info()
       			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        		logging.error("Auto_Logger: SCP of XC logs to Admin server failed!. Exception : %s %s %s %s"% (e, exc_type, fname, str(exc_tb.tb_lineno)))
			return 1


	################################################################################################

	def add_spn_to_calea_list(self, spn):
		'''
		   Description	: This function adds SPN to the Calea list.
		   Arguments 	: Device (origin/destination/remote)
		   Returns	: None
		'''
		self.calea_spn = spn		
		ssh = self.ssh_to_server('10.66.12.55', self.user, self.pwd)
		try:
			cmd = 'echo "' + self.calea_spn + ' ' + self.calea_spn + ' ' + '1:"' + '>> /oomasw/var/blacklist/calea.txt'
			logging.info('Auto Logger: Executing command : %s' % cmd)
			ssh.exec_command(cmd)
			logging.info('Auto Logger: Added SPN %s to Calea list successfully!' % self.calea_spn)	
		except Exception as e :
        		exc_type, exc_obj, exc_tb = sys.exc_info()
       			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        		logging.error("Auto_Logger: Failed to add SPN to calea.txt file!. Exception : %s %s %s %s"% (e, exc_type, fname, str(exc_tb.tb_lineno)))
			sys.exit(1)



	################################################################################################

	def delete_spn_from_calea_list(self):
		'''
		   Description	: This function deletes SPN from the Calea list.
		   Arguments 	: SPN to be deleted
		   Returns	: None
		'''		
		ssh = self.ssh_to_server('10.66.12.55', self.user, self.pwd)
		try:
			cmd = "sed -i " + "'/" + self.calea_spn + " " + self.calea_spn + " " + "1:" + "/d'" + " /oomasw/var/blacklist/calea.txt"
			logging.info('Auto Logger: Executing command : %s' % cmd)
			ssh.exec_command(cmd)
			logging.info('Auto Logger: Deleted SPN %s from Calea list successfully!' % self.calea_spn)	
		except Exception as e :
       			exc_type, exc_obj, exc_tb = sys.exc_info()
       			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        		logging.error("Auto_Logger: Failed to add SPN to calea.txt file!. Exception : %s %s %s %s"% (e, exc_type, fname, str(exc_tb.tb_lineno)))
			sys.exit(1)


	################################################################################################

	def read_log_file(self, target, key):
		'''
		   Description	: This function read log file and return values for particular key.
		   Argument	: key : read value of key
		   Argument	: target : read respective target file
		   Return 	: return value for key
		'''
		ssh_client = self.ssh_to_server(self.log_server_ip, self.user, self.pwd)		
		sftp_client = ssh_client.open_sftp()
		logging.info("Auto_logger:reading logs from "+self.log_path+'/'+self.tc_name+'_'+target+'.log' )
		remote_file = sftp_client.open(self.log_path+'/'+self.tc_name+'_'+target+'.log')
		mat = []
		try:
    			for line in remote_file:
       				if key in line:
					logging.info("Auto_logger:line:"+line)
					mat.append(line)
			return mat
		finally:
    			remote_file.close()		


	################################################################################################

	def get_header_from_method(self, header, target, method):
		'''
		   Description	: This function read fetched header line from aparticular method.
		   Argument	: header to be fetched
		   Argument	: target [origin(caller)/destination(callee)] 
		   Argument	: method [INVITE, 100 Trying, 180 Ringing, 200 OK-INVITE, ACK, BYE, 200 OK-BYE]
		   Return 	: Complete message
		'''
		message = self.extract_SIP_method_from_logfile(target, method)
		try:
			value = re.search(header + '.*', message, re.MULTILINE)
			return value.group()
		except:
			logging.error("Header not found in method...")
			return ""


	################################################################################################

	def extract_SIP_method_from_logfile(self, target, method):
		'''
		   Description	: This function read log file and return values for particular key.
		   Argument	: target [origin(caller)/destination(callee)] 
		   Argument	: method [INVITE, 100 Trying, 180 Ringing, 200 OK-INVITE, ACK, BYE, 200 OK-BYE]
		   Return 	: Complete message
		'''
		ssh_client = self.ssh_to_server(self.log_server, self.user, self.pwd)
		#ssh_client = self.ssh_to_server('10.66.13.64','root','!hello123')
		try:		
			sftp_client = ssh_client.open_sftp()
			logging.info("Auto_logger: Reading logs from " + self.log_path + '/' + self.tc_name + '_' + target + '.log')
			remote_file = sftp_client.open(self.log_path + '/' + self.tc_name + '_' + target + '.log')
			#remote_file = sftp_client.open('/tmp/Automation_logs/TC_3994.log/TC_3994_origin.log')
		except Exception as e :
       			exc_type, exc_obj, exc_tb = sys.exc_info()
       			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        		logging.error("Auto_Logger: Reading log file failed. Exception : %s %s %s %s"% (e, exc_type, fname, str(exc_tb.tb_lineno)))
			sys.exit(1)

		if method == 'INVITE' or method == 'ACK':
			method += ' sip:'
		elif method == '200 OK-INVITE' or method == '200 OK-BYE':
			method_type =  method.split('-')[1]
			method = 'SIP/2.0 ' + method.split('-')[0]

		flag = 0
		message = ""
		if "200 OK" in method:
			msg_list = []
	    		for line in remote_file:
	       			if method in line:
					#logging.info(line)
					message += line
					flag = 1
				else:
					if flag == 1:				
						message += line
						if ' send ' in line or ' recv ' in line:
							#logging.info("stopping capture")
							msg_list.append(message)
							message = ""
							flag = 0
			remote_file.close()
			for msg in msg_list:
				#logging.info(msg)
				exact = re.search('CSeq: [0-9]{1,10} %s' % method_type, msg, re.DOTALL) 
				try:
					logging.info(exact.group())
					logging.info(msg)
					return msg
				except:
					logging.info('Checking next 200 OK message...')	
						
		else:
	    		for line in remote_file:
	       			if method in line:
					#logging.info(line)
					message += line
					flag = 1
				else:
					if flag == 1:				
						message += line
						if ' send ' in line or ' recv ' in line:
							#logging.info("stopping capture")
							remote_file.close()
							logging.info(message)
							return message			
		remote_file.close()
		#logging.info(message)
		return message		


	################################################################################################

	def start_core_logging(self, spn_list, node):
		'''
		   Description	: This function starts logging on Sawmill server.
		   Arguments 	: SPN list, Node under test
		   Returns	: None
		'''
		logging.info('Auto_Logger: Starting log capture...')
		#self.admin_server, self.pro_server = TestBedHealthCheckup.get_server_details()			
		self.spn_list = spn_list
		self.src_spn = spn_list[0]
		try:
			self.dest_spn = spn_list[1]
		except:
			self.dest_spn = "xxxx"
		logging.info("Auto_Logger: Fetching logs for SPN List : %s" % spn_list)
		self.node = node
		chan_sm = self.login_to_sawmill_server()

		# fetching date on sawmill server
		chan_sm.send('echo `date +%Y%m%d`' + '\n')
		time.sleep(1)
		resp = chan_sm.recv(9999)
		timestamp = re.search('[0-9].*', resp).group().strip()
		#logging.info(timestamp)	
		self.sm_log_file = '/tmp/' + self.tc_name + '_' + str(timestamp) + '.log'

		# execute tail command to capture the sawmil log
		self.thread1 = threading.Thread(target = self.sawmill_log_thread, args = (chan_sm, str(timestamp)))
		self.thread1.start()
		time.sleep(5)
		self.thread1.join()
		chan_sm.send('ps -ef | grep tail | grep -v grep' + '\n')
		time.sleep(3)
		resp = chan_sm.recv(9999)
		logging.info('Response : ' + resp)		
		logging.info('Auto_Logger: Started sawmill log capture for test case : %s' % self.tc_name)



	################################################################################################

	def sawmill_log_thread(self, channel, timestamp):		
		channel.send("pkill tail; cd /logs/%s; nohup tail -f ./*%s.log |  egrep '%s|%s' > %s &" % (self.node, timestamp, self.src_spn, self.dest_spn, self.sm_log_file) + '\n')
		#channel.send("cd /logs/%s; nohup tail -f ./*%s.log > %s &" % (self.node, timestamp, self.sm_log_file) + '\n') 
 		#resp = channel.recv(9999)
		#logging.info('Response : ' + resp)



	################################################################################################

	def login_to_sawmill_server(self):
		'''
		   Description	: This function logs in to sawmill server.
		   Arguments 	: None
		   Returns	: ssh channel handle
		'''
		self.sawmill_ip = '10.66.13.76'
		self.sawmill_user = 'dilip'
		self.sawmill_pwd = 'X8r$kH4C'
		self.ssh = self.ssh_to_server(self.admin_ip, self.user, self.pwd)
		chan_sm = self.ssh.invoke_shell()	
		try:
			ssh_command = 'ssh ' + self.sawmill_user + '@' + self.sawmill_ip
			logging.info('Auto_Logger: Sending command : %s' % ssh_command)
			chan_sm.send(ssh_command + '\n')                                   
			buff = ''
			while not buff.endswith('assword: '):
    				resp = chan_sm.recv(9999)
    				buff += resp
			chan_sm.send(self.sawmill_pwd + '\n')                                   
			buff = ''
			while not buff.endswith('$ '):
    				resp = chan_sm.recv(9999)
    				buff += resp
			logging.info('Auto_Logger: Successfully logged in to Sawmill server!')
			return chan_sm
		except Exception as e :
        		exc_type, exc_obj, exc_tb = sys.exc_info()
        		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        		logging.error("Auto_Logger: Unable to ssh to sawmill server. Exception : %s %s %s %s"% (e, exc_type, fname, str(exc_tb.tb_lineno)))
			sys.exit(1)		


	################################################################################################

	def stop_core_logging(self):
		'''
		   Description	: This function stops logging on Sawmill server.
		   Arguments 	: None
		   Returns	: None
		'''
		logging.info('Auto_Logger: Stopping logs on Sawmill server...')
		chan_sm = self.login_to_sawmill_server()
		counter = 1
		while counter < 3:
			chan_sm.send('ps -ef | grep tail | grep -v grep' + '\n')
			time.sleep(1)
			resp = chan_sm.recv(9999)
			logging.info(resp)
			try:
				pid = re.search('%s.*[0-9]{2,6}' % self.sawmill_user, str(resp))
				logging.info("Auto_Logger: PID to kill is " + pid.group().split()[1])
				chan_sm.send('kill -9 ' + pid.group().split()[1] + '\n')
			except:
				logging.info('No logger process running on Sawmill!')
				return
			chan_sm.send('ps -ef | grep tail | grep -v grep' + '\n')
			time.sleep(1)
			resp = chan_sm.recv(9999)
			if str(resp).find('-f') > 0:
				counter = counter + 1
			else:
				logging.info("Auto_Logger: Sawmill logger process killed successfully!")
				break
			logging.info("Auto_Logger: Retrying to kill Sawmill logger process...")
		
		success = self.transfer_log_file(chan_sm, self.sm_log_file)
		if success == 0:
			#self.verify_XC_logs(spn)
			logging.info('Sawmill Log file %s transferred successfully to /tmp/ dir of admin server!' % self.sm_log_file)
		else:
			logging.error('Failed to scp logs. Please manually check sawmill logs on server in ' + self.sm_log_file)



	################################################################################################

	def start_thread_sm(self, channel, node):	
		# change the sawmillog path
		if 'cert' in node:
			#node += '-logs'
			samillog_file_path= 'cd /logs/' + node + '-logs'
		else:
			samillog_file_path= 'cd /logs/' + node

		#Final_sawmillog_command = 'cd /logs/cert1-logs;tail '+'-f '+ XCsawmil_logfile + ' > /var/tmp/xc4.log'
		Final_sawmillog_command = 'pkill tail;' + samillog_file_path + '; nohup tail -f ' + self.XCsawmil_logfile + ' > ' + self.sm_log_file + ' &'		
		channel.send(Final_sawmillog_command + '\n' )


	
	################################################################################################

	def start_logging_XC_on_sawmil(self, node, tc_name):
		'''
		   Description	: This function starts logging XC logs on Sawmill server.
		   Arguments 	: None
		   Returns	: None
		'''
		self.admin_server, self.pro_server = TestBedHealthCheckup.get_server_details()
		self.admin_ip = self.admin_server['admin_ip']
		self.user = self.admin_server['server_user']
		self.pwd = self.admin_server['server_pwd']
		self.log_server_ip = self.admin_server['log_server_ip']
		self.pro_server = self.pro_server['provision1_dc1_ip']
		chan_XCsawmil = self.login_to_sawmill_server()
		
		# fetching date on sawmill server
		chan_XCsawmil.send('echo `date +%Y%m%d`' + '\n')
		time.sleep(1)
		resp = chan_XCsawmil.recv(9999)
		timestamp = re.search('[0-9].*', resp).group().strip()
		#logging.info(timestamp)
		
		# Filename for sawmillog
		self.XCsawmil_logfile = 'xc2-' + node + '-' + str(timestamp) + '.log'
		self.sm_log_file = '/tmp/' + tc_name + '_' + str(timestamp) + '.log'

		# execute tail command to capture the sawmil log
		self.thread1 = threading.Thread(target = self.start_thread_sm, args = (chan_XCsawmil, node))
		self.thread1.start()
		time.sleep(5)
		self.thread1.join()
		chan_XCsawmil.send('ps -ef | grep tail | grep -v grep' + '\n')
		time.sleep(3)
		resp = chan_XCsawmil.recv(9999)
		logging.info('Response : ' + resp)		
		logging.info('Auto_Logger: Started sawmill log capture for test case : %s' % tc_name)



if __name__ == "__main__":
	print file_path
