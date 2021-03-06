import traceback

from analyzer_manager import AnalyzerManager
from attacker_manager import AttackerManager
from color_output import ColorOutput
from network_manager import NetworkManager
from simulation_manager import SimulationManager
from topology_manager import TopologyManager
from utility import Utility


class Client:
    """
    This class is an example of all of our work, we named it Client
    """

    if __name__ == "__main__":
        try:
            nm: NetworkManager = NetworkManager(id_machine=Utility.ask_user_choice(['local','vm'], "Choose the configuration"))
            tm: TopologyManager = TopologyManager(nm, False)
            sim: SimulationManager = SimulationManager(nm)
            anm: AnalyzerManager = None
            am: AttackerManager = None
            threads_attack = []

            if Utility.ask_user_boolean("Do you want to build the topology?"):
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
                print(ColorOutput.INFO_TAG + ": [1/6] Creating the DNS ...")
                # Config DNS and DHCP
                tm.dns_config(DNS)

                # Add some node
                print(ColorOutput.INFO_TAG + ": [2/6] Creating the workspace area ...")
                tm.create_n_node(1, "Firefox")
                tm.create_n_node(3, "thomasbeckers/alpine-curl")
                print(ColorOutput.INFO_TAG + ": [3/6] Creating HTTP server ...")
                tm.create_HTTP()
                print(ColorOutput.INFO_TAG + ": [4/6] Creating FTP server ...")
                tm.create_FTP()
                print(ColorOutput.INFO_TAG + ": [5/6] Creating DB server ...")
                tm.create_db()

                # config http
                HTTP = tm.get_http_nodes()[0]
                tm.http_config(HTTP)

                # config ftp
                FTP = tm.get_ftp_nodes()[0]
                tm.ftp_config(FTP)

                print(ColorOutput.INFO_TAG + ": [6/6] Creating MAIL server ...")
                MAIL = tm.create_MAIL()
                db = tm.get_db_nodes()[0]
                tm.db_config(db)

            print(ColorOutput.INFO_TAG + ": Starting nodes ...")
            nm.start_all_nodes()

            # Launch the analyze phase
            if Utility.ask_user_boolean("Do you want to launch an analyze?"):
                anm = AnalyzerManager(nm)
                anm.start_nodes()
                if Utility.ask_user_boolean("Do you want to do overall capture?"):
                    anm.start_all_capture()

                analyze_flag = Utility.ask_user_boolean("Do you want to do a specific capture")
                while analyze_flag:
                    choices = ['DNS', 'HTTP', 'FTP', 'MAIL']
                    analyze = Utility.ask_user_choice(choices, "Which node do you want to capture a service node?")
                    if analyze == 'DNS':
                        anm.start_capture_node(DNS)
                    elif analyze == 'HTTP':
                        anm.start_capture_node(HTTP)
                    elif analyze == 'FTP':
                        anm.start_capture_node(FTP)

                    elif analyze == 'MAIL':
                        anm.start_capture_node(MAIL)

                    analyze_flag = Utility.ask_user_boolean("Do you want to do an other?")

            # Launch simulation phase
            alpines = None
            if Utility.ask_user_boolean("Do you want to launch the activity simulation?"):
                alpines = tm.get_pc_nodes("alpine-curl")
                print("Starting mail activity ...")
                sim.mail_activity(alpines)
                print("Starting FTP activity ...")
                sim.http_ftp_activity(alpines)


            # Launch attack phase
            attack_flag = Utility.ask_user_boolean("Do you want to make attacks?")
            if attack_flag:
                am = AttackerManager(tm)
                if Utility.ask_user_boolean("Do you want to make a DNS tunnel?"):
                    am.dns_tunneling()

                # Add the attacker
                flag_am_position = ['out', 'in_service', 'in_lan']
                position = Utility.ask_user_choice(flag_am_position, "Where do you want to put attackers?")
                am.create_attackers(1, position)
                attacker = am.list_attackers[0]
                while attack_flag :
                    # Ask which attack made
                    attack = Utility.ask_user_choice(['Host discovery', 'Scan ports', 'Dos attack'])
                    if attack == 'Host discovery':
                        if position == flag_am_position[0]:
                            am.launch_attack_host_discovery([attacker, '192.168.122.', 0, 100])
                        else:
                            am.launch_attack_host_discovery([attacker, '10.0.0.', 0, 100])
                    elif attack == 'Scan ports':
                        if position == flag_am_position[0]:
                            am.launch_attack_scan_ports([attacker, '192.168.122.10', 1, 1024])
                        else:
                            am.launch_attack_scan_ports([attacker, '10.0.0.14', 1, 1024])
                    elif attack == 'Dos attack':
                        if position == flag_am_position[0]:
                            am.launch_attack_dos([attacker, '192.168.122.30', '192.168.122.10', 80])
                        else:
                            am.launch_attack_dos([attacker, '192.168.122.30', '10.0.0.14', 80])

                    attack_flag = Utility.ask_user_boolean("Do you want to make an other attack?")


            # Stop the activity simulation
            if alpines is not None:
                if Utility.ask_user_boolean("Do you want to stop the activity simulation?"):
                    print("Stopping activity ...")
                    nm.start_all_nodes()
                    sim.kill_mail_activity(alpines)
                    sim.kill_http_ftp_activity(alpines)


            # Stop the capture
            if anm is not None:
                if Utility.ask_user_boolean("Do you want to stop the capture?"):
                    anm.stop_all_capture()


        except Exception:
            print(ColorOutput.ERROR_TAG)
            traceback.print_exc()

        finally:

            # Waiting the end of threads for attacks
            if am is not None:
                am.stop_threads_attacks()

            # Stopping node
            if nm is not None :
                if Utility.ask_user_boolean("Do you want to stop all node?"):
                    print(ColorOutput.INFO_TAG+": Stopping node ...")
                    nm.stop_all_node()

            # Clean the project
            if nm is not None and tm is not None:
                if Utility.ask_user_boolean("Do you want to clean all?"):
                    tm.clean()
