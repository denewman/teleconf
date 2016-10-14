'''
Backend function to configure telemetry (MDT) on Cisco router via YDK
Version: 1.3
Change history:
	v1.0	2016-08-24	YS	Created first version
	v1.1	2016-08-25	YS	Enhanced exception handling
	v1.2   	2016-08-26  AA  Added MDT confgiuration deleting function
	v1.3	2016-09-25	YS	Support multiple sensors
	v1.4	2016-09-28	YS	Added Destination group configure
	v1.5	2016-09-30	YS	Added encoding and protocol values
							when configuring Destination group
	v1.6	2016-10-10	YS	Added deletion function to delte only
							sensor or subscription
	v2.0	2016-10-14	YS	Use cisco XR native schema to configure
							encoding and protocol within destination 
							group
'''
from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService 
import ydk.models.openconfig.openconfig_telemetry as oc_telemetry 
import ydk.models.cisco_ios_xr.Cisco_IOS_XR_telemetry_model_driven_cfg as xr_telemetry
from ydk.services import CRUDService
from ncclient.transport.errors import AuthenticationError,SSHError

class Mdtconf(object):
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
		'''
		Input variables:
			1, RouteId: Router's ip address or name which is accessible via SSH/Telnet
			2, Username: user name for accessing the router
			3, Password: password for accessing the router
			4, RouterPort: the TCP port of the router which is used for remote access, eg: 22, 830 etc
			5, AccessProtocol: ssh or telnet 
			6, DgroupName: destination group name
			7, AddFamily: address family, either ipv4 or ipv6
			8, DestIp: IP address of the telemetry receiving host
			9, RmtPort: TCP/UDP port of the retelemery receiving host, eg: 5432
			10,SGroupName: Sensor group name
			11,SPath: sensor path, eg: 
				Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters
			   If there are multiple paths, please use ',' (comma) to seperate them
			12,SubName: subscription name
			13,SubId: subscripton ID
			14,Interval: interval of pushing telemetry data, in ms, eg: 30000
		'''
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
			xr = NetconfServiceProvider(
				address = self.RouterId,
				port = self.RouterPort,
				username = self.Username,
				password = self.Password,
				protocol = self.AccessProtocol)
		except AuthenticationError:
			returncode = 1
		except SSHError:
			returncode = 2
		except:
			returncode = 3	
		
		return xr,returncode
	
	
				
	def push_conf(self):
		returncode = 0
		xr,returncode = self.access_router()
		if returncode > 0:
			print "\n"+self.OUTPUT.get(returncode)+"\n"
			return returncode
		
		try:
			sgroup = oc_telemetry.TelemetrySystem.SensorGroups.SensorGroup()
			sgroup.sensor_group_id = self.SGroupName
			sgroup.config.sensor_group_id = self.SGroupName
			sgroup.sensor_paths = sgroup.SensorPaths()		
			
			split = ","
			PathList = self.SPath.split(split)
			for path in PathList:
				new_sensorpath = sgroup.SensorPaths.SensorPath()
				new_sensorpath.path = path
				new_sensorpath.config.path = path
				sgroup.sensor_paths.sensor_path.append(new_sensorpath)
		
			rpc_service = CRUDService()
			rpc_service.create(xr, sgroup)
			sub = oc_telemetry.TelemetrySystem.Subscriptions.Persistent.Subscription()
			sub.subscription_id = long(self.SubId)
			sub.config.subscription_id = long(self.SubId)
		
			sub.sensor_profiles = sub.SensorProfiles()
			new_sgroup = sub.SensorProfiles.SensorProfile()
			new_sgroup.sensor_group = self.SGroupName
			new_sgroup.config.sensor_group = self.SGroupName
			new_sgroup.config.sample_interval = long(self.Interval)

			sub.sensor_profiles.sensor_profile.append(new_sgroup)
	
			rpc_service.create(xr, sub)
			
			
			dgroup = xr_telemetry.TelemetryModelDriven.DestinationGroups.DestinationGroup()
			dgroup.destination_id = self.DgroupName
			dgroup.destinations = dgroup.Destinations()
			
			new_destination = dgroup.Destinations.Destination()
			new_destination.address_family = xr_telemetry.AfEnum.IPV4
			
			new_ipv4=xr_telemetry.TelemetryModelDriven.DestinationGroups.DestinationGroup().Destinations().Destination().Ipv4()
			new_ipv4.destination_port = int(self.RmtPort)
			new_ipv4.ipv4_address = self.DestIp
			
			new_ipv4.encoding = xr_telemetry.EncodeTypeEnum.SELF_DESCRIBING_GPB
			new_ipv4.protocol = xr_telemetry.TelemetryModelDriven.DestinationGroups.DestinationGroup().Destinations().Destination().Ipv4().Protocol()
			new_ipv4.protocol.protocol = xr_telemetry.ProtoTypeEnum.TCP
			new_destination.ipv4.append(new_ipv4)
			
			dgroup.destinations.destination.append(new_destination)
			rpc_service.create(xr, dgroup)
			

		except:
			returncode = 4
		xr.close()
	
		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode
		
	def del_conf(self):
		'''
		This function is duplicate to deleteMDTConfig()
		'''
		returncode = 0
		xr,returncode = self.access_router()

		if returncode > 0:
			print "\n"+self.OUTPUT.get(returncode)+"\n"
			return returncode

		try:
			rpc_service = CRUDService()
			rpc_service.delete(xr, oc_telemetry.TelemetrySystem())
		except:
			returncode = 11
		xr.close()

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode
		
	def deleteMDTconfig(self):
		'''
		Delete all MDT configure
		'''
		returncode = 0
		xr,returncode = self.access_router()

		if returncode > 0:
			print "\n"+self.OUTPUT.get(returncode)+"\n"
			return returncode

		try:
			rpc_service = CRUDService()
			rpc_service.delete(xr, oc_telemetry.TelemetrySystem())
		except:
			returncode = 11
		xr.close()

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode
		
	def deleteSub(self):
		'''
		Delete subscription only
		'''
		returncode = 0
		xr,returncode = self.access_router()

		if returncode > 0:
			print "\n"+self.OUTPUT.get(returncode)+"\n"
			return returncode
		
		try:
			rpc_service = CRUDService()
			sub = oc_telemetry.TelemetrySystem.Subscriptions.Persistent.Subscription()
			sub.subscription_id = long(self.SubId)
			sub.config.subscription_id = long(self.SubId)
			rpc_service.delete(xr, sub)			
		except:
			returncode = 11
		
		xr.close()

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode
	
	def deleteSensor(self):
		'''
		Delete sensor group only
		'''
		returncode = 0
		xr,returncode = self.access_router()

		if returncode > 0:
			print "\n"+self.OUTPUT.get(returncode)+"\n"
			return returncode
		
		try:
			rpc_service = CRUDService()
			sgroup = oc_telemetry.TelemetrySystem.SensorGroups.SensorGroup()
			sgroup.sensor_group_id = self.SGroupName
			sgroup.config.sensor_group_id = self.SGroupName
			rpc_service.delete(xr, sgroup)			
		except:
			returncode = 11
		
		xr.close()

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode
	
	def deleteDestination(self):
		'''
		Delete desntination group only
		'''
		returncode = 0
		xr,returncode = self.access_router()

		if returncode > 0:
			print "\n"+self.OUTPUT.get(returncode)+"\n"
			return returncode
		
		try:
			rpc_service = CRUDService()
			dgroup = xr_telemetry.TelemetryModelDriven.DestinationGroups.DestinationGroup()
			dgroup.destination_id = self.DgroupName
			
			'''
			dgroup = oc_telemetry.TelemetrySystem.DestinationGroups.DestinationGroup()
			dgroup.group_id = self.DgroupName
			dgroup.config.group_id = self.DgroupName
			'''
			rpc_service.delete(xr, dgroup)			
		except:
			returncode = 11
		
		xr.close()

		print "\n"+self.OUTPUT.get(returncode)+"\n"
		return returncode