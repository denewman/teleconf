'''
This is the sample client code showing how to call the API to push telemetry configure to the router
Follow the bellow syntax to run this sample code:

python sample_mdt.py [router ip] [user name] [password] [RouterPort] [access protocol] \
		[destination group name] [address family] [destination ip] [remote port] \
		[sensor group name] [sensor path] [subscription name] [subscription ID] [interval]
		
eg:
python sample_mdt.py 192.168.2.3 vagrant vagrant 22 ssh Dgroup1 ipv4 172.30.8.4 5432 SGroup1 \
"Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters" \
Sub1 4 3000
'''

from mdtconf import Mdtconf
import sys

def main(argv):
	RouterId = argv[1]
	Username = argv[2]
	Password = argv[3]
	RouterPort = argv[4]
	AccessProtocol = argv[5]
	DgroupName = argv[6]
	AddFamily = argv[7]
	DestIp = argv[8]
	RmtPort = argv[9]
	SGroupName = argv[10]
	SPath = argv[11]
	SubName = argv[12]
	SubId =argv[13]
	Interval = argv[14]
	
	conf = Mdtconf(RouterId,Username,Password,RouterPort,
		AccessProtocol,DgroupName,AddFamily,DestIp,RmtPort,SGroupName,
		SPath,SubName,SubId,Interval)
	result = conf.push_conf()
if __name__ == '__main__':
    # Connect to the db.
	main(sys.argv)
	