'''
Client code to call the policy driven telemetry configuration API (pdtconf.py)
in order to push or delete the configuration on Cisco router. 

Version: 1.0
Change history
		v1.0	2016-09-13	YS	created first version

Usage: call_pdtconf.py [options]

Options:
  -h, --help          show this help message and exit
  --n=ROUTERID        mandatory,router ip or name which is accessable
  --u=USERNAME        mandatory,user name to access the router
  --p=PASSWORD        mandatory,password to access the router
  --pn=POLICYNAME     mandatory,policy name, this value will also been used as
                      the policy file name.
                      eg: if the poilcy name is 'Test', the policy file name
                      will then be 'Test.json'
  --pp=PATHS          mandatory,paths used by the policy.
                      eg: RootOper.InfraStatistics.Interface(*).Latest.Generic
                      Counters
  --dst=DESTIP        IP address of the telemetry receiving host
  --c=CONFTYPE        optional,Configuration type, either 'push' or 'del',
                      default is 'push'
  --rp=ROUTERPORT     optional,the TCP port which is used for remote
                      access to router, default is 22
  --m=ACCESSPROTOCOL  optional,access protocol, telnet or ssh, default is ssh
  --pv=POLICYVERSION  optional,policy version, default value is 1
  --pd=DESCRIPTION    optional,policy description, default value is empty
  --pc=COMMENT        optional,policy comment,default value is empty
  --pi=IDENTIFIER     optional,policy identifier, default value is empty
  --pe=PERIOD         optional,policy period, in seconds, default value is 30
  --af=ADDFAMILY      optional,address family, either ipv4 or ipv6, default
                      value is ipv4
  --dp=RMTPORT        optional,TCP/UDP port of the tetelemery receiving host,
                      default is 2103

Example:
		python call_pdtconf.py --n=192.168.2.2 --u=vagrant --p=vagrant\
		--pn=Test --pp="RootOper.InfraStatistics.Interface(*).Latest.GenericCounters"\ 
		--dst=172.32.1.1
'''


from optparse import OptionParser
from pdtconf import Pdtconf
import sys

def main(argv):
	ConfType = "push"
	AccessProtocol = "ssh"
	RouterPort = 22
	PolicyVersion = 1
	Description = ""
	Comment = ""
	Identifier = ""
	Period = 30
	AddFamily = "ipv4"
	RmtPort = 2103
	
	RouterId = ""
	Username = ""
	Password = ""
	PolicyName = ""
	Paths = ""
	DestIp = ""
	PolicyGroupName = ""

	parser = OptionParser()
	
	'''
	Mandatory Arguements
	'''
	parser.add_option("--n",dest="RouterId",help="mandatory,router ip or name which is accessable")
	parser.add_option("--u",dest="Username",help="mandatory,user name to access the router")
	parser.add_option("--p",dest="Password",help="mandatory,password to access the router")
	parser.add_option("--pn",dest="PolicyName",help="mandatory,policy name, this value will also been used as\
						the policy file name.\
						eg: if the poilcy name is 'Test', the policy file name will then be 'Test.json'")
	parser.add_option("--pp",dest="Paths",help="mandatory,paths used by the policy.\
						eg: RootOper.InfraStatistics.Interface(*).Latest.GenericCounters")
	parser.add_option("--dst",dest="DestIp",help="mandatory,IP address of the telemetry receiving host")
	parser.add_option("--pg",dest="PolicyGroupName",help="mandatory,the name of the policy group")
	'''
	Optional Arguements
	'''
	parser.add_option("--c",dest="ConfType",help="optional,Configuration type, either 'push' or 'delete',\
						default is 'push'")
	parser.add_option("--rp",dest="RouterPort",help="optional,the TCP port which is used for remote\
						access to router, default is 22")
	parser.add_option("--m",dest="AccessProtocol",\
						help="optional,access protocol, telnet or ssh, default is ssh")
	parser.add_option("--pv",dest="PolicyVersion",\
						help="optional,policy version, default value is 1")
	parser.add_option("--pd",dest="Description",\
						help="optional,policy description, default value is empty")
	parser.add_option("--pc",dest="Comment",\
						help="optional,policy comment,default value is empty")
	parser.add_option("--pi",dest="Identifier",\
						help="optional,policy identifier, default value is empty")
	parser.add_option("--pe",dest="Period",\
						help="optional,policy period, in seconds, default value is 30")
	parser.add_option("--af",dest="AddFamily",\
						help="optional,address family, either ipv4 or ipv6, default value is ipv4")
	parser.add_option("--dp",dest="RmtPort",\
						help="optional,TCP/UDP port of the tetelemery receiving host, default is 2103")
	(options, args) = parser.parse_args()
	
	if options.RouterId:
		RouterId = options.RouterId
	if options.Username:
		Username = options.Username
	if options.Password:
		Password = options.Password
	if options.PolicyName:
		PolicyName = options.PolicyName
	if options.Paths:
		Paths = options.Paths
	if options.ConfType:
		ConfType = options.ConfType
	if options.RouterPort:
		RouterPort = options.RouterPort
	if options.AccessProtocol:
		AccessProtocol = options.AccessProtocol
	if options.PolicyVersion:
		PolicyVersion = options.PolicyVersion
	if options.Description:
		Description = options.Description
	if options.Comment:
		Comment = options.Comment
	if options.Identifier:
		Identifier = options.Identifier
	if options.Period:
		Period = options.Period
	if options.AddFamily:
		AddFamily = options.AddFamily
	if options.RmtPort:
		RmtPort = options.RmtPort
	if options.PolicyGroupName:
		PolicyGroupName = options.PolicyGroupName
	if options.DestIp:
		DestIp = options.DestIp
	
	if RouterId == "" or Username == "" or\
		Password == "" or PolicyName == "" or\
		Paths == "" or PolicyGroupName == "" or\
		DestIp == "":
		print "\n"+"Missing mandatory arguements"+"\n"
		parser.print_help()
		sys.exit()
	
	conf = Pdtconf(ConfType,RouterId,Username,Password,RouterPort,
			AccessProtocol,PolicyName,PolicyVersion,Description,Comment,Identifier,
			Period,Paths,AddFamily,DestIp,RmtPort,PolicyGroupName)
	if ConfType == "push":
		result = conf.push_conf()
	
	
if __name__ == '__main__':
    # Connect to the db.
	main(sys.argv[1:])
