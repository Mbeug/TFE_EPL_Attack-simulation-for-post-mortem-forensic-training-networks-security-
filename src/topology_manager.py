import os
import time

from colorOutput import ColorOutput
from docker_manager import DockerManager
from network_manager import NetworkManager
from node import Node


class TopologyManager:
    """
    Class to manage the topology of any network we want on the gns3 server
    must be done:
        add n docker
        link to switch (with n interfaces)
        add router
        add server
        add creator netconfig
        manage the position
        add NAT

    """
    def __init__(self,networkmanager=NetworkManager(0,{
                                                        "compute_id": "vm",
                                                        "name": "GNS3 VM (GNS3 VM)"})):
        self.nm = networkmanager
        self.dm = DockerManager(self.nm.selected_machine["compute_id"])
        self.max_x = 700  # That's means we have 7 columns
        #self.max_y = 10000 # That's means we have 100 rows
        self.list_pcs= []
        self.nat = self.create_NAT()
        self.switch_lan = None
        self.switch_services = None
        self.list_services = []
        self.net_config_dhcp = '''# DHCP
                                  auto eth0
                                  iface eth0 inet dhcp
                               '''
        pass


    def set_max_x(self, new_x:int):
        self.max_x = new_x
        pass

    def set_net_config_dhcp(self, new_config):
        self.net_config_dhcp = new_config

    def set_max_y(self, new_y:int):
        self.max_y = new_y
        pass

    def create_n_node(self, n:int, template_name: str = None, docker_name: str = None, docker_img:str =None):
        if template_name == None and docker_img == None:
            print(ColorOutput.ERROR_TAG+': Please fill arg template_name or docker_name with its image')
            exit(1)
        if self.switch_services == None:
            self.switch_services = self.nm.create_template_by_name("Ethernet switch", 450, 100)

        if self.switch_lan == None:
            self.switch_lan = self.nm.create_template_by_name("Ethernet switch",int(3*self.max_x/4), int(n * 100 / 2))
            self.nm.link_nodes(self.switch_services['node_id'],self.switch_lan['node_id'],
                               [0,self.get_switch_port(self.switch_services),self.get_switch_port(self.switch_lan)])
        starting_y = 0
        if len(self.list_pcs) != 0:
            starting_y = int(self.list_pcs[-1]['y'])
        if template_name!= None:
            for i in range(n):
                current_pc = self.nm.create_template_by_name(template_name,self.max_x,starting_y+((i+1)*100))
                self.nm.add_file_to_node(current_pc["node_id"], "/etc/network/interfaces", self.net_config_dhcp)
                self.nm.link_nodes(self.switch_lan['node_id'],current_pc['node_id'],[0,self.get_switch_port(self.switch_lan)],[0,0])
                self.list_pcs.append(current_pc)

        # if docker_name != None and docker_img == None :
        #     print(ColorOutput.ERROR_TAG+': Please give the docker\'s image')
        #     exit(1)
        #
        # if docker_name != None and docker_img != None:
        #     self.nm.create_docker_template(docker_name, docker_img)
        #     for i in range(n):
        #         current_docker = self.nm.create_template_by_name(docker_name, self.max_x, i*100)
        #         self.nm.link_nodes(self.switch_lan['node_id'],current_docker['node_id'],[0,self.get_switch_port(self.switch_lan)],[0,0])
        #         self.list_pcs.append(current_docker)

        pass

    def get_switch_port(self,switch):
        list_ports = []
        for port in switch['properties']['ports_mapping']:
            list_ports.append(port['port_number'])
        last_port = list_ports[-1]

        list_links = self.nm.get_link_node(switch['node_id'])
        for link in list_links:
            for node in link['nodes']:
                if node['node_id']==switch['node_id']:
                    list_ports.remove(node['port_number'])

        if len(list_ports)==0:
            #must add port
            for i in range(last_port+1, 2*last_port):
                switch['properties']['ports_mapping'].append(
                    {'name': 'Ethernet' + str(i), 'port_number': i, 'type': 'access', 'vlan': 1})

            self.nm.put_node(switch['node_id'], {'properties': switch['properties']})
            return last_port+1
        else:
            return list_ports[0]


    def clean(self):
        list_nodes = self.nm.get_all_nodes()
        for node in list_nodes:
            self.nm.delete_node(node['node_id'])

    def create_DNS(self, personal_net_config_dns=None):
        if self.switch_services == None:
            self.switch_services = self.nm.create_template_by_name("Ethernet switch", 450, 100)



        if personal_net_config_dns == None:
            personal_net_config_dns =   """# Static config
                                            auto eth0
                                            iface eth0 inet static
                                                address 192.168.122.10
                                                netmask 255.255.255.0
                                                gateway 192.168.122.1
                                                up echo nameserver 8.8.8.8 > /etc/resolv.conf
                                            auto eth1
                                            iface eth1 inet static
                                                address 10.0.0.1
                                                netmask 255.255.255.0"""

        dns = self.nm.create_template_by_name("thomasbeckers/dns",250,100)
        self.nm.add_file_to_node(dns['node_id'], "/etc/network/interfaces", personal_net_config_dns)

        #linking to switch service
        self.nm.link_nodes(self.nat["node_id"], dns["node_id"], [0,0],[0,0])
        self.nm.link_nodes(dns["node_id"],self.switch_services["node_id"], [1,0], [0,self.get_switch_port(self.switch_services)])
        return dns

    # dns must be started
    def dns_config(self, dns):
        self.nm.start_node(dns["node_id"])
        time.sleep(2)
        self.dm.exec_to_docker(dns['properties']['container_id'], "iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
        self.dm.copy_to_docker("../config_files/dns/dnsmasq.conf", dns["properties"]["container_id"], "/etc/")
        self.dm.copy_to_docker("../config_files/dns/hosts", dns["properties"]["container_id"], "/etc/")
        self.dm.exec_to_docker(dns["properties"]["container_id"], "service dnsmasq restart")
        #time.sleep(2)
        #self.nm.stop_node(dns["node_id"])
        pass

    def create_HTTP(self, personal_net_config_http=None):
        if self.switch_services == None:
            self.switch_services = self.nm.create_template_by_name("Ethernet switch", 450, 100)
            #linking to switch_lan
            self.nm.link_nodes(self.switch_services['node_id'],self.switch_lan['node_id'],
                               [0,self.get_switch_port(self.switch_services)], [0,self.get_switch_port(self.switch_lan)])


        if personal_net_config_http == None:
            personal_net_config_http = '''# Static config
                                            auto eth0
                                            iface eth0 inet static
                                                address 10.0.0.14
                                                netmask 255.255.255.0
                                                gateway 10.0.0.1
                                                up echo nameserver 8.8.8.8 > /etc/resolv.conf'''

        http = self.nm.create_template_by_name("thomasbeckers/http",150,250)
        self.nm.add_file_to_node(http["node_id"],"/etc/network/interfaces",personal_net_config_http)

        #linking to switch services
        self.nm.link_nodes(self.switch_services["node_id"],http['node_id'],[0,self.get_switch_port(self.switch_services)],[0,0])
        self.list_services.append(http)
        return http

    def get_http_nodes(self):
        list_http = []
        for service in self.list_services:
            if 'http' in service['name'] :
                list_http.append(service)

        return list_http

    # http must be started
    def http_config(self, HTTP):
        self.nm.start_node(HTTP['node_id'])
        #todo

        pass

    def create_FTP(self, personal_net_config_ftp=None):
        if self.list_services == None:
            self.switch_services = self.nm.create_template_by_name("Ethernet switch", 450, 100)
            #linking to switch_lan
            self.nm.link_nodes(self.switch_services['node_id'],self.switch_lan['node_id'],
                               [0,self.get_switch_port(self.switch_services)], [0,self.get_switch_port(self.switch_lan)])


        if personal_net_config_ftp == None:
            personal_net_config_ftp =    '''# Static config
                                            auto eth0
                                            iface eth0 inet static
                                                address 10.0.0.15
                                                netmask 255.255.255.0
                                                gateway 10.0.0.1
                                                up echo nameserver 8.8.8.8 > /etc/resolv.conf'''

        ftp =  self.nm.create_template_by_name("thomasbeckers/ftp", 200, 250)
        self.nm.add_file_to_node(ftp['node_id'], "/etc/network/interfaces", personal_net_config_ftp)

        #linking to switch services
        self.nm.link_nodes(self.switch_services['node_id'],ftp["node_id"], [0,self.get_switch_port(self.switch_services)], [0,0])
        self.list_services.append(ftp)

        return ftp

    def get_ftp_nodes(self):
        list_ftp = []
        for service in self.list_services:
            if 'ftp' in service['name']:
                list_ftp.append(service)

        return list_ftp

    # node must be started
    def ftp_config(self, ftp):
        self.nm.start_node(ftp["node_id"])
        time.sleep(2)
        self.dm.copy_to_docker("../config_files/ftp/vsftpd.conf",ftp["properties"]["container_id"],"/etc/vsftpd.conf")
        self.dm.copy_to_docker("../python_scripts/write_file.py",ftp["properties"]["container_id"],"/srv/ftp/write_file.py")
        self.dm.exec_to_docker(ftp["properties"]["container_id"],"chown root:root /etc/vsftpd.conf")
        self.dm.exec_to_docker(ftp["properties"]["container_id"],"service vsftpd restart")
        #time.sleep(2)
        #self.nm.stop_node(ftp["node_id"])
        pass

    def set_net_config_dhcp_on(self, personal_net_config_dhcp):
        self.net_config_dhcp = personal_net_config_dhcp

    def create_NAT(self):
        return  self.nm.create_template_by_name("NAT",100,100)

    def create_MAIL(self, personal_net_config_mail=None):
        if personal_net_config_mail == None:
            personal_net_config_mail = '''# Static config
                                            auto eth0
                                            iface eth0 inet static
                                                address 10.0.0.16
                                                netmask 255.255.255.0
                                                gateway 10.0.0.1
                                                up echo nameserver 8.8.8.8 > /etc/resolv.conf'''

        mail = self.nm.create_template_by_name("thomasbeckers/mail",300,250)
        self.nm.add_file_to_node(mail['node_id'], "/etc/network/interfaces", personal_net_config_mail)

        self.nm.link_nodes(self.switch_services['node_id'], mail["node_id"],
                           [0, self.get_switch_port(self.switch_services)], [0, 0])
        self.list_services.append(mail)