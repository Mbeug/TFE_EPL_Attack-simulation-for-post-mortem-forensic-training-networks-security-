import threading
import time

from color_output import ColorOutput
from topology_manager import TopologyManager

from utility import Utility


class AttackerManager:
    """
    Class to manage attackers in the network. This class calls some methods of the :py:class:`docker_manager` class
    """

    def __init__(self, topology_manager: TopologyManager):
        self.tm = topology_manager
        self.nm = self.tm.nm
        self.dm = self.tm.dm
        self.list_attackers = self.get_attackers(self.tm.list_pcs)
        self.threads_list =[]
        pass

    def create_attackers(self, nb_attackers, flag_position):
        """
        Method creating nb_attackers at the flag_position

        :param nb_attackers: The number of attackers we want to create
        :param flag_position: The position( 'out' or 'in_service' or 'in_lan') where we want to put attackers
        :return: Add to the list of attackers the new attackers

        """
        self.tm.create_n_node(nb_attackers, 'thomasbeckers/alpine-scapy', flag_position)
        list_pcs = self.tm.list_pcs
        list_services = self.tm.list_services
        list = list_pcs + list_services
        self.list_attackers=self.get_attackers(list)


        print(ColorOutput.INFO_TAG+": {0} attacker(s) added at the position '{1}'.".format(nb_attackers,flag_position))
        pass

    def host_discovery(self, attacker_pc, ip_dst, start_range, end_range):
        """
        This method launch the host discovery with some parameters

        :param attacker_pc: which attacker launch this attack
        :param ip_dst: The mask of the ip address
        :param start_range: The number of the port on which the discovery is to begin
        :param end_range: The number of the port on which the discovery is to be completed
        :return: Write in the out_discovery_host.txt the result of the execution

        .. note:: The file is stored in out directory
        """
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
        f.write(script.format(ip_dst, start_range, end_range))
        f.close()

        self.nm.start_node(attacker_pc['node_id'])
        self.dm.exec_to_docker(attacker_pc["properties"]["container_id"], "mkdir scapy_scripts")
        self.dm.copy_to_docker("./scapy_scripts/host_discovery.py",
                               attacker_pc["properties"]["container_id"],
                               "/scapy_scripts/host_discovery.py")
        time.sleep(4)
        res = self.dm.exec_to_docker(attacker_pc["properties"]["container_id"],
                                     "python3 scapy_scripts/host_discovery.py")
        print(ColorOutput.INFO_TAG + ": result of the host discovery is in the txt file in the out directory")
        Utility.print_in_file(str(res[1].decode('utf-8')), "out_discovery_host.txt")
        pass

    def scan_port(self, attacker_pc, ip_dst, start_port, end_port):
        """
        This method launch a scan of ports on the pc at a specific ip address with the pc attacker.

        :param attacker_pc: The pc attacker
        :param ip_dst: The target of the scan
        :param start_port: The starting port number
        :param end_port: The ending port number
        :return: Write in the out_scan_ports.txt the result of the execution
        """
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
        f.write(script.format(ip_dst, start_port, end_port))
        f.close()

        self.nm.start_node(attacker_pc['node_id'])
        self.dm.exec_to_docker(attacker_pc["properties"]["container_id"], "mkdir scapy_scripts")
        self.dm.copy_to_docker("./scapy_scripts/scan_ports.py",
                               attacker_pc["properties"]["container_id"],
                               "/scapy_scripts/scan_ports.py")
        time.sleep(4)
        res = self.dm.exec_to_docker(attacker_pc["properties"]["container_id"],
                                     "python3 scapy_scripts/scan_ports.py")
        print("\n" + ColorOutput.INFO_TAG + ": result of the scan ports is in the out directory")
        Utility.print_in_file(str(res[1].decode('utf-8')), "out_scan_ports.txt")
        pass

    def dos(self, attacker_pc, ip_src, ip_dst, port):
        """
        This method launch a Dos attack, it represents the execution of what a bot in a botnet could do.

        :param attacker_pc: The bot
        :param ip_src: The ip bot
        :param ip_dst: The target of the attack
        :param port: The port number
        :return: Write in the out_dos_attack.txt the result of the execution
        """
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
        time.sleep(4)
        res = self.dm.exec_to_docker(attacker_pc["properties"]["container_id"],
                                     "python3 scapy_scripts/dos.py")
        print(ColorOutput.INFO_TAG + ": result of the dos is in the out directory")
        Utility.print_in_file(str(res[1].decode('utf-8')), "out_dos_attack.txt")
        pass

    @staticmethod
    def get_attackers(list_pcs):
        """
        This method allows you to have the list of attackers.

        :param list_pcs: The list of pcs present in the topology
        :return: the list of all attackers present in the topology
        """
        list_attackers = []
        for pc in list_pcs:
            if 'thomasbeckers/alpine-scapy' in pc['name']:
                list_attackers.append(pc)
        return list_attackers

    def attacker_config(self):
        """
        This method configure attackers pcs

        """
        for attacker in self.list_attackers:
            self.dm.copy_to_docker("./python_scripts/write_file.py", attacker["properties"]["container_id"],
                                   "pathoffile")
        pass

    def dns_tunneling(self):
        """
        This method launch a dns tunneling
        """
        self.tm.create_n_node(1, 'thomasbeckers/iodine', 'out')
        self.tm.create_n_node(1, 'thomasbeckers/iodine', 'in_lan')
        list_machines = self.tm.get_pc_nodes('thomasbeckers/iodine')
        server = list_machines[0]
        client = list_machines[1]
        self.nm.start_node(server['node_id'])
        self.nm.start_node(client['node_id'])
        self.dm.exec_to_docker(server["properties"]["container_id"], "iodined -f 172.16.0.1 test.com -P uclouvain",
                               True)
        time.sleep(4)
        self.dm.exec_to_docker(client["properties"]["container_id"],
                               "iodine -f -r 192.168.122.30 test.com -P uclouvain", True)



    def launch_attack_host_discovery(self, param):
        """
        This method launch a thread with the host discovery attack

        :param param: It's necessary parameters for the :py:meth:`~self.host_discovery` method

        """
        thread_host = threading.Thread(name="Thread host discovering out", target=self.host_discovery, args=param)
        thread_host.start()
        self.threads_list.append(thread_host)
        pass

    def launch_attack_scan_ports(self, param):
        """
        This method launch a thread with the scan ports attack

        :param param: It's necessary parameters for the :py:meth:`~self.scan_port` method

        """
        thread_scan_port = threading.Thread(name="Thread Scan port inner", target=self.scan_port,args=param)
        thread_scan_port.start()
        self.threads_list.append(thread_scan_port)
        pass

    def launch_attack_dos(self, param):
        """
        This method launch a thread with the dos attack

        :param param: It's necessary parameters for the :py:meth:`~self.dos` method

        """
        thread_dos = threading.Thread(name="Thread Dos attack out", target=self.dos,args=param)
        thread_dos.start()
        self.threads_list.append(thread_dos)
        pass

    def stop_threads_attacks(self):
        """
        This method join all thread launched
        """
        print(ColorOutput.INFO_TAG + ": Waiting threads for attacks processes ...")
        for thread in self.threads_list:
            print(ColorOutput.INFO_TAG + ": We are waiting end of "+ thread.getName())
            thread.join()
            print(ColorOutput.INFO_TAG+ ": is closed")