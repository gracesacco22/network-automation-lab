from ncclient import manager
from ncclient.xml_ import to_ele
import logging
import time
import threading

logging.basicConfig(level=logging.DEBUG)

rpc1 = """
<cli xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"><mode>EXEC</mode><cmdline>copy tftp://admin:CXlabs.123@10.225.244.88/nxos64-cs.10.5.1.F.bin bootflash:nxos64-cs.10.5.1.F.bin vrf management use-kstack </cmdline></cli>
"""

rpc2 = """
<cli xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"><mode>EXEC</mode><cmdline>install all nxos bootflash:nxos64-cs.10.5.1.F.bin.bin non-disruptive</cmdline></cli>
"""

def initial_call():
    with manager.connect(host="", port="830", timeout=1200, username="admin", password="Cisco123", hostkey_verify=False, device_params={"name":"nexus"}) as conn:
        rpcreply1 = conn.dispatch(to_ele(rpc1))
        return(rpcreply1)

def check_for_file():
    with manager.connect(host="", port="830", timeout=60, username="admin", password="Cisco123", hostkey_verify=False, device_params={"name": "nexus"}) as conn2:
        rpcreply2 = conn2.dispatch(to_ele(rpc2))
        return(rpcreply2)

if __name__ == '__main__':
    first = threading.Thread(target=initial_call)
    second = threading.Thread(target=check_for_file)
    first.start()
    second.start()
