# teleconf

Introduction:

	This is the API for pushing/removing telemetry configuration on Cisco IOS XR router
	
	
Files:

	Model Driven Telemery (MDT)
		API via Yang/Netconf          
			model/mdtconf.py
			model/mdtconf_ext.py (extension 1)
			model/sample_mdt.py (sample client code)
											
		API via SSH (Netmiko)      
			model/mdtconf_ssh.py (extension 2)
			
		
	Policy Driven Telemetry (PDT)
		API via SSH/SCP (Paramiko) 
			model/pdtconf.py
			model/call_pdtconf.py (sample client code)

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
	

PDT API specification:

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


Example of using "sample_mdt.py" to call MDT API

	syntax of running "sample_mdt.py":
		python sample_mdt.py [ConfigType] [router ip] [user name] [password] [RouterPort] [access protocol] \
		[destination group name] [address family] [destination ip] [remote port] \
		[sensor group name] [sensor path] [subscription name] [subscription ID] [interval]
		
	eg:
		For pushing configuration to the router:

		python sample_mdt.py push  192.168.2.3 vagrant vagrant 22 ssh Dgroup1 ipv4 172.30.8.4 5432 SGroup1 \
		"Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters" \
		Sub1 4 3000

		For deleting configuration from the router:
		
		python sample_mdt.py delete  192.168.2.3 vagrant vagrant 22 ssh Dgroup1 ipv4 172.30.8.4 5432 SGroup1 \
		"Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters" \
		Sub1 4 3000

Example of using "call_pdtconf.py" to call PDT API
	
	Sytax of running "call_pdtconf.py":
	
	Usage: call_pdtconf.py [options]

	Options:
		-h, --help            show this help message and exit
		--n=ROUTERID          mandatory,router ip or name which is accessable
		--u=USERNAME          mandatory,user name to access the router
		--p=PASSWORD          mandatory,password to access the router
		--pn=POLICYNAME       mandatory,policy name, this value will also been used
				              as the policy file name.
				              eg: if the poilcy name is 'Test', the policy file name
                              will then be 'Test.json'
		--pp=PATHS            mandatory,paths used by the policy.
				              eg: RootOper.InfraStatistics.Interface(*).Latest.GenericCounters
		--dst=DESTIP          mandatory,IP address of the telemetry receiving host
		--pg=POLICYGROUPNAME  mandatory,the name of the policy group
		--c=CONFTYPE          optional,Configuration type, either 'push' or
				              'delete',default is 'push'
		--rp=ROUTERPORT       optional,the TCP port which is used for remote
				              access to router, default is 22
		--m=ACCESSPROTOCOL    optional,access protocol, telnet or ssh, default is
				              ssh
		--pv=POLICYVERSION    optional,policy version, default value is 1
		--pd=DESCRIPTION      optional,policy description, default value is empty
		--pc=COMMENT          optional,policy comment,default value is empty
		--pi=IDENTIFIER       optional,policy identifier, default value is empty
		--pe=PERIOD           optional,policy period, in seconds, default value is 30
		--af=ADDFAMILY        optional,address family, either ipv4 or ipv6, default
				              value is ipv4
		--dp=RMTPORT          optional,TCP/UDP port of the tetelemery receiving
			 	              host, default is 2103
	
	eg:
	python call_pdtconf.py --n=64.104.255.10 --rp=5000 --u=vagrant --p=vagrant --pn=Test --pp="aa,bb,cc" \
	--dst=172.32.1.1 --pg=testgroup12

MDT API extention 1 code: model/mdtconf_ext.py

	This configuration is an extension of MDT API. 
	This code is a Configuring Model-Driven Telemetry (MDT) with OpenConfig
	YANG OpenConfig YANG that uses a netconf client. 
	This configuration extends the capability of MDT API for supporting
	multi path within the same subscription group.
	
	The extension API takes six arguments.
        1 - RouterId (Router IP address)
        2 - Username (Router username)
        3 - password (Router Password)
        4 - RouterPort (Router Port number)
        5 - SGroupName (Subscription group name)
        6 - SPath (Subscription path)


	To run the script:
        python mdtconf_ext.py RouterId Username password RouterPort SGroupName SPath

	Ex.:
        python mdtconf_ext.py 192.168.2.3 vagrant vagrant 22 SGroup4 CiscoWorld:arp/nodes/node/entries/entry
		
MDT API extention 2 code: model/mdtconf_ssh.py
	
	This API is model driven implementation to router using Netmiko (SSH)

	This API has 11 arguments and 4 functions
	
	1- Command : This argument is used to choose the configuration type
						 ex;
						 1- newConfig : To have a new configuration with new Destination Group, Sensor Group and Subscription
						 2- subscription: To only create a new subscription
						 3- destination: To only create a new destination group
						 4- sensor: To only create a new sensor group
	
	2- RouterId : The router IP address
	3- Username : The router username
	4- Password : The router password
	5- RouterPort : The router port number
	6- DgroupName : Destination Group Name
	7- DIPAddress : Destination IPv4 address
	8- DgroupPort : Destination port number
	9- SenorGroupName : Sensor Group Name
	10- SensorPath : Sensor path
	11- SubName : Subscription Name
	12- interval : Streaming interval
	
	Funtions are:-

	configureAll(): To invoke:
					python mdtconf_ssh.py  newConfig RouterId Username Password RouterPort DgroupName \
					DIPAddress  DgroupPort SenorGroupName SensorPath SubName interval

					Ex:
					python mdtconf_ssh.py  newConfig  192.168.2.3 vagrant vagrant 22 Dgroup1 172.16.18.5 5001 \
					SGroup1 sgroup1/ciscorouter/com Sub1 3000


	subscription():To invoke:
					python mdtconf_ssh.py  subscription RouterId Username Password RouterPort DgroupName \
					SubName SenorGroupName interval

					Ex:
					python mdtconf_ssh.py  subscription  192.168.2.3 vagrant vagrant 22 Dgroup1 Sub2  \
					SGroup1  3000


	destination(): To invoke:

					python mdtconf_ssh.py  destination RouterId Username Password RouterPort DgroupName \
					DIPAddress DgroupPort
					
					Ex:
					python mdtconf_ssh.py  destination  192.168.2.3 vagrant vagrant 22 Dgroup2 \
					192.168.4.3  7872


	sensor(): 		To invoke:
					python mdtconf_ssh.py  sensor RouterId Username Password RouterPort SenorGroupName SensorPath


					Ex:
					python mdtconf_ssh.py  sensor  192.168.2.3 vagrant vagrant 22 SGroup2 \
					Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters
	