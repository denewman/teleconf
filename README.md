# teleconf

Introduction:
	This is the API for pushing/removing telemetry configuration on Cisco IOS XR router
	
Files:
	model/mdtconf.py	The actual API for model driven telemetry configuration  
	model/sample_mdt.py	This is the sample client code showing how to call the API 

API specification:
	Input:
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
	
	Return values:
		0: Operation success
		1: Authentication fail, eg: wrong user name or password
		2: SSH fail,could not open socket to router, eg: specify the wrong ssh port 
		3: unable to connect to router, eg: any other reason of failed to access the router
		4: Configuration failed, eg: router refuses to take the configuration due to invalid values
		11: Unable to delete configuration

Example of using "sample_mdt.py" to call the API

	syntax of running "sample_mdt.py":
		python sample_mdt.py [router ip] [user name] [password] [RouterPort] [access protocol] \
		[destination group name] [address family] [destination ip] [remote port] \
		[sensor group name] [sensor path] [subscription name] [subscription ID] [interval]
		
	eg:
		python sample_mdt.py 192.168.2.3 vagrant vagrant 22 ssh Dgroup1 ipv4 172.30.8.4 5432 SGroup1 \
		"Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters" \
		Sub1 4 3000
