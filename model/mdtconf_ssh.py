'''
Backend function to configure telemetry (MDT) on Cisco router via SSH
Version: 1.1
Change history:
	v1.0	2016-09-27	AA	Created first version
	v1.1	2016-09-28	YS	Support multiple sensors
'''

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import sys


class MdtSSHconf(object):

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
            xr = {
                'device_type': 'cisco_xr',
                'ip':  self.RouterId ,
                'username': self.Username,
                'password': self.Password,
                'port' : self.RouterPort,          # optional, defaults to 22
                'secret': '',     # optional, defaults to ''
                'verbose': False,       # optional, defaults to False
            }

            xr = ConnectHandler(**xr)
        except NetMikoAuthenticationException:
               returncode = 1
        except SSHException:
               returncode = 2
        except:
               returncode = 3

        return xr,returncode


    def configureAll(self):

       returncode = 0
       xr , returncode = self.access_router()

       try:
           create_destination_group = [ 'telemetry model-driven',
           'destination-group ' + self.DgroupName,
           'address family '+ self.AddFamily +" "+ self.DestIp +' port ' + self.RmtPort,
           'encoding self-describing-gpb',
           'protocol tcp',
           'commit' ]

           output = xr.send_config_set(create_destination_group)
        #    print(output)
	   split = ","
	   PathList = self.SPath.split(split)

           create_sensor_group = [ 'telemetry model-driven',
                               'sensor-group ' + self.SGroupName ]
	   for path in PathList:
		create_sensor_group.append('sensor-path '+ path)
		print "path is "+path
		
	   create_sensor_group.append('commit')

           output = xr.send_config_set(create_sensor_group)
        #    print(output)

           # Create a subscription

           create_subscription = [ 'telemetry model-driven',
                               'subscription ' + self.SubName + self.SubId,
                               'sensor-group-id '+ self.SGroupName +' sample-interval ' + self.Interval,
                               'destination-id ' + self.DgroupName,
                               'commit' ]

           output = xr.send_config_set(create_subscription)
        #    print(output)


        #    output = xr.send_command('show running-config telemetry model-driven')
        #    print(output)

       except:
           returncode = 4

       print "\n"+self.OUTPUT.get(returncode)+"\n"
       return returncode




    def destination(self):

        returncode = 0
        xr,returncode = self.access_router()

        try:

           create_destination_group = [ 'telemetry model-driven',
               'destination-group ' + self.DgroupName,
               'address family '+ self.AddFamily +" "+ self.DestIp +' port ' + self.RmtPort,
               'encoding self-describing-gpb',
               'protocol tcp',
               'commit' ]

           output = xr.send_config_set(create_destination_group)
        #    print(output)




        except:
           returncode = 4

        print "\n"+self.OUTPUT.get(returncode)+"\n"
        return returncode





    def subscription(self):

        returncode = 0
        xr,returncode = self.access_router()

        try:

            create_subscription = [ 'telemetry model-driven',
                                'subscription ' + self.SubName + self.SubId,
                                'sensor-group-id '+ self.SGroupName +' sample-interval ' + self.Interval,
                                'destination-id ' + self.DgroupName,
                                'commit' ]


            output = xr.send_config_set(create_subscription)
            # print(output)




        except:
            returncode = 4

        print "\n"+self.OUTPUT.get(returncode)+"\n"
        return returncode


    def sensor(self):

        returncode = 0
        xr,returncode = self.access_router()

        try:

           create_sensor_group = [ 'telemetry model-driven',
                               'sensor-group ' + self.SGroupName,
                               'sensor-path  '+ self.SPath ,
                               'commit' ]

           output = xr.send_config_set(create_sensor_group)
        #    print(output)




        except:
           returncode = 4

        print "\n"+self.OUTPUT.get(returncode)+"\n"
        return returncode
