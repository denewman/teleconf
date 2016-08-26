'''
This is the sample client code showing how to call the API to push telemetry configure to the router
Follow the bellow syntax to run this sample code:

python sample_mdt.py [ConfigType] [router ip] [user name] [password] [RouterPort] [access protocol] \
		[destination group name] [address family] [destination ip] [remote port] \
		[sensor group name] [sensor path] [subscription name] [subscription ID] [interval]
		
eg:
Pushing configuration
python sample_mdt.py push 192.168.2.3 vagrant vagrant 22 ssh Dgroup1 ipv4 172.30.8.4 5432 SGroup1 \
"Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters" \
Sub1 4 3000

Deleting configuration:
python sample_mdt.py push 192.168.2.3 vagrant vagrant 22 ssh Dgroup1 ipv4 172.30.8.4 5432 SGroup1 \
"Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters" \
Sub1 4 3000
'''

from mdtconf import Mdtconf
import sys

def main(argv):

	ConfigType = argv[1]
	RouterId = argv[2]
	Username = argv[3]
	Password = argv[4]
	RouterPort = argv[5]
	AccessProtocol = argv[6]
	DgroupName = argv[7]
	AddFamily = argv[8]
	DestIp = argv[9]
	RmtPort = argv[10]
	SGroupName = argv[11]
	SPath = argv[12]
	SubName = argv[13]
	SubId =argv[14]
	Interval = argv[15]
	
	
	conf = Mdtconf(RouterId,Username,Password,RouterPort,
		AccessProtocol,DgroupName,AddFamily,DestIp,RmtPort,SGroupName,
		SPath,SubName,SubId,Interval)
	
	if ConfigType == "push":
		result = conf.push_conf()
	elif ConfigType == "delete":
		result = conf.del_conf()
	
if __name__ == '__main__':
    # Connect to the db.
	main(sys.argv)
	