# teleconf

Introduction:
	This is the API for pushing/removing telemetry configuration on Cisco IOS XR router
	
Files:
	model/mdtconf.py	The actual API for model driven telemetry configuration 
	model/pdtconf.py	The actual API for policy driven telemetry configuration
	model/sample_mdt.py	This is the sample client code showing how to call the MDT API (via YANG/Netconf)
	model/call_pdtconf.py This is the sample client code showing how to call the PDT API (via SSH/SCP) 

MDT API specification:

	Input variables:
		1: RouteId: Router's ip address or name which is accessible via SSH/Telnet
		2: Username: user name for accessing the router
		3: Password: password for accessing the router
		4: RouterPort: the TCP port of the router which is used for remote access, eg: 22, 830 etc
		5: AccessProtocol: ssh or telnet 
		6: DgroupName: destination group name
		7: AddFamily: address family, either ipv4 or ipv6
		8: DestIp: IP address of the telemetry receiving host
		9: RmtPort: TCP/UDP port of the retelemery receiving host, eg: 5432
		10:SGroupName: Sensor group name
		11:SPath: sensor path, eg: 
			Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters
		12:SubName: subscription name
		13:SubId: subscripton ID
		14:Interval: interval of pushing telemetry data, in ms, eg: 30000
	
	Return values:
		0: Operation success
		1: Authentication fail, eg: wrong user name or password
		2: SSH fail,could not open socket to router, eg: specify the wrong ssh port 
		3: unable to connect to router, eg: any other reason of failed to access the router
		4: Configuration failed, eg: router refuses to take the configuration due to invalid values
		11: Unable to delete configuration

Sample code of calling MDT API

	from mdtconf import Mdtconf
	conf = Mdtconf(RouterId,Username,Password,RouterPort,
		AccessProtocol,DgroupName,AddFamily,DestIp,RmtPort,SGroupName,
		SPath,SubName,SubId,Interval)
	
	##push configure##
	result = conf.push_conf()
	
	##delete configure##
	result = conf.del_conf()
	

PDT API specification (via Paramiko SSH/SCP):

	Input variables:
		1: ConfType: either 'push' or 'delete'
		2: RouterId: Router's ip address or name which is accessible via SSH/Telnet
		3: Username: user name for accessing the router
		4: Password: password for accessing the router
		5: RouterPort: the TCP port of the router which is used for remote access, eg: 22, 830 etc
		6: AccessProtocol: ssh or telnet 
		7: PolicyName: the name of the policy, as well as the policy file name (JSON file)
					eg: if the poilcy name is 'Test', the policy file name will
					then be 'Test.json'
		8: PolicyVersion: the value of 'Version' in policy
		9: Description: descriptoin of the policy, use " " to represent no description
		10:Comment: comment of the policy,us " " to represent no comment
		11:Identifier: string to identify the policy
		12:Period: 16-bit unsigned integer, in seconds
		13:Paths: eg, RootOper.InfraStatistics.Interface(*).Latest.GenericCounters
		14:AddFamily: address family, either ipv4 or ipv6
		15:DestIp: IP address of the telemetry receiving host
		16:RmtPort: TCP/UDP port of the tetelemery receiving host, eg: 2103
		17:PolicyGroupName: the name of the policy group
	
	Return values:
		0: Operation success
		1: Authentication fail
		2: SSH fail,could not open socket to router
		3: Unable to connect to router
		4: Configuration failed
		5: Bad host key
		6: Unable to establshi scp session
		7: SCP fail
		8: File copy fail
		9: Unable to move files between directories on router
		11:Unable to delete configuration
		
Sample code of calling PDT API
	
	from pdtconf import Pdtconf
	conf = Pdtconf(ConfType,RouterId,Username,Password,RouterPort,
			AccessProtocol,PolicyName,PolicyVersion,Description,Comment,Identifier,
			Period,Paths,AddFamily,DestIp,RmtPort,PolicyGroupName)
	##push configure##
	result = conf.push_conf()
	
	##delete configure##
	result = conf.del_conf()