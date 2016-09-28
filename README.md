# teleconf

Introduction:

	This is the API for pushing/removing telemetry configuration on Cisco IOS XR router
	
Files:

	Model Driven Telemetry (MDT)
		API via Yang/Netconf          
			model/mdtconf_netconf.py 	(not complete yet)
		
		API via YDK
			model/mdtconf_ydk.py
			model/call_mdtconf_ydk.py (sample client code)
			
		API via SSH (Netmiko)      
			model/mdtconf_ssh.py 
			model/call_mdtconf_ssh.py (sample client code)
		
	Policy Driven Telemetry (PDT)
		API via SSH/SCP (Paramiko) 
			model/pdtconf.py
			model/call_pdtconf.py (sample client code)

MDT API specification (for all implementations: YDK, SSH, Netconf/Yang):

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

Sample code of calling MDT API (YDK)

	from mdtconf_ydk import Mdtconf
	conf = Mdtconf(RouterId,Username,Password,RouterPort,
		AccessProtocol,DgroupName,AddFamily,DestIp,RmtPort,SGroupName,
		SPath,SubName,SubId,Interval)
	
	##push configure##
	result = conf.push_conf()
	
	##delete configure##
	result = conf.del_conf()
	
Sample code of calling MDT API (SSH)

	from mdtconf_ssh import MdtSSHconf
	conf = MdtSSHconf(RouterId,Username,Password,RouterPort,
		AccessProtocol,DgroupName,AddFamily,DestIp,RmtPort,SGroupName,
		SPath,SubName,SubId,Interval)
	
	##push all configuration##
	result = conf.configureAll()
	
	##push subscription configuration only##
	result = conf.subscription()
	
	##push sesor configuration only##
	result = conf.sensor()
	
	##push destination group configuration only##
	result = conf.destination()
	
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
	           then be 'Test.policy'
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
		
Sample code of calling PDT API (SSH/SCP)
	
	from pdtconf import Pdtconf
	conf = Pdtconf(ConfType,RouterId,Username,Password,RouterPort,
			AccessProtocol,PolicyName,PolicyVersion,Description,Comment,Identifier,
			Period,Paths,AddFamily,DestIp,RmtPort,PolicyGroupName)
	##push configure##
	result = conf.push_conf()
	
	##delete configure##
	result = conf.del_conf()


Example of using "call_mdtconf_ydk.py" to call MDT API (YDK)

	python call_mdtconf_ydk.py [ConfigType] [router ip] [user name] [password] [RouterPort] [access protocol] \
		[destination group name] [address family] [destination ip] [remote port] \
		[sensor group name] [sensor path] [subscription name] [subscription ID] [interval]
		
	eg:
	Pushing configuration
	python call_mdtconf_ydk.py push 192.168.2.3 vagrant vagrant 22 ssh Dgroup1 ipv4 172.30.8.4 5432 SGroup1 \
	"Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters" \
	Sub1 4 3000

	Deleting configuration:
	python call_mdtconf_ydk.py delete 192.168.2.3 vagrant vagrant 22 ssh Dgroup1 ipv4 172.30.8.4 5432 SGroup1 \
	"Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters" \
	Sub1 4 3000

Example of using "call_mdtconf_ssh.py" to call MDT API (SSH)
	python call_mdtconf_ssh.py [ConfigType] [router ip] [user name] [password] [RouterPort] [access protocol] \
		[destination group name] [address family] [destination ip] [remote port] \
		[sensor group name] [sensor path] [subscription name] [subscription ID] [interval]

	eg:
	Pushing all configuration
	python call_mdtconf_ssh.py configAll 192.168.2.3 vagrant vagrant 22 ssh Dgroup1 ipv4 172.30.8.4 5432 SGroup1 \
	"Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters" \
	Sub1 4 3000

	Adding subscription only:
	python call_mdtconf_ssh.py sub 192.168.2.3 vagrant vagrant 22 ssh Dgroup1 ipv4 172.30.8.4 5432 SGroup1 \
	"Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters" \
	Sub1 4 3000

	Adding destination only:
	python call_mdtconf_ssh.py dest 192.168.2.3 vagrant vagrant 22 ssh Dgroup1 ipv4 172.30.8.4 5432 SGroup1 \
	"Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters" \
	Sub1 4 3000

	Adding sensor path only:
	python call_mdtconf_ssh.py sensor 192.168.2.3 vagrant vagrant 22 ssh Dgroup1 ipv4 172.30.8.4 5432 SGroup1 \
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

