from attacker_manager import AttackerManager
from network_manager import NetworkManager
from topology_manager import TopologyManager
from simulation_manager import SimulationManager

class Client:
    """
    this class simulate a client
    """
    if __name__ == "__main__":
        nm = NetworkManager()
        tm = TopologyManager(nm,True)
    #     sim = SimulationManager(nm)
    # # creation of DNS
    # my_net_config_dns = '''# Static config
    #                             auto eth0
    #                             iface eth0 inet static
    #                                 address 192.168.122.10
    #                                 netmask 255.255.255.0
    #                                 gateway 192.168.122.1
    #                                 up echo nameserver 8.8.8.8 > /etc/resolv.conf
    #                             auto eth1
    #                             iface eth1 inet static
    #                                 address 10.0.0.1
    #                                 netmask 255.255.255.0'''
    #
    # DNS = tm.create_DNS(my_net_config_dns)
    #
    # # Config DNS and DHCP
    # tm.dns_config(DNS)
    #
    # # Add some node
    # tm.create_n_node(1, "Firefox")
    # tm.create_n_node(3, "thomasbeckers/alpine-curl")
    # tm.create_HTTP()
    # tm.create_FTP()
    # tm.create_db()
    #
    # # config http
    # HTTP = tm.get_http_nodes()[0]
    # tm.http_config(HTTP)
    #
    # # config ftp
    # FTP = tm.get_ftp_nodes()[0]
    # tm.ftp_config(FTP)
    #
    # MAIL = tm.create_MAIL()
    #
    # db = tm.get_db_nodes()[0]
    # tm.db_config(db)
    #
    # nm.start_all_nodes()

    #add the attacker
    flag_am_position = ['out','in_service','in_lan']
    am = AttackerManager(tm,flag_am_position[0])
    # launch differents attacks
    attack_flag = input("Do you want to make an attack? (Y/N)").lower()
    while attack_flag != 'y' and attack_flag != 'n':
        attack_flag = input(
            "You enter a wrong value: " + str(attack_flag) + " . Please try with 'y' or 'n'.").lower()
    if attack_flag == 'y':
        attack = int(input("Which attack do you want to do? \n"
                           "[0]:host discorvery\n"
                           "[1]:scan ports\n"
                           "[2]:dos\n"))
    if attack == 0 :
        am.host_discovery('192.168.122.10') #ok
    elif attack == 1 :
        am.scan_port('192.168.122.10',1,1024) #ok
    elif attack == 2 :
        am.dos('192.168.122.30','192.168.122.10',80) #ok

    # alpines = tm.get_pc_nodes("alpine-curl")
    # # sim.mail_activity(alpines)
    # # sim.kill_mail_activity([alpines[0]])
    # sim.http_ftp_activity(alpines)

    # end of client
    kill_all_flag = input("Do you want to close all? (Y/N)").lower()
    while kill_all_flag != 'y' and kill_all_flag != 'n':
        kill_all_flag = input(
            "You enter a wrong value: " + str(kill_all_flag) + " . Please try with 'y' or 'n'.").lower()

    if kill_all_flag == 'y':
        nm.stop_all_node( )
        tm.clean()