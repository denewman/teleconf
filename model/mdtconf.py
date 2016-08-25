'''
Backend function to configure telemetry (MDT) on Cisco router
Still working in progress
'''
from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService 
import ydk.models.openconfig.openconfig_telemetry as oc_telemetry 
from ydk.services import CRUDService

class Mdtconf(object):
	OUTPUT = {
		0: 'Operation success!',
		1: 'Wrong user name/password',
		2: 'Unable to connect to router',
		3: 'Configuration failed',
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
		
		xr = NetconfServiceProvider(
			address = self.RouterId,
			port = self.RouterPort,
			username = self.Username,
			password = self.Password,
			protocol = self.AccessProtocol)
		return xr
		'''
		print "test access router "+self.RouterId
		return "finish"
		'''
	def push_conf(self):
		returncode = 0
		xr = self.access_router()
		
		sgroup = oc_telemetry.TelemetrySystem.SensorGroups.SensorGroup()
		sgroup.sensor_group_id = self.SGroupName
		sgroup.config.sensor_group_id = self.SGroupName
		sgroup.sensor_paths = sgroup.SensorPaths()
		new_sensorpath = sgroup.SensorPaths.SensorPath()
		new_sensorpath.path = self.SPath
		new_sensorpath.config.path = self.SPath
		
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

		xr.close()
		
		print self.OUTPUT.get(returncode)
		return returncode
		
	def del_conf(self):
		returncode = 0
		xr = self.access_router()
		'''
		TODO: 
			develop the function for deleting the MDT confgiuration
		'''
		return returncode
		
	
		