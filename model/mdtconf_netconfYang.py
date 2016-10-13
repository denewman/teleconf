'''
Backend function to configure telemetry (MDT) on Cisco router via Netconf/Yang
using ncclient
Version: 1.0
Change history:
	v1.0	2016-10-13	AA	Implemeted Netconf/Yang telemetry API
	v1.1	2016-10-14	YS	Within configureAll function, changed 
							destianation group ip address from 
							172.16.15.14 to the input valriable 
							self.DestIp
							changed protcol from "grpc" to "tcp"
'''
from ncclient import manager
import re
from subprocess import Popen, PIPE, STDOUT
import sys


class MdtNetconfYang(object):

	OUTPUT = {
	0: 'Operation success!',
	1: 'Authentication fail',
	2: 'SSH fail,could not open socket to router',
	3: 'Unable to connect to router',
	4: 'Configuration failed',
	11: 'Unable to delete configuration'
	}

	def __init__(self, RouterId,Username,Password,RouterPort,
	AccessProtocol,DgroupName,AddFamily,DestIp,RmtPort,SGroupName,
	SPath,SubName,SubId,Interval):
	# '''
	# Input variables:
	#     1, RouteId: Router's ip address or name which is accessible via SSH/Telnet
	#     2, Username: user name for accessing the router
	#     3, Password: password for accessing the router
	#     4, RouterPort: the TCP port of the router which is used for remote access, eg: 22, 830 etc
	#     5, AccessProtocol: ssh or telnet
	#     6, DgroupName: destination group name
	#     7, AddFamily: address family, either ipv4 or ipv6
	#     8, DestIp: IP address of the telemetry receiving host
	#     9, RmtPort: TCP/UDP port of the retelemery receiving host, eg: 5432
	#     10,SGroupName: Sensor group name
	#     11,SPath: sensor path, eg:
	#         Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters
	#		If there are multiple paths, please use ',' (comma) to seperate them
	#     12,SubName: subscription name
	#     13,SubId: subscripton ID
	#     14,Interval: interval of pushing telemetry data, in ms, eg: 30000
	# '''
		self.RouterId = RouterId
		self.Username = Username
		self.Password = Password
		self.RouterPort = RouterPort
		self.AccessProtocol = AccessProtocol
		self.DgroupName = DgroupName
		self.AddFamily = AddFamily
		self.DestIp = DestIp
		self.RmtPort = RmtPort
		self.SGroupName = SGroupName
		self.SPath = SPath
		self.SubName = SubName
		self.SubId = SubId
		self.Interval = Interval

	def access_router(self):

		xr = 0
		returncode = 0
		try:
			xr = manager.connect(
			host = self.RouterId,
			username = self.Username,
			password = self.Password,
			port = self.RouterPort,
			allow_agent=False,
	    	look_for_keys=False,
	    	hostkey_verify=False,
	    	unknown_host_cb=True
			)

			# xr = ConnectHandler(**xr)
		except NetMikoAuthenticationException:
			returncode = 1
		except SSHException:
			returncode = 2
		except:
			returncode = 3

		return xr,returncode


	def destination(self):

		returncode = 0
		xr , returncode = self.access_router()
		
		try:
			edit_data = '''
			<config>
			<telemetry-model-driven xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-telemetry-model-driven-cfg">
			   <destination-groups>
			    <destination-group>
			     <destination-id>''' + self.DgroupName + '''</destination-id>
			     <destinations>
			      <destination>
			       <address-family>'''+self.AddFamily+'''</address-family>
			       <'''+self.AddFamily+'''>
			        <'''+self.AddFamily+'''-address>''' + self.DestIp + '''</'''+self.AddFamily+'''-address>
			        <destination-port>'''+ self.RmtPort +'''</destination-port>
			        <encoding>self-describing-gpb</encoding>
			        <protocol>
			         <protocol>tcp</protocol>
			         <tls-hostname></tls-hostname>
			         <no-tls>0</no-tls>
			        </protocol>
			       </'''+self.AddFamily+'''>
			      </destination>
			     </destinations>
			    </destination-group>
			   </destination-groups>
			  </telemetry-model-driven>
			</config>
			'''

			xr.edit_config(edit_data, target='candidate', format='xml')
			xr.commit()
		except:
			returncode = 4

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode

	def sensor(self):

		returncode = 0
		xr , returncode = self.access_router()

		try:
			edit_data = '''
			<config>
			<telemetry-model-driven xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-telemetry-model-driven-cfg">
			   <sensor-groups>
			    <sensor-group>
			     <sensor-group-identifier>'''+ self.SGroupName +'''</sensor-group-identifier>
			     <sensor-paths>
			      <sensor-path>
			       <telemetry-sensor-path>'''+ self.SPath+'''</telemetry-sensor-path>
			      </sensor-path>
			     </sensor-paths>
			    </sensor-group>
			   </sensor-groups>
			  </telemetry-model-driven>
			</config>
			'''

			xr.edit_config(edit_data, target='candidate', format='xml')
			xr.commit()

		except:

			returncode = 4

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode


	def subscription(self):

		returncode = 0
		xr , returncode = self.access_router()

		try:
			edit_data = '''
		      <config>
		      <telemetry-model-driven xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-telemetry-model-driven-cfg">
		            <subscriptions>
		             <subscription>
		              <subscription-identifier>'''+ self.SubName + self.SubId+'''</subscription-identifier>
		              <sensor-profiles>
		               <sensor-profile>
		                <sensorgroupid>'''+ self.SGroupName +'''</sensorgroupid>
		                <sample-interval>'''+ self.Interval +'''</sample-interval>
		               </sensor-profile>
		              </sensor-profiles>
		              <destination-profiles>
		               <destination-profile>
		                <destination-id>'''+ self.DgroupName+'''</destination-id>
		                <enable></enable>
		               </destination-profile>
		              </destination-profiles>
		             </subscription>
		            </subscriptions>
		      </telemetry-model-driven>
		      </config>
		      '''
			xr.edit_config(edit_data, target='candidate', format='xml')
			xr.commit()
		except:
			returncode = 4

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode


	def configureAll(self):


		returncode = 0
		xr , returncode = self.access_router()

		try:
			edit_data = '''
		      <config>
			    <telemetry-model-driven xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-telemetry-model-driven-cfg">
				   <destination-groups>
				    <destination-group>
				     <destination-id>'''+self.DgroupName+'''</destination-id>
				     <destinations>
				      <destination>
				       <address-family>'''+self.AddFamily+'''</address-family>
				       <'''+self.AddFamily+'''>
						<'''+self.AddFamily+'''-address>''' + self.DestIp + '''</'''+self.AddFamily+'''-address>
				        <destination-port>'''+self.RmtPort+'''</destination-port>
				        <encoding>self-describing-gpb</encoding>
				        <protocol>
				         <protocol>tcp</protocol>
				         <tls-hostname></tls-hostname>
				         <no-tls>0</no-tls>
				        </protocol>
				       </'''+self.AddFamily+'''>
				      </destination>
				     </destinations>
				    </destination-group>
				   </destination-groups>
				   <sensor-groups>
				    <sensor-group>
				     <sensor-group-identifier>'''+self.SGroupName+'''</sensor-group-identifier>
				     <sensor-paths>
				      <sensor-path>
				       <telemetry-sensor-path>'''+self.SPath+'''</telemetry-sensor-path>
				      </sensor-path>
				     </sensor-paths>
				    </sensor-group>
				   </sensor-groups>
				   <subscriptions>
				    <subscription>
				     <subscription-identifier>'''+self.SubName +self.SubId+'''</subscription-identifier>
				     <sensor-profiles>
				      <sensor-profile>
				       <sensorgroupid>'''+self.SGroupName+'''</sensorgroupid>
				       <sample-interval>'''+self.Interval+'''</sample-interval>
				      </sensor-profile>
				     </sensor-profiles>
				     <destination-profiles>
				      <destination-profile>
				       <destination-id>'''+self.DgroupName+'''</destination-id>
				       <enable></enable>
				      </destination-profile>
				     </destination-profiles>
				    </subscription>
				   </subscriptions>
				  </telemetry-model-driven>
		      </config>
		      '''
			xr.edit_config(edit_data, target='candidate', format='xml')
			xr.commit()
		except:
			returncode = 4

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode

	def deleteSensor(self):

		# remove the nc:operation="remove" from sensor-group to only delete a sensor path no a sensor group
		returncode = 0
		xr , returncode = self.access_router()

		try:
			edit_data = '''
			  <config>
			  <telemetry-model-driven xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-telemetry-model-driven-cfg">
			     <sensor-groups>
			      <sensor-group nc:operation="remove">
			       <sensor-group-identifier>'''+self.SGroupName+'''</sensor-group-identifier>
			       <enable></enable>
			       <sensor-paths>
			        <sensor-path nc:operation="remove">
			         <telemetry-sensor-path >'''+self.SPath+'''</telemetry-sensor-path>
			        </sensor-path>
			       </sensor-paths>
			      </sensor-group>
			     </sensor-groups>
			    </telemetry-model-driven>
			    </config>
		      '''
			xr.edit_config(edit_data, target='candidate', format='xml')
			xr.commit()
		except:
			returncode = 4

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode


	def deleteDestination(self):

		returncode = 0
		xr , returncode = self.access_router()

		try:
			edit_data = '''
			  <config>
			  <telemetry-model-driven xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-telemetry-model-driven-cfg">
			    <destination-groups>
			      <destination-group nc:operation="remove">
			       <destination-id>'''+self.DgroupName+'''</destination-id>
			       <destinations>
			        <destination >
			         <address-family>'''+self.AddFamily+'''</address-family>
			         <'''+self.AddFamily+''' nc:operation="delete">
			          <'''+self.AddFamily+'''-address>'''+self.DestIp+'''</'''+self.AddFamily+'''-address>
			          <destination-port>'''+self.RmtPort+'''</destination-port>
			          <encoding>self-describing-gpb</encoding>
			          <protocol>
			           <protocol>tcp</protocol>
			           <tls-hostname></tls-hostname>
			           <no-tls>0</no-tls>
			          </protocol>
			         </'''+self.AddFamily+'''>
			        </destination>
			       </destinations>
			      </destination-group>
			     </destination-groups>
			     </telemetry-model-driven>
			     </config>
		      '''
			xr.edit_config(edit_data, target='candidate', format='xml')
			xr.commit()
		except:
			returncode = 4

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode



	def deleteSub(self):


		returncode = 0
		xr , returncode = self.access_router()

		try:
			edit_data = '''
		      <config>
		      <telemetry-model-driven xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-telemetry-model-driven-cfg">
		            <subscriptions>
		             <subscription nc:operation="remove">
		              <subscription-identifier>'''+ self.SubName + self.SubId+'''</subscription-identifier>
		              <sensor-profiles>
		               <sensor-profile>
		                <sensorgroupid>'''+ self.SGroupName +'''</sensorgroupid>
		                <sample-interval>'''+ self.Interval +'''</sample-interval>
		               </sensor-profile>
		              </sensor-profiles>
		              <destination-profiles>
		               <destination-profile>
		                <destination-id>'''+ self.DgroupName+'''</destination-id>
		                <enable></enable>
		               </destination-profile>
		              </destination-profiles>
		             </subscription>
		            </subscriptions>
		      </telemetry-model-driven>
		      </config>
		      '''
			xr.edit_config(edit_data, target='candidate', format='xml')
			xr.commit()
		except:
			returncode = 4

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode

	def deleteMDTconfig(self):

		returncode = 0
		xr , returncode = self.access_router()

		try:
			edit_data = '''
		      <config>
			    <telemetry-model-driven xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-telemetry-model-driven-cfg">
				   <destination-groups>
				    <destination-group nc:operation="remove">
				     <destination-id>'''+self.DgroupName+'''</destination-id>
				     <destinations>
				      <destination>
				       <address-family>'''+self.AddFamily+'''</address-family>
				       <'''+self.AddFamily+'''>
				        <'''+self.AddFamily+'''-address>172.16.15.14</'''+self.AddFamily+'''-address>
				        <destination-port>'''+self.RmtPort+'''</destination-port>
				        <encoding>self-describing-gpb</encoding>
				        <protocol>
				         <protocol>grpc</protocol>
				         <tls-hostname></tls-hostname>
				         <no-tls>0</no-tls>
				        </protocol>
				       </'''+self.AddFamily+'''>
				      </destination>
				     </destinations>
				    </destination-group>
				   </destination-groups>
				   <sensor-groups>
				    <sensor-group nc:operation="remove">
				     <sensor-group-identifier>'''+self.SGroupName+'''</sensor-group-identifier>
				     <sensor-paths>
				      <sensor-path>
				       <telemetry-sensor-path>'''+self.SPath+'''</telemetry-sensor-path>
				      </sensor-path>
				     </sensor-paths>
				    </sensor-group>
				   </sensor-groups>
				   <subscriptions>
				    <subscription nc:operation="remove">
				     <subscription-identifier>'''+self.SubName +self.SubId+'''</subscription-identifier>
				     <sensor-profiles>
				      <sensor-profile>
				       <sensorgroupid>'''+self.SGroupName+'''</sensorgroupid>
				       <sample-interval>'''+self.Interval+'''</sample-interval>
				      </sensor-profile>
				     </sensor-profiles>
				     <destination-profiles>
				      <destination-profile>
				       <destination-id>'''+self.DgroupName+'''</destination-id>
				       <enable></enable>
				      </destination-profile>
				     </destination-profiles>
				    </subscription>
				   </subscriptions>
				  </telemetry-model-driven>
		      </config>
		      '''
			xr.edit_config(edit_data, target='candidate', format='xml')
			xr.commit()
		except:
			returncode = 4

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode
