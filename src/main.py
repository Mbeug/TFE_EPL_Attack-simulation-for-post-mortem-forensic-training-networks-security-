import argparse
import configparser
import os
import sys
import time

import tqdm

from colorOutput import ColorOutput
from newtwork_manager import NetworkManager
from simple_topology import SimpleTopology

home_dir = os.path.expanduser("~")
config_server = configparser.ConfigParser()
config_server.read_file(open(home_dir+"/.config/GNS3/2.2/gns3_server.conf"))

section = "Server"
gns3_user = config_server.get(section, "user")
gns3_password = config_server.get(section, "password")
gns3_host = config_server.get(section, "host")
gns3_port = config_server.get(section, "port")

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="*** GNS3 remote control ***")
    parser.add_argument("-s", "--start", help="launch the basic topology network", action="store_true")
    parser.add_argument("-u", "--updater", help="launch the network manager", action="store_true")
    parser.add_argument("-a", "--analyser", help="launch the analyser manager", action="store_true")
    parser.add_argument("-A", "--Attacker", help="launch the attacker manager", action="store_true")
    args = parser.parse_args()

    print("*"*10+"- Launching GNS3 program -"+"*"*10)
    if sys.platform == "darwin":
        print(ColorOutput.INFO_TAG + "You are on the OSX version !")
        os.system("open -a virtualbox")
        os.system("open -a gns3")
    else :
        print(ColorOutput.INFO_TAG+"You are in the Linux version !")
        os.system("/usr/bin/gns3")

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

    exit_key = input("Press 'q' to exit.\n")
    while exit_key != 'q':
        exit_key = input()


    if exit_key == "q":
        if sys.platform == "darwin":
            print("Goodbye OSX!")
            os.system("osascript -e 'quit app \"GNS3\"'")
            os.system("osascript -e 'quit app \"virtualbox\"'")
        else :
            print("Goodbye Linux!")
            os.system("killall gns3")
    pass
    exit(0)