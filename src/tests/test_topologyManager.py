from unittest import TestCase

from topology_manager import TopologyManager


class TestTopologyManager(TestCase):
    tm = TopologyManager()
    nm = tm.nm

    def test_create_topology(self):
        # creation of DNS
        my_net_config_dns = '''# Static config
                                auto eth0
                                iface eth0 inet static
                                    address 192.168.122.10
                                    netmask 255.255.255.0
                                    gateway 192.168.122.1
                                    up echo nameserver 8.8.8.8 > /etc/resolv.conf
                                auto eth1
                                iface eth1 inet static
                                    address 10.0.0.1
                                    netmask 255.255.255.0'''

        DNS = self.tm.create_DNS(my_net_config_dns)


        # Config DNS and DHCP
        self.tm.dns_config(DNS)# TODO we can add some parameters to raise the personification of the dns

        # Add some node
        self.tm.create_n_node(3,"Firefox")
        self.tm.create_n_node(2,"Alpine")
        self.tm.create_HTTP()
        self.tm.create_FTP()

        # config http
        HTTP = self.tm.get_http_nodes()[0]
        self.tm.http_config(HTTP)

        # config ftp
        FTP = self.tm.get_ftp_nodes()[0]
        self.tm.ftp_config(FTP)

        MAIL = self.tm.create_MAIL()
        self.nm.start_all_nodes()

        flag = int(input(
            "Do you want clear(Y=1/N=0)?:"))
        while (flag != 1 and flag != 0):
            flag = int(input("Your input isn't supported, try again:"))
        if flag:
            self.tm.clean()

        self.assertTrue(True)