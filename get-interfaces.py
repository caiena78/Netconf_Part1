mport sys
from argparse import ArgumentParser
from ncclient import manager

import xml.dom.minidom


data='''
<filter>
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface/>
</native>
</filter>
'''

if __name__ == '__main__':

    parser = ArgumentParser(description='Select options.')

    # Input parameters
    parser.add_argument('--host', type=str, required=True,
                        help='The device IP or DN. Required')
    parser.add_argument('-u', '--username', type=str, required=True,
                        help='Username on the device. Required')
    parser.add_argument('-p', '--password', type=str, required=True,
                        help='Password for the username. Required')
    parser.add_argument('--port', type=int, default=830,
                        help='Specify this if you want a non-default port. Default: 830')

    args = parser.parse_args()

    m = manager.connect(host=args.host,
                        port=args.port,
                        username=args.username,
                        password=args.password,
                        device_params={'name':'csr'})

     m.timeout = 120

    reply = m.get(data)
    # Pretty print the XML reply
    xmlDom = xml.dom.minidom.parseString(str(reply))
    print(xmlDom.toprettyxml(indent='  '))
