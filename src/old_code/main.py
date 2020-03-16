import argparse
import configparser
import os
import sys
import time

import tqdm

from colorOutput import ColorOutput
from network_manager import NetworkManager
from old_code.simple_topology import SimpleTopology

home_dir = os.path.expanduser("~") #Risk to bug with win version : d'apres la doc python sur os.path ça passe
config_server = configparser.ConfigParser()
config_server.read_file(open(home_dir+"/.config/GNS3/2.2/gns3_server.conf"))

section = "Server"
gns3_user = config_server.get(section, "user")
gns3_password = config_server.get(section, "password")
gns3_host = config_server.get(section, "host")
gns3_port = config_server.get(section, "port")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="*** GNS3 remote control ***")
    parser.add_argument("-s", "--start", help="launch the basic topology network", action="store_true")
    parser.add_argument("-u", "--updater", help="launch the network manager", action="store_true")
    parser.add_argument("-a", "--analyser", help="launch the analyser manager", action="store_true")
    parser.add_argument("-A", "--Attacker", help="launch the attacker manager", action="store_true")
    args = parser.parse_args()

    print("*"*10+"- Launching GNS3 program -"+"*"*10)
    platform = sys.platform
    if platform == "darwin":
        print(ColorOutput.INFO_TAG + "You are on the OSX version !")
        os.system("open -a virtualbox")
        os.system("open -a gns3")
    elif platform == "linux" or platform == "linux2":
        print(ColorOutput.INFO_TAG+": You are on the Linux version !")
    elif platform == "win32":
        print(ColorOutput.INFO_TAG+"You are in the Windows version !")
        os.popen("gns3")
    else :
        print(ColorOutput.ERROR_TAG+": The platform isn't supported.")
        exit(1)
    # put ping for the check co
    for i in tqdm.tqdm(range(60)):
        time.sleep(0.1)
    network = None
    if args.start:
        time.sleep(1)
        input("Press Enter after choose the recent project to continue...")
        print("*"*10+" Launching the basic network topology "+"*"*10)
        network = SimpleTopology()

    if args.updater:
        print("*"*10+"Network manager"+"*"*10)
        net_manager = None
        if network == None:
            # Start a new topology
            net_manager = NetworkManager()
        else:
            net_manager = network.nm
            # Ready to modify the basic topology

    if args.analyser:
        print("analyser manager")
        # os.system("python3 analyser_manager.py")
    if args.Attacker:
        print("attacker manager")
        # os.system("python3 attacker_manager.py")

    exit_key = input("Press 'q' to exit.\n").lower()
    while exit_key != 'q':
        exit_key = input("You enter a wrong value: "+str(exit_key)+". Please try with 'q' or 'Q'.").lower()

    kill_all_flag = input("Do you want to close all? (Y/N)").lower()
    while kill_all_flag != 'y' and kill_all_flag != 'n':
        kill_all_flag = input("You enter a wrong value: "+str(kill_all_flag)+" . Please try with 'y' or 'n'.").lower()

    if exit_key == "q":
        if platform == "darwin":
            print("Goodbye OSX!")
            if kill_all_flag == 'y':
                os.system("osascript -e 'quit app \"GNS3\"'")
                os.system("osascript -e 'quit app \"virtualbox\"'")
        elif platform == "linux" or platform == "linux2" :
            print("Goodbye Linux!")
            if kill_all_flag == 'y':
                os.system("killall gns3")

        elif platform == "win32":
            print("GoodBye Windows!")
    pass
    exit(0)