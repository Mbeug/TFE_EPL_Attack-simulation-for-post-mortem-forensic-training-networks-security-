from network_manager import NetworkManager
from topology_manager import TopologyManager

if __name__ == "__main__":
    nm = NetworkManager()
    tm = TopologyManager(nm)

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

    DNS = tm.create_DNS(my_net_config_dns)

    # Config DNS and DHCP
    tm.dns_config(DNS)

    # Add some node
    tm.create_n_node(3, "Firefox")
    tm.create_n_node(2, "Alpine")
    tm.create_HTTP()
    tm.create_FTP()
    tm.create_db()

    # config http
    HTTP = tm.get_http_nodes()[0]
    tm.http_config(HTTP)

    # config ftp
    FTP = tm.get_ftp_nodes()[0]
    tm.ftp_config(FTP)

    MAIL = tm.create_MAIL()

    db = tm.get_db_nodes()[0]
    tm.db_config(db)

    nm.start_all_nodes()

    flag = int(input(
        "Do you want clear(Y=1/N=0)?:"))
    while (flag != 1 and flag != 0):
        flag = int(input("Your input isn't supported, try again:"))
    if flag:
        nm.stop_all_node()
        tm.clean()