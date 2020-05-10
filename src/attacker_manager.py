import time

from colorOutput import ColorOutput
from topology_manager import TopologyManager


class AttackerManager:
    """

    """
    ASYNC_FLAG = False

    def __init__(self,topology_manager:TopologyManager, nb_attacker:int, flag_position:str):
        self.tm = topology_manager
        self.nm = self.tm.nm
        self.dm = self.tm.dm
        self.create_attackers(nb_attacker,flag_position)
        self.list_attackers = self.get_attackers(self.tm.list_pcs)

        pass

    def create_attackers(self, nb_attackers, flag_position):
        self.tm.create_n_node(nb_attackers, 'thomasbeckers/alpine-scapy', flag_position)
        self.list_attackers = self.get_attackers(self.tm.list_pcs)
        pass
    def host_discovery(self, attacker_pc,ip_dst,start_range,end_range):
        script = '''
from scapy.all import *

TIMEOUT = 1
conf.verb = 0
for ip in range({1}, {2}):
    packet = IP(dst="{0}" + str(ip), ttl=5)/ICMP()
    reply = sr1(packet, timeout=TIMEOUT)
    if not (reply is None):
         print(reply.src, "is online")
    else:
         print("Timeout waiting for %s" % packet[IP].dst)

        '''

        f = open("./scapy_scripts/host_discovery.py", "w")
        f.write(script.format(ip_dst,start_range,end_range))
        f.close()

        self.nm.start_node(attacker_pc['node_id'])
        self.dm.exec_to_docker(attacker_pc["properties"]["container_id"],"mkdir scapy_scripts")
        self.dm.copy_to_docker("./scapy_scripts/host_discovery.py",
                               attacker_pc["properties"]["container_id"],
                               "/scapy_scripts/host_discovery.py")
        res = self.dm.exec_to_docker(attacker_pc["properties"]["container_id"],
                               "python3 scapy_scripts/host_discovery.py",self.ASYNC_FLAG)
        print(ColorOutput.INFO_TAG+": result of the host discovery\n"+str(res[1].decode('utf-8')))
        pass

    def scan_port(self,attacker_pc, ip_dst, start_port,end_port):
        script = '''
from scapy.all import *

# Scan port of {0}
ans, unans = sr( IP(dst="{0}")/TCP(flags="S", dport=({1},{2})) )
#ans.summary( lambda sr: r.sprintf("%TCP.sport% \t %TCP.flags%") )

# Show opened ports
print('Ports open:')
ans.summary(lfilter = lambda s_r: s_r[1].sprintf("%TCP.flags%") == "SA",prn=lambda s_r:s_r[1].sprintf("%TCP.sport% is open"))


        '''
        f = open("./scapy_scripts/scan_ports.py", "w")
        f.write(script.format(ip_dst,start_port,end_port))
        f.close()

        self.nm.start_node(attacker_pc['node_id'])
        self.dm.exec_to_docker(attacker_pc["properties"]["container_id"], "mkdir scapy_scripts")
        self.dm.copy_to_docker("./scapy_scripts/scan_ports.py",
                               attacker_pc["properties"]["container_id"],
                               "/scapy_scripts/scan_ports.py")
        res =self.dm.exec_to_docker(attacker_pc["properties"]["container_id"],
                               "python3 scapy_scripts/scan_ports.py",self.ASYNC_FLAG)
        print(ColorOutput.INFO_TAG + ": result of the scan ports\n" + str(res[1].decode('utf-8')))
        pass

    def dos(self,attacker_pc, ip_src, ip_dst, port):
        script = '''
from scapy.all import *

# Not working
while True:
        send( IP(src="{0}",dst="{1}")/TCP(flags="S", dport=({2})) )
                '''
        f = open("./scapy_scripts/dos.py", "w")
        f.write(script.format(ip_src, ip_dst, port))
        f.close()
        self.nm.start_node(attacker_pc['node_id'])
        self.dm.exec_to_docker(attacker_pc["properties"]["container_id"], "mkdir scapy_scripts")
        self.dm.copy_to_docker("./scapy_scripts/dos.py",
                               attacker_pc["properties"]["container_id"],
                               "/scapy_scripts/dos.py")
        res = self.dm.exec_to_docker(attacker_pc["properties"]["container_id"],
                               "python3 scapy_scripts/dos.py",self.ASYNC_FLAG)
        print(ColorOutput.INFO_TAG + ": result of the dos\n" + str(res[1].decode('utf-8')))
        pass


    def get_attackers(self, list_pcs):
        list_attackers = []
        for pc in list_pcs :
            if 'thomasbeckers/alpine-scapy' in pc['name']:
                list_attackers.append(pc)
        print(ColorOutput.INFO_TAG +': attacker pc not found')
        return list_attackers

    def attacker_config(self):
        for attacker in self.list_attackers:
            self.dm.copy_to_docker("./python_scripts/write_file.py", attacker["properties"]["container_id"],
                               "pathoffile")
        pass

    def dns_tunneling(self):
        self.tm.create_n_node(1, 'thomasbeckers/iodine', 'out')
        self.tm.create_n_node(1, 'thomasbeckers/iodine', 'in_lan')
        list_machines = self.tm.get_pc_nodes('thomasbeckers/iodine')
        server = list_machines[0]
        client = list_machines[1]
        self.nm.start_node(server['node_id'])
        self.nm.start_node(client['node_id'])
        print( self.dm.exec_to_docker(server["properties"]["container_id"], "iodined -f 172.16.0.1 test.com -P uclouvain", True) )
        time.sleep(4)
        print( self.dm.exec_to_docker(client["properties"]["container_id"], "iodine -f -r 192.168.122.30 test.com -P uclouvain", True))