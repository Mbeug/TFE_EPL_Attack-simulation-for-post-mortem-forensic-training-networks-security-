from colorOutput import ColorOutput
from topology_manager import TopologyManager


class AttackerManager:
    """

    """
    def __init__(self,topology_manager:TopologyManager,flag_position:str):
        self.tm = topology_manager
        self.nm = self.tm.nm
        self.dm = self.tm.dm
        self.tm.create_n_node(1,'thomasbeckers/alpine-scapy',flag_position)
        self.attacker_pc = self.get_attacker_pc(self.tm.list_pcs) #must changed if we want more than one attacker

        pass

    def host_discovery(self, ip_dst):
        script = '''
from scapy.all import *

TIMEOUT = 1
conf.verb = 0
for ip in range(0, 256):
    packet = IP(dst="{}" + str(ip), ttl=5)/ICMP()
    reply = sr1(packet, timeout=TIMEOUT)
    if not (reply is None):
         print(reply.src, "is online")
    else:
         print("Timeout waiting for %s" % packet[IP].dst)

        '''

        f = open("./scapy_scripts/host_discovery.py", "w")
        f.write(script.format(ip_dst))
        f.close()

        self.nm.start_node(self.attacker_pc['node_id'])
        self.dm.exec_to_docker(self.attacker_pc["properties"]["container_id"],"mkdir scapy_scripts")
        self.dm.copy_to_docker("./scapy_scripts/host_discovery.py",
                               self.attacker_pc["properties"]["container_id"],
                               "/scapy_scripts/host_discovery.py")
        self.dm.exec_to_docker(self.attacker_pc["properties"]["container_id"],
                               "python3 scapy_scripts/host_discovery.py")
        pass

    def scan_port(self, ip_dst, start_port,end_port):
        script = '''
from scapy.all import *

# Scan port of {0}
ans, unans = sr( IP(dst="{0}")/TCP(flags="S", dport=({1},{2})) )
#ans.summary( lambda sr: r.sprintf("%TCP.sport% \t %TCP.flags%") )

# Show opened ports
print('Ports open')
ans.summary(lfilter = lambda s_r: s_r[1].sprintf("%TCP.flags%") == "SA",prn=lambda s_r:s_r[1].sprintf("%TCP.sport% is open"))


        '''
        f = open("./scapy_scripts/scan_ports.py", "w")
        f.write(script.format(ip_dst,start_port,end_port))
        f.close()

        self.nm.start_node(self.attacker_pc['node_id'])
        self.dm.exec_to_docker(self.attacker_pc["properties"]["container_id"], "mkdir scapy_scripts")
        self.dm.copy_to_docker("./scapy_scripts/scapy_scan_ports.py",
                               self.attacker_pc["properties"]["container_id"],
                               "/scapy_scripts/scapy_scan_ports.py")
        self.dm.exec_to_docker(self.attacker_pc["properties"]["container_id"],
                               "python3 scapy_scripts/scapy_scan_ports.py")
        pass

    def dos(self, ip_src, ip_dst, port):
        script = '''
from scapy.all import *

# Not working
while True:
        send( IP(src="{0}",dst="{1}")/TCP(flags="S", dport=({2})) )
                '''
        f = open("./scapy_scripts/dos.py", "w")
        f.write(script.format(ip_src, ip_dst, port))
        f.close()
        self.nm.start_node(self.attacker_pc['node_id'])
        self.dm.exec_to_docker(self.attacker_pc["properties"]["container_id"], "mkdir scapy_scripts")
        self.dm.copy_to_docker("./scapy_scripts/scapy_dos.py",
                               self.attacker_pc["properties"]["container_id"],
                               "/scapy_scripts/scapy_dos.py")
        self.dm.exec_to_docker(self.attacker_pc["properties"]["container_id"],
                               "python3 scapy_scripts/scapy_dos.py")
        pass

    #TODO: modify to multiple attackers
    def get_attacker_pc(self, list_pcs):
        for pc in list_pcs :

            if 'thomasbeckers/alpine-scapy' in pc['name']:
                return pc
        print(ColorOutput.INFO_TAG +': attacker pc not found')
        return None

    def attacker_config(self):
        self.dm.copy_to_docker("./python_scripts/write_file.py", self.attacker_pc["properties"]["container_id"],
                               "pathoffile")
        pass
