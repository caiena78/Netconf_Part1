
import lxml.etree as ET
from argparse import ArgumentParser
from ncclient import manager
from ncclient.operations import RPCError

payload = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>1/0/9</name>
            <description>Netconf Trunk Port</description>           
            <!--This will cause an RPC error if the interface is not shutdown -->
            <shutdown xc:operation="delete"/>            
           <switchport>
            <mode xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
              <trunk/>
            </mode>
            <trunk xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
              <allowed>
                <vlan>
                  <vlans>100,200</vlans>
                </vlan>
              </allowed>
            </trunk>
          </switchport>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
"""

if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')

    # script arguments
    parser.add_argument('-a', '--host', type=str, required=True,
                        help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str, required=True,
                        help="Device Username (netconf agent username)")
    parser.add_argument('-p', '--password', type=str, required=True,
                        help="Device Password (netconf agent password)")
    parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")
    args = parser.parse_args()

    # connect to netconf agent
    with manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         timeout=90,
                         hostkey_verify=False,
                         device_params={'name': 'csr'}) as m:

        # execute netconf operation
        try:
            data  = m.edit_config(target='running', config=payload).xml
        except RPCError as e:
            data = e._raw
        print(data)

