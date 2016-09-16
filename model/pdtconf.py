'''
Backend function to configure policy based telemetry (PDT) on Cisco router
Version: 1.0
Change history:
	v1.0	2016-09-09	YS	Created first version
'''

import json
import os
from paramiko import SSHClient,ssh_exception
from scp import SCPClient
import time
import sys

class Pdtconf(object):
	OUTPUT = {
		0: 'Operation success!',
		1: 'Authentication fail',
		2: 'SSH fail,could not open socket to router',
		3: 'Unable to connect to router',
		4: 'Configuration failed',
		5: 'Bad host key',
		6: 'Unable to establshi scp session',
		7: 'SCP fail',
		8: 'File copy fail',
		9: 'Unable to move files between directories on router',
		11: 'Unable to delete configuration'
		}
	TMPDIR = "/tmp"
	HOMEDIR1 = "/disk0:"
	HOMEDIR2 = "/disk0\:"
	TELEDIR = "/telemetry/policies"
	def __init__(self, ConfType,RouterId,Username,Password,RouterPort,
		AccessProtocol,PolicyName,PolicyVersion,Description,Comment,Identifier,
		Period,Paths,AddFamily,DestIp,RmtPort,PolicyGroupName):
		'''
		Input variables:
			1, ConfType: either 'push' or 'delete'
			2, RouterId: Router's ip address or name which is accessible via SSH/Telnet
			3, Username: user name for accessing the router
			4, Password: password for accessing the router
			5, RouterPort: the TCP port of the router which is used for remote access, eg: 22, 830 etc
			6, AccessProtocol: ssh or telnet 
			7, PolicyName: the name of the policy, as well as the policy file name (JSON file)
							eg: if the poilcy name is 'Test', the policy file name will
							then be 'Test.policy'
			8, PolicyVersion: the value of 'Version' in policy
			9, Description: descriptoin of the policy, use " " to represent no description
			10,Comment: comment of the policy,us " " to represent no comment
			11,Identifier: string to identify the policy
			12,Period: 16-bit unsigned integer, in seconds
			13,Paths: eg, RootOper.InfraStatistics.Interface(*).Latest.GenericCounters
			14,AddFamily: address family, either ipv4 or ipv6
			15,DestIp: IP address of the telemetry receiving host
			16,RmtPort: TCP/UDP port of the tetelemery receiving host, eg: 2103
			17,PolicyGroupName: the name of the policy group
		'''
		self.ConfType = ConfType
		self.RouterId = RouterId
		self.Username = Username
		self.Password = Password
		self.RouterPort = RouterPort
		self.AccessProtocol = AccessProtocol
		self.PolicyName = PolicyName
		self.PolicyVersion = PolicyVersion
		self.Description = Description
		self.Comment = Comment
		self.Identifier = Identifier
		self.Period = Period
		self.Paths = Paths
		self.AddFamily = AddFamily
		self.DestIp = DestIp
		self.RmtPort = RmtPort
		self.PolicyGroupName = PolicyGroupName
		'''
		Generate path list in case there are more than one paths provided.
		Assume comma (,) is used as seperator of paths.
		'''
		PathList = []
		split = ","
		PathList = Paths.split(split)
		self.PathList = PathList
		
	def access_router(self):
		ssh = SSHClient()
		ssh.load_system_host_keys()
		scp = 0
		returncode = 0
		'''
		Try ssh first, if fail, then return
		'''
		try:
			ssh.connect(self.RouterId,username=self.Username,
				password=self.Password,port=int(self.RouterPort))
		except ssh_exception.AuthenticationException:
			returncode = 1
		except ssh_exception.BadHostKeyException:
			returncode = 5
		except:
			returncode = 3		

		if returncode > 0:
			return ssh,scp,returncode		

		'''
		Try scp if ssh success
		'''
		try:
			scp = SCPClient(ssh.get_transport())
		except:
			returncode = 6
			return ssh,scp,returncode
			
		return ssh,scp,returncode
	
	def push_conf(self):
		'''
		Procedures to configure the policy based telemetry on Cisco router:
			Step 1, create json object contains the policy configuration
			Step 2, upload json file to router via SCP
			Step 3, configure policy on router via CLI command
		'''
		returncode = 0
		'''
		Create json object and file contains the policy configuration 
		'''
		json_file = self.TMPDIR+"/"+self.PolicyName+".policy"
		json_file_name = self.PolicyName+".policy"
		print "\n"+"creating json object......"+"\n"
		data = {"Name":self.PolicyName,
				"Metadata": {
					"Version": self.PolicyVersion,
					"Description": self.Description,
					"Comment": self.Comment,
					"Identifier": self.Identifier
				},
				"CollectionGroups": {
					"FirstGroup": {
						"Period": self.Period,
						"Paths": [
							self.PathList
						]
					}
				}
				}		
		json_data = json.dumps(data,indent=4)
		fh = open (json_file,'w')
		for line in json_data:
			fh.write(line)
		fh.close()
		
		'''
		Upload json file to router via SCP
		'''
		print "uploading policy file "+json_file+" to router "+self.RouterId+"......\n"
		ssh,scp,returncode = self.access_router()
		if returncode > 0:
			print "\n"+self.OUTPUT.get(returncode)+"\n"
			return returncode

		remotefile1 = self.HOMEDIR1+"/"+json_file_name
		remotefile2 = self.HOMEDIR2+"/"+json_file_name
		remotefile3 = self.TELEDIR+"/"+json_file_name
		copycmd = "cp "+remotefile2+" "+self.TELEDIR+"/.\r\n"
		delcmd = "rm "+remotefile2+"\r\n"		
		try:
			scp.put(json_file,remotefile1)	
		except:
			returncode = 7
		
		'''
		Close and re-open ssh/scp session, this is due to the socket closing after SCP uploading
		TODO: need to find a better solution to avoid closing/re-openning session
		'''
		print "closing and re-openning ssh session......"+"\n"
		scp.close
		ssh.close
		ssh,scp,returncode = self.access_router()
		if returncode > 0:
			print "\n"+self.OUTPUT.get(returncode)+"\n"
			return returncode
			
		'''
		Move the policy file to default telemetry directory
		'''
		if returncode == 0:
			print "moving policy file from "+self.HOMEDIR1+" to "+self.TELEDIR+"......\n"	
			try:
				channel = ssh.invoke_shell()			
				sys.stdout.flush()
				time.sleep(3)
				channel.send('run\r\n')
				time.sleep(3)
				channel.send(copycmd)
				channel.send(delcmd)
				channel.send('exit')
				channel.close
			except:
				returncode = 9
		
		
		'''
		Configure router via CLI command
		'''
		if returncode == 0:
			print "configuring policy on router......"
			
			try:
				channel2 = ssh.invoke_shell()			
				sys.stdout.flush()
				time.sleep(3)
				channel2.send('conf t\r\n')
				channel2.send('telemetry\r\n')
				channel2.send('encoder json\r\n')
				cmd = "policy group "+self.PolicyGroupName+"\r\n"
				channel2.send(cmd)
				cmd = "policy "+self.PolicyName+"\r\n"
				channel2.send(cmd)
				cmd = "destination "+self.AddFamily+" "+str(self.DestIp)+" port "+str(self.RmtPort)+"\r\n"
				channel2.send(cmd)
				channel2.send('commit\r\n')
				time.sleep(2)
				channel2.close				
			except:
				returncode = 4
			
		'''
		Cleanup
		'''
		os.unlink(json_file)
		scp.close
		ssh.close
		
		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode
		
	def del_conf(self):
		'''
		This deletion function has not been implemented yet
		TODO: develop the actual deletion function
		'''
		print "Deletion function is not supported yet"
		returncode = 11
		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode
		
		