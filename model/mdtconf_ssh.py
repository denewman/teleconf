#!/usr/bin/python

from netmiko import ConnectHandler
import sys

#arguments
#python mdtssh.py  newConfig  192.168.2.3 vagrant vagrant 22 Dgroup1 172.16.18.5 5001 SGroup1 sgroup1/ciscorouter/com Sub1 3000
def configureAll(argv,cisco_xrv):

    # RouterId = argv[1]
    # Username = argv[2]
    # Password = argv[3]
    # RouterPort = argv[4]
    DgroupName = argv[6]
    DIPAddress = argv[7]
    DgroupPort = argv[8]
    SenorGroupName = argv[9]
    SensorPath = argv[10]
    SubName = argv[11]
    interval = argv[12]

    net_connect = ConnectHandler(**cisco_xrv)


    # Create a destination-group
    create_destination_group = [ 'telemetry model-driven',
                        'destination-group ' + DgroupName,
                        'address family ipv4 '+ DIPAddress +' port ' + DgroupPort,
                        'encoding self-describing-gpb',
                        'protocol tcp',
                        'commit' ]

    output = net_connect.send_config_set(create_destination_group)
    #print(output)

    #  Create a sensor-group

    create_sensor_group = [ 'telemetry model-driven',
                        'sensor-group ' + SenorGroupName,
                        'sensor-path  '+ SensorPath ,
                        'commit' ]

    output = net_connect.send_config_set(create_sensor_group)
    # print(output)

    # Create a subscription

    create_subscription = [ 'telemetry model-driven',
                        'subscription ' + SubName,
                        'sensor-group-id '+ SenorGroupName +' sample-interval ' + interval,
                        'destination-id ' + DgroupName,
                        'commit' ]

    output = net_connect.send_config_set(create_subscription)
    #print(output)


    output = net_connect.send_command('show running-config telemetry model-driven')
    #print(output)

#python mdtssh.py  subscription  192.168.2.3 vagrant vagrant 22 Dgroup1 Sub2  SGroup1  3000

def subscription(argv,cisco_xrv):

    DgroupName = argv[6]
    SubName = argv[7]
    SenorGroupName = argv[8]
    interval = argv[9]



    net_connect = ConnectHandler(**cisco_xrv)


    create_subscription = [ 'telemetry model-driven',
                        'subscription ' + SubName,
                        'sensor-group-id '+ SenorGroupName +' sample-interval ' + interval,
                        'destination-id ' + DgroupName,
                        'commit' ]

    output = net_connect.send_config_set(create_subscription)
    # print(output)


    output = net_connect.send_command('show running-config telemetry model-driven')
    #print(output)


#python mdtssh.py  destination  192.168.2.3 vagrant vagrant 22 Dgroup2 192.168.4.3  7872

def destination(argv,cisco_xrv):

    DgroupName = argv[6]
    DIPAddress = argv[7]
    DgroupPort = argv[8]


    net_connect = ConnectHandler(**cisco_xrv)


    create_destination_group = [ 'telemetry model-driven',
                        'destination-group ' + DgroupName,
                        'address family ipv4 '+ DIPAddress +' port ' + DgroupPort,
                        'encoding self-describing-gpb',
                        'protocol tcp',
                        'commit' ]

    output = net_connect.send_config_set(create_destination_group)
    # print(output)


    output = net_connect.send_command('show running-config telemetry model-driven')
    #print(output)

# python mdtssh.py  sensor  192.168.2.3 vagrant vagrant 22 SGroup2 Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters

def sensor(argv,cisco_xrv):

    SenorGroupName = argv[6]
    SensorPath = argv[7]
    net_connect = ConnectHandler(**cisco_xrv)


    create_sensor_group = [ 'telemetry model-driven',
                        'sensor-group ' + SenorGroupName,
                        'sensor-path  '+ SensorPath ,
                        'commit' ]

    output = net_connect.send_config_set(create_sensor_group)
    # print(output)


    output = net_connect.send_command('show running-config telemetry model-driven')
    #print(output)

if __name__=='__main__':

    Command = sys.argv[1]
    RouterId = sys.argv[2]
    Username = sys.argv[3]
    Password = sys.argv[4]
    RouterPort = sys.argv[5]

    cisco_xrv = {
        'device_type': 'cisco_xr',
        'ip':  RouterId ,
        'username': Username,
        'password': Password,
        'port' : RouterPort,          # optional, defaults to 22
        'secret': '',     # optional, defaults to ''
        'verbose': False,       # optional, defaults to False
    }

    if Command =='subscription':
        subscription(sys.argv, cisco_xrv)
    elif Command =='destination':
        destination(sys.argv, cisco_xrv)
    elif Command =='sensor':
        sensor(sys.argv, cisco_xrv)
    elif Command =='newConfig':
        configureAll(sys.argv, cisco_xrv)
