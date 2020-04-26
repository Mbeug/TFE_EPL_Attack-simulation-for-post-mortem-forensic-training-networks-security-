import traceback



from analyser_manager import AnalyserManager
from attacker_manager import AttackerManager
from colorOutput import ColorOutput
from network_manager import NetworkManager
from simulation_manager import SimulationManager
from topology_manager import TopologyManager
from utility import Utility
from tqdm.auto import tqdm

class Client:
    """
    this class simulate a client
    """
    if __name__ == "__main__":
        try :
            nm = NetworkManager()
            tm = TopologyManager(nm,False)
            sim = SimulationManager(nm)


            if Utility.ask_user_boolean("Do you want to build the topology?"):
                # creation of DNS
                pbar = tqdm(range(9))
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
                pbar.update(1)
                # Config DNS and DHCP
                tm.dns_config(DNS)

                # Add some node
                tm.create_n_node(1, "Firefox")
                pbar.update(2)
                tm.create_n_node(3, "thomasbeckers/alpine-curl")
                pbar.update(5)
                tm.create_HTTP()
                pbar.update(6)
                tm.create_FTP()
                pbar.update(7)
                tm.create_db()
                pbar.update(8)

                # config http
                HTTP = tm.get_http_nodes()[0]
                tm.http_config(HTTP)

                # config ftp
                FTP = tm.get_ftp_nodes()[0]
                tm.ftp_config(FTP)

                MAIL = tm.create_MAIL()
                pbar.update(9)
                db = tm.get_db_nodes()[0]
                tm.db_config(db)
                pbar.close()
            nm.start_all_nodes()

            # Launch simulation phase
            if Utility.ask_user_boolean("Do you want to launch the activity simulation?"):
                alpines = tm.get_pc_nodes("alpine-curl")
                sim.mail_activity(alpines)
                sim.kill_mail_activity([alpines[0]])
                sim.http_ftp_activity(alpines)

            # Launch attack phase
            attack_flag = Utility.ask_user_boolean("Do you want to make attacks?")
            if attack_flag:
                # Add the attacker
                flag_am_position = ['out', 'in_service', 'in_lan']
                am = AttackerManager(tm,Utility.ask_user_number("How many attackers do you want?"),Utility.ask_user_choice(flag_am_position, "Where do you want to put it?"))

                attacker = None
                if len(am.list_attackers)>0:
                    attacker = am.list_attackers[0]
                while attack_flag and attacker != None:
                    # Ask which attack made
                    attack = Utility.ask_user_choice(['Host discovery', 'Scan ports', 'Dos attack'])
                    if attack == 'Host discovery':
                        am.host_discovery(attacker,'192.168.122.',0,100)
                    elif attack == 'Scan ports' :
                        am.scan_port(attacker,'192.168.122.10',1,1024)
                    elif attack == 'Dos attack' :
                        am.dos(attacker,'192.168.122.30','192.168.122.10',80)

                    attack_flag=Utility.ask_user_boolean("Do you want to make an other attack?")


            # Launch the analyse phase
            if Utility.ask_user_boolean("Do you want to make an analyse?"):
                anm = AnalyserManager(nm)
                anm.start_nodes()
                anm.stop_nodes()
                anm.start(DNS)
                anm.stop(DNS)
                anm.start_all_capture()
                anm.stop_all_capture()
                anm.start_capture_btw(DNS, HTTP)
                anm.stop_capture_btw(DNS, HTTP)

        except Exception :
            print(ColorOutput.ERROR_TAG)
            traceback.print_exc()

        finally:
            # end of client
            if Utility.ask_user_boolean("Do you want to close all?"):
                nm.stop_all_node()
                tm.clean()
