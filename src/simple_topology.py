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
        nb_vpcs = int(input("How many VPCS?\n"))
        self.create_n_vpcs(nb_vpcs)
        # Link all switches
        self.link_all_switches(nb_vpcs)
        self.link_to_cloud()
        # Start the network
        pass

    def create_n_vpcs(self, nb_vpc):
        nb_switch = math.ceil(nb_vpc/7)  # 7 is max vpcs number by switch
        range_vpcs = nb_vpc
        switch_x = 10
        switch_y= nb_switch*-80/2

        for idx_switch in range(nb_switch):
            cur_switch = self.create_switch("Switch "+str(idx_switch), (int(switch_x), int(switch_y)))
            # cur_switch.set_position((int(switch_x), int(switch_y)))
            vpcs_x = switch_x + 100
            vpcs_per_switch = min(range_vpcs,7)
            vpc_y = switch_y+vpcs_per_switch*-80/2
            for idx_vpcs in range(vpcs_per_switch):
                cur_vpc = self.create_vpc("VPC "+str(idx_switch)+":"+str(idx_vpcs), (int(vpcs_x),int(vpc_y)))
                # cur_vpc.set_position((int(vpcs_x),int(vpc_y)))
                self.link_vpc_to_switch(cur_switch, idx_vpcs, cur_vpc)
                self.list_vpcs.append(cur_vpc)
                vpc_y += 80
            self.list_switch.append(cur_switch)
            range_vpcs -= 7
            switch_y += 360
            switch_x -= 200
        pass

    def create_switch(self, name, pos):
        return Node(self.nm, name, 'ethernet_switch', self.nm.selected_project['project_id'], "/symbols/ethernet_switch.svg", pos)

    def create_vpc(self, name, pos):
        return Node(self.nm, name, 'vpcs', self.nm.selected_project['project_id'],"/symbols/computer.svg", pos)

    def link_vpc_to_switch(self, switch, switch_port, vpc):
        payload = {"nodes": [{"adapter_number": 0, "node_id": switch.get_id(), "port_number": switch_port}, {"adapter_number": 0, "node_id": vpc.get_id(), "port_number": 0}]}
        response = self.nm.gns3_req_param('/projects/' + self.nm.selected_project['project_id'] + '/links', payload)

        if response.status_code != 200 and response.status_code != 201:
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)

    def link_all_switches(self, nb_vpc):
        if math.ceil(nb_vpc / 7) < 7 - (nb_vpc % 7) and nb_vpc % 7 != 0:
            print(ColorOutput.INFO_TAG+": have enough place in the last switch")
            last_switch = self.list_switch[-1]
            last_switch_port = nb_vpc%7
            for idx_switch in range(0,len(self.list_switch)-1):
                self.link_switch_to_switch(last_switch, last_switch_port, self.list_switch[idx_switch], 7)
                last_switch_port += 1
        else:
            print(ColorOutput.INFO_TAG+ ": must to add switch")
        pass

    def link_to_cloud(self):
        pass

    def link_switch_to_switch(self, switch_a , port_a, switch_b, port_b):
        payload = {"nodes": [{"adapter_number": 0, "node_id": switch_a.get_id(), "port_number": port_a},
                             {"adapter_number": 0, "node_id": switch_b.get_id(), "port_number": port_b}]}
        response = self.nm.gns3_req_param('/projects/' + self.nm.selected_project['project_id'] + '/links', payload)

        if response.status_code != 200 and response.status_code != 201:
            print(ColorOutput.DEBUG_TAG + ": port a " + str(port_a) + " port b " + str(port_b))
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)
        pass
