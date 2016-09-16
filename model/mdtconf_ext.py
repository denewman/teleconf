from ncclient import manager
import re
from subprocess import Popen, PIPE, STDOUT
import sys

def main(argv):

    RouterId = argv[1]
    Username = argv[2]
    Password = argv[3]
    RouterPort = argv[4]
    SGroupName = argv[5]
    SPath = argv[6]


    xr = manager.connect(
        host= RouterId,
        port= RouterPort,
        username= Username,
        password= Password,
    	allow_agent=False,
    	look_for_keys=False,
    	hostkey_verify=False,
    	unknown_host_cb=True)



    edit_data = '''
    <config>
    <telemetry-system xmlns="http://openconfig.net/yang/telemetry">
       <sensor-groups>
        <sensor-group>
         <sensor-group-id>''' + SGroupName +'''</sensor-group-id>
         <sensor-paths>
          <sensor-path>
           <config>
            <path>''' + SPath + '''</path>
           </config>
          </sensor-path>
         </sensor-paths>
        </sensor-group>
       </sensor-groups>
    </config>
    '''

    xr.edit_config(edit_data, target='candidate', format='xml')
    xr.commit()

    filter = '''<telemetry-system xmlns="http://openconfig.net/yang/telemetry">'''

    c = xr.get_config(source='running', filter=('subtree', filter))
    # print the configuration for testing purposes
    #print(c)

if __name__ == '__main__':
    # Connect to the db.

    # will connect to the db to find whether the subscription group name is existed or not
    # hard coded for testing
    # you cant change SGroup3 to any existing group name that has been created by the mdtconf API
    if sys.argv[5]=='SGroup3':
        main(sys.argv)
    else:
        print sys.argv[5] + ' is not existed \nUse another  subscription group name'
