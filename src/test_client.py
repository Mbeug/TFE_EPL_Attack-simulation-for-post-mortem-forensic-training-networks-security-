import traceback
import threading

from analyser_manager import AnalyserManager
from attacker_manager import AttackerManager
from colorOutput import ColorOutput
from network_manager import NetworkManager
from simulation_manager import SimulationManager
from topology_manager import TopologyManager
from utility import Utility



class Client:
    """
    this class simulate a client
    """
    global threads_attack
    if __name__ == "__main__":
        try:
            nm = NetworkManager()
            tm = TopologyManager(nm, False)
            sim = SimulationManager(nm)
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
                print(ColorOutput.INFO_TAG+": Creating the DNS ...")
                # Config DNS and DHCP
                tm.dns_config(DNS)

                # Add some node
                print(ColorOutput.INFO_TAG+": Creating the workspace area ...")
                tm.create_n_node(1, "Firefox")
                tm.create_n_node(3, "thomasbeckers/alpine-curl")
                print(ColorOutput.INFO_TAG+": Creating HTTP server ...")
                tm.create_HTTP()
                print(ColorOutput.INFO_TAG+": Creating FTP server ...")
                tm.create_FTP()
                print(ColorOutput.INFO_TAG+": Creating DB server")
                tm.create_db()


                # config http
                HTTP = tm.get_http_nodes()[0]
                tm.http_config(HTTP)

                # config ftp
                FTP = tm.get_ftp_nodes()[0]
                tm.ftp_config(FTP)

                print(ColorOutput.INFO_TAG+": Creating MAIL server ...")
                MAIL = tm.create_MAIL()
                db = tm.get_db_nodes()[0]
                tm.db_config(db)

            print(ColorOutput.INFO_TAG+": Starting nodes ...")
            nm.start_all_nodes()

            # Launch simulation phase
            alpines = None
            if Utility.ask_user_boolean("Do you want to launch the activity simulation?"):
                alpines = tm.get_pc_nodes("alpine-curl")
                print("Starting mail activity ...")
                sim.mail_activity(alpines)
                print("Starting FTP activity")
                sim.http_ftp_activity(alpines)

            # Launch attack phase
            attack_flag = Utility.ask_user_boolean("Do you want to make attacks?")
            if attack_flag:
                # Add the attacker
                flag_am_position = ['out', 'in_service', 'in_lan']
                position = Utility.ask_user_choice(flag_am_position, "Where do you want to put attackers?")
                am = AttackerManager(tm, Utility.ask_user_number("How many attackers do you want?"), position)
                attacker = None
                if len(am.list_attackers) > 0:
                    attacker = am.list_attackers[0]
                while attack_flag and attacker is not None:
                    # Ask which attack made
                    attack = Utility.ask_user_choice(['Host discovery', 'Scan ports', 'Dos attack'])
                    if attack == 'Host discovery':
                        if position == flag_am_position[0]:
                            thread_host = threading.Thread(name="Thread host discovering out", target=am.host_discovery,
                                             args=[attacker, '192.168.122.', 0, 100])
                            thread_host.start()
                            threads_attack.append(thread_host)
                            #am.host_discovery(attacker, '192.168.122.', 0, 100)
                        else:
                            thread_host = threading.Thread(name="Thread host discovering inner", target=am.host_discovery,
                                                 args=[attacker, '10.0.0.', 0, 100])
                            thread_host.start()
                            threads_attack.append(thread_host)
                            #am.host_discovery(attacker, '10.0.0.', 0, 100)
                    elif attack == 'Scan ports':
                        if position == flag_am_position[0]:
                            thread_scan_port = threading.Thread(name="Thread Scan port out", target=am.scan_port,
                                                 args=[attacker, '192.168.122.10', 1, 1024])
                            thread_scan_port.start()
                            threads_attack.append(thread_scan_port)
                            #am.scan_port(attacker, '192.168.122.10', 1, 1024)
                        else:
                            thread_scan_port = threading.Thread(name="Thread Scan port inner", target=am.scan_port,
                                                 args=[attacker, '192.168.122.10', 1, 1024])
                            thread_scan_port.start()
                            threads_attack.append(thread_scan_port)
                            am.scan_port(attacker, '192.168.122.10', 1, 1024)
                    elif attack == 'Dos attack':
                        if position == flag_am_position[0]:
                            thread_dos = threading.Thread(name="Thread Dos attack out", target=am.dos,
                                                 args=[attacker, '192.168.122.30', '192.168.122.10', 80])
                            thread_dos.start()
                            threads_attack.append(thread_dos)
                            #am.dos(attacker, '192.168.122.30', '192.168.122.10', 80)
                        else:
                            thread_dos = threading.Thread(name="Thread Dos attack in", target=am.dos,
                                                 args=[attacker, '192.168.122.30', '192.168.122.10', 80])
                            thread_dos.start()
                            threads_attack.append(thread_dos)
                            #am.dos(attacker, '192.168.122.30', '192.168.122.10', 80)

                    attack_flag = Utility.ask_user_boolean("Do you want to make an other attack?")

            # Launch the analyse phase
            if Utility.ask_user_boolean("Do you want to make an analyse?"):
                anm = AnalyserManager(nm)
                anm.start_nodes()
                if Utility.ask_user_boolean("Do you want to do overall capture?"):
                    anm.start_all_capture()
                    anm.stop_all_capture()
                analyse_flag = Utility.ask_user_boolean("Do you want to do a specific capture")
                while analyse_flag:
                    choices = ['DNS', 'HTTP', 'FTP', 'MAIL']
                    analyse = Utility.ask_user_choice(choices,"Which node do you want to capture?")
                    if analyse == 'DNS':
                        anm.start_capture_node(DNS)
                        anm.stop_capture_node(DNS)
                    elif analyse == 'HTTP':
                        anm.start_capture_node(HTTP)
                        anm.stop_capture_node(HTTP)
                    elif analyse == 'FTP':
                        anm.start_capture_node(FTP)
                        anm.stop_capture_node(FTP)
                    elif analyse == 'MAIL':
                        anm.start_capture_node(MAIL)
                        anm.stop_capture_node(MAIL)

                    analyse_flag = Utility.ask_user_boolean("Do you want to do an other?")
                anm.stop_nodes()


            # Stop the activity simulation
            if alpines is not None:
                print("Stopping activity ...")
                nm.start_all_nodes()
                sim.kill_mail_activity(alpines)
                sim.kill_http_ftp_activity(alpines)
                nm.stop_all_node()



        except Exception:
            print(ColorOutput.ERROR_TAG)
            traceback.print_exc()

        finally:
            # end of client
            print(ColorOutput.INFO_TAG+": waiting threads for attacks processes ...")
            for thread in threads_attack:
                thread.join()

            nm.stop_all_node()

            if nm is not None and tm is not None:
                if Utility.ask_user_boolean("Do you want to close all?"):
                    tm.clean()
