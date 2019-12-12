import math

from colorOutput import ColorOutput
from newtwork_manager import NetworkManager
from node import Node


class SimpleTopology:

    def __init__(self):
        self.nm = NetworkManager()
        self.list_switch = []
        self.list_vpcs = []
        self.build()


    def build(self):
        # Creating n vpcs with its switches
        self.create_n_vpcs(int(input("How many VPCS?\n")))
        # Link all switches
        # Start the network
        pass

    def create_n_vpcs(self, nb_vpc):
        nb_switch = math.ceil(nb_vpc/7)  # 7 is max vpcs number by switch
        range_vpcs = nb_vpc
        switch_x = 10
        switch_y= nb_switch*-80/2
        vpcs_x = switch_x + 100
        for idx_switch in range(nb_switch):
            cur_switch = self.create_switch("Switch "+str(idx_switch))
            #cur_switch.set_position((int(switch_x), int(switch_y)))
            vpcs_per_switch = min(range_vpcs,7)
            vpc_y = vpcs_per_switch*-80/2
            for idx_vpcs in range(vpcs_per_switch):
                cur_vpc = self.create_vpc("VPC "+str(idx_switch)+":"+str(idx_vpcs))
                #cur_vpc.set_position((int(vpcs_x),int(vpc_y)))
                self.link_to(cur_switch, idx_vpcs, cur_vpc)
                self.list_vpcs.append(cur_vpc)
                vpc_y += 80
            self.list_switch.append(cur_switch)
            range_vpcs -= 7
            switch_y += 80
        pass

    def create_switch(self, name):
        return Node(self.nm, name, 'ethernet_switch', self.nm.selected_project['project_id'], "/symbols/ethernet_switch.svg")

    def create_vpc(self, name):
        return Node(self.nm, name, 'vpcs', self.nm.selected_project['project_id'],"/symbols/computer.svg")

    def link_to(self, switch, switch_port, vpc):
        payload = {"nodes": [{"adapter_number": 0, "node_id": switch.get_id(), "port_number": switch_port}, {"adapter_number": 0, "node_id": vpc.get_id(), "port_number": 0}]}
        response = self.nm.gns3_req_param('/projects/' + self.nm.selected_project['project_id'] + '/links', payload)

        if response.status_code != 200 and response.status_code != 201:
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)
