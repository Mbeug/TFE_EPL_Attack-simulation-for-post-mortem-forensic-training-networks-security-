import time

from colorOutput import ColorOutput
from docker_manager import DockerManager
from network_manager import NetworkManager


class TopologyManager:
    """
    Class to manage the topology of any network we want on the gns3 server

    """

    def __init__(self, networkManager=None, haveNat=False):

        if networkManager is None:
            self.nm = NetworkManager()
        else:
            self.nm = networkManager

        self.dm = DockerManager(self.nm.selected_machine["compute_id"])
        self.list_pcs = []
        self.nat = None
        self.flag_have_nat = haveNat
        self.switch_lan = None
        self.switch_services = None
        self.switch_out = None
        self.list_services = []
        self.net_config_dhcp = '''# DHCP
                                  auto eth0
                                  iface eth0 inet dhcp
                               '''

    def set_net_config_dhcp(self, new_config):
        """
        This method set basic net config dhcp
        :param new_config: str

        """
        self.net_config_dhcp = new_config

    pass

    def create_n_node(self, n: int, template_name: str, switch_selected: str = 'in_lan'):
        """
        This method create n pcs (vpcs, vm, docker) link it to one switch (lan_switch)
        :param n: number of pcs
        :param template_name:The name of the template pc
        :param switch_selected: the name of switch where we want create n vpcs
        :return: add to list of pc the n new pcs
        """

        self.check_switch_service()

        if switch_selected == 'in_lan':
            if self.switch_lan is None:
                self.switch_lan = self.nm.create_template_by_name("Ethernet switch", self.switch_services['x'] + 300,
                                                                  self.switch_services['y'])
                self.nm.link_nodes(self.switch_services['node_id'], self.switch_lan['node_id'],
                                   [0, self.get_switch_port(self.switch_services),
                                    self.get_switch_port(self.switch_lan)])
            # add n pc of template name
            for i in range(n):
                current_pc = self.nm.create_template_by_name(template_name, self.switch_lan['x'] + 200,
                                                             self.switch_lan['y'] + (len(self.list_pcs)) * 100)
                self.nm.add_file_to_node(current_pc["node_id"], "/etc/network/interfaces", self.net_config_dhcp)
                self.nm.link_nodes(self.switch_lan['node_id'], current_pc['node_id'],
                                   [0, self.get_switch_port(self.switch_lan)], [0, 0])
                self.list_pcs.append(current_pc)

        elif switch_selected == 'in_service':
            for i in range(n):
                current_pc = self.nm.create_template_by_name(template_name, self.switch_services['x'] + (
                    len(self.list_services)) * 100, self.switch_services['y'] + 200)
                self.nm.add_file_to_node(current_pc["node_id"], "/etc/network/interfaces", self.net_config_dhcp)
                self.nm.link_nodes(self.switch_services['node_id'], current_pc['node_id'],
                                   [0, self.get_switch_port(self.switch_services)], [0, 0])
                self.list_services.append(current_pc)

        elif switch_selected == 'out':
            if self.switch_out is None:
                self.switch_out = self.nm.create_template_by_name("Ethernet switch", 130,
                                                                  100)
            net_config = '''# Static config
                            auto eth0
                            iface eth0 inet static
                                address 192.168.122.30
                                netmask 255.255.255.0
                                gateway 192.168.122.1
                                up echo nameserver 8.8.8.8 > /etc/resolv.conf
            '''
            for i in range(n):
                current_pc = self.nm.create_template_by_name(template_name, self.switch_out['x'],
                                                             self.switch_out['y'] + 200)
                self.nm.add_file_to_node(current_pc["node_id"], "/etc/network/interfaces", net_config)
                self.nm.link_nodes(self.switch_out['node_id'], current_pc['node_id'],
                                   [0, self.get_switch_port(self.switch_out)], [0, 0])
                self.list_pcs.append(current_pc)
        else:
            print(ColorOutput.ERROR_TAG + ": your position of switch flag (" + switch_selected + ") isn't supported!")
            exit(1)
            pass

    def get_switch_port(self, switch):
        """
        Get the first empty port and add some if necessary ports to the specific switch
        :param switch: the specific switch
        :return: the number of the first empty port
        """
        list_ports = []
        for port in switch['properties']['ports_mapping']:
            list_ports.append(port['port_number'])
        last_port = list_ports[-1]

        list_links = self.nm.get_link_node(switch['node_id'])
        for link in list_links:
            for node in link['nodes']:
                if node['node_id'] == switch['node_id']:
                    list_ports.remove(node['port_number'])

        if len(list_ports) == 0:
            # must add port
            for i in range(last_port + 1, 2 * last_port):
                switch['properties']['ports_mapping'].append(
                    {'name': 'Ethernet' + str(i), 'port_number': i, 'type': 'access', 'vlan': 1})

            self.nm.put_node(switch['node_id'], {'properties': switch['properties']})
            return last_port + 1
        else:
            return list_ports[0]

    def add_dns_adapter(self, node):
        """
        Add one adapter to the specified node
        :param node: the node where we want to add an adapter
        :return: 
        """
        current_adapter = node['properties']['adapters']
        node['properties']['adapters'] = current_adapter + 1
        res = self.nm.put_node(node['node_id'],
                               {'properties': {'adapters': node['properties']['adapters'], 'start_command': ''},
                                'node_type': node['node_type'], 'node_id': node['node_id'],
                                'compute_id': node['compute_id']})
        return res.json()

    def clean(self):
        """
        This method delete all nodes in the project
        """
        list_nodes = self.nm.get_all_nodes()
        for node in list_nodes:
            self.nm.delete_node(node['node_id'])
        pass

    def create_DNS(self, personal_net_config_dns=None):
        """
        This method create a dns
        :param personal_net_config_dns: customize net config of dns
        :return: the dns node
        """
        self.check_switch_service()

        if personal_net_config_dns is None:
            personal_net_config_dns = """# Static config
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

        dns = self.nm.create_template_by_name("thomasbeckers/dns", 250, 100)
        dns = self.add_dns_adapter(dns)
        self.nm.add_file_to_node(dns['node_id'], "/etc/network/interfaces", personal_net_config_dns)

        # linking to switch service
        if self.flag_have_nat and self.nat is None:
            self.nat = self.create_NAT()
            self.nm.link_nodes(self.nat["node_id"], self.switch_out["node_id"], [0, 0],
                               [0, self.get_switch_port(self.switch_out)])
        if self.switch_out is None:
            self.switch_out = self.nm.create_template_by_name("Ethernet switch", dns['x'] - 300,
                                                              dns['y'])

        self.nm.link_nodes(dns["node_id"], self.switch_out["node_id"], [0, 0],
                           [0, self.get_switch_port(self.switch_out)])
        self.nm.link_nodes(dns["node_id"], self.switch_services["node_id"], [1, 0],
                           [0, self.get_switch_port(self.switch_services)])
        return dns

    # dns must be started
    def dns_config(self, dns):
        """
        Add some config to the specific dns
        :param dns: the specific dns

        """
        self.nm.start_node(dns["node_id"])
        time.sleep(2)
        self.dm.exec_to_docker(dns['properties']['container_id'],
                               "iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
        self.dm.copy_to_docker("./config_files/dns/dnsmasq.conf", dns["properties"]["container_id"], "/etc/")
        self.dm.copy_to_docker("./config_files/dns/hosts", dns["properties"]["container_id"], "/etc/")
        self.dm.exec_to_docker(dns["properties"]["container_id"], "service dnsmasq restart")
        pass

    def create_HTTP(self, personal_net_config_http=None):
        """
        This method create an HTTP server
        :param personal_net_config_http: custom net config http
        :return: http node
        """
        self.check_switch_service()

        if personal_net_config_http is None:
            personal_net_config_http = '''# Static config
                                            auto eth0
                                            iface eth0 inet static
                                                address 10.0.0.14
                                                netmask 255.255.255.0
                                                gateway 10.0.0.1
                                                up echo nameserver 8.8.8.8 > /etc/resolv.conf'''

        http = self.nm.create_template_by_name("thomasbeckers/http",
                                               self.switch_services['x'] + (len(self.list_services)) * 100,
                                               self.switch_services['y'] + 200)
        self.nm.add_file_to_node(http["node_id"], "/etc/network/interfaces", personal_net_config_http)

        # linking to switch services
        self.nm.link_nodes(self.switch_services["node_id"], http['node_id'],
                           [0, self.get_switch_port(self.switch_services)], [0, 0])
        self.list_services.append(http)
        return http

    def get_http_nodes(self):
        """

        :return: a list of all http server in the project
        """
        list_http = []
        for service in self.list_services:
            if 'http' in service['name']:
                list_http.append(service)

        return list_http

    def http_config(self, http):
        """
        Add some config to a specific http server
        :param http: the specific http server

        """
        self.nm.start_node(http['node_id'])
        self.dm.copy_to_docker("./config_files/http/database.php", http["properties"]["container_id"], '/var/www/html/')
        pass

    def create_FTP(self, personal_net_config_ftp=None):
        """
        This method create a ftp server
        :param personal_net_config_ftp: the custom net config ftp
        :return: The ftp node
        """
        self.check_switch_service()

        if personal_net_config_ftp is None:
            personal_net_config_ftp = '''# Static config
                                            auto eth0
                                            iface eth0 inet static
                                                address 10.0.0.15
                                                netmask 255.255.255.0
                                                gateway 10.0.0.1
                                                up echo nameserver 8.8.8.8 > /etc/resolv.conf'''

        ftp = self.nm.create_template_by_name("thomasbeckers/ftp",
                                              self.switch_services['x'] + (len(self.list_services)) * 100,
                                              self.switch_services['y'] + 200)
        self.nm.add_file_to_node(ftp['node_id'], "/etc/network/interfaces", personal_net_config_ftp)

        # linking to switch services
        self.nm.link_nodes(self.switch_services['node_id'], ftp["node_id"],
                           [0, self.get_switch_port(self.switch_services)], [0, 0])
        self.list_services.append(ftp)

        return ftp

    def get_ftp_nodes(self):
        """

        :return: a list of all ftp server in the project
        """
        list_ftp = []
        for service in self.list_services:
            if 'ftp' in service['name']:
                list_ftp.append(service)

        return list_ftp

    # node must be started
    def ftp_config(self, ftp):
        """
        Add some config to the ftp server
        :param ftp: the specific ftp server

        """
        self.nm.start_node(ftp["node_id"])
        time.sleep(2)
        self.dm.copy_to_docker("./config_files/ftp/vsftpd.conf", ftp["properties"]["container_id"], "/etc/vsftpd.conf")
        self.dm.copy_to_docker("./python_scripts/write_file.py", ftp["properties"]["container_id"],
                               "/srv/ftp/write_file.py")
        self.dm.copy_to_docker("./config_files/ftp/files", ftp["properties"]["container_id"], "/srv/ftp/")
        self.dm.exec_to_docker(ftp["properties"]["container_id"], "chown root:root /etc/vsftpd.conf")
        self.dm.exec_to_docker(ftp["properties"]["container_id"], "service vsftpd restart")
        # time.sleep(2)
        # self.nm.stop_node(ftp["node_id"])
        pass

    def set_net_config_dhcp_on(self, personal_net_config_dhcp):
        """
        This method set the basic net config dhcp

        """
        self.net_config_dhcp = personal_net_config_dhcp
        pass

    def create_NAT(self):
        """
        This method create a NAT
        """
        self.flag_have_nat = True
        if self.switch_out is None:
            self.switch_out = self.nm.create_template_by_name("Ethernet switch", 130,
                                                              100)
        return self.nm.create_template_by_name("NAT", 0, 100)

    def create_MAIL(self, personal_net_config_mail=None):
        """
        This methode create a mail server
        :param personal_net_config_mail: custom net config mail server
        :return: mail node
        """
        self.check_switch_service()

        if personal_net_config_mail is None:
            personal_net_config_mail = '''# Static config
                                            auto eth0
                                            iface eth0 inet static
                                                address 10.0.0.16
                                                netmask 255.255.255.0
                                                gateway 10.0.0.1
                                                up echo nameserver 8.8.8.8 > /etc/resolv.conf'''

        mail = self.nm.create_template_by_name("thomasbeckers/mail",
                                               self.switch_services['x'] + (len(self.list_services)) * 100,
                                               self.switch_services['y'] + 200)
        self.nm.add_file_to_node(mail['node_id'], "/etc/network/interfaces", personal_net_config_mail)

        self.nm.link_nodes(self.switch_services['node_id'], mail["node_id"],
                           [0, self.get_switch_port(self.switch_services)], [0, 0])
        self.list_services.append(mail)
        return mail

    def check_switch_service(self):
        """
        This method check if the switch service is already created otherwise create it

        """
        if self.switch_services is None:
            self.switch_services = self.nm.create_template_by_name("Ethernet switch", 450, 100)
            # linking to switch_lan
            if self.switch_lan is not None:
                self.nm.link_nodes(self.switch_services['node_id'], self.switch_lan['node_id'],
                                   [0, self.get_switch_port(self.switch_services)],
                                   [0, self.get_switch_port(self.switch_lan)])
        pass

    def create_db(self, personal_net_config_db=None):
        """
        This method create a server database
        :param personal_net_config_db: custom personal net config for the db server
        :return: db node
        """
        self.check_switch_service()

        if personal_net_config_db is None:
            personal_net_config_db = '''# Static config
                                            auto eth0
                                            iface eth0 inet static
                                                address 10.0.0.17
                                                netmask 255.255.255.0
                                                gateway 10.0.0.1
                                                up echo nameserver 8.8.8.8 > /etc/resolv.conf'''

        db = self.nm.create_template_by_name("thomasbeckers/db",
                                             self.switch_services['x'] + (len(self.list_services)) * 100,
                                             self.switch_services['y'] + 200)
        self.nm.add_file_to_node(db["node_id"], "/etc/network/interfaces", personal_net_config_db)

        # linking to switch services
        self.nm.link_nodes(self.switch_services["node_id"], db['node_id'],
                           [0, self.get_switch_port(self.switch_services)], [0, 0])
        self.list_services.append(db)
        return db

    def get_db_nodes(self):
        """
        list all db servers in the project
        :return:
        """
        list_db = []
        for service in self.list_services:
            if 'db' in service['name']:
                list_db.append(service)

        return list_db

    # db must be started
    def db_config(self, db):
        """
        Add some config to the specific db server
        :param db: the specific db server
        """
        self.nm.start_node(db['node_id'])
        # wait mysql to start
        time.sleep(5)
        self.dm.copy_to_docker("./config_files/db/setup.sql", db["properties"]["container_id"])
        self.dm.exec_to_docker(db["properties"]["container_id"], "/bin/sh -c 'mysql -u root < setup.sql'")
        pass

    def get_pc_nodes(self, name):
        """
        This method allows to get a list of specific type of pcs.

        :param name: The name of the specific pcs
        :return: The list of the specific pcs
        """
        list_template = []
        for pc in self.list_pcs:
            if name in pc['name']:
                list_template.append(pc)

        return list_template
