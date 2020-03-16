import math

from colorOutput import ColorOutput
from network_manager import NetworkManager
from node import Node


class SimpleTopology:

    def __init__(self):
        self.nm = NetworkManager()
        self.list_switch = []
        self.list_vpcs = []
        self.router = None

    def build(self, nb_vpcs = None):
        # Creating n vpcs with its switches
        if nb_vpcs == None :
            nb_vpcs = int(input("How many VPCS?\n"))
        self.create_n_vpcs(nb_vpcs)
        # Linking
        #self.create_router()
        #self.link_lan_to_router()
        # self.link_to_cloud()
        # Start the network
        pass

    def create_n_vpcs(self,nb_vpc):
        switch = self.create_switch("Switch 0",(10,200))
        nb_add_port = nb_vpc - 7
        if nb_add_port > 0:
            for i in range(8,8+nb_add_port):
                switch.response['properties']['ports_mapping'].append({'name': 'Ethernet'+str(i), 'port_number': i, 'type': 'access', 'vlan': 1})

        switch.set_ports({'ports_mapping':switch.response['properties']['ports_mapping']})


        vpcs_x = switch.get_position()[0] + 100
        vpc_y = switch.get_position()[1] + nb_vpc*(-80)/2
        for idx_vpcs in range(nb_vpc):
            cur_vpc = self.create_vpc("VPC 0:"+str(idx_vpcs), (int(vpcs_x), int(vpc_y)))
            self.link_vpc_to_switch(switch, idx_vpcs, cur_vpc)
            self.list_vpcs.append(cur_vpc)
            vpc_y += 80

        self.list_switch.append(switch)
        pass

    def create_switch(self, name, pos):
        tmp = Node(self.nm, name, 'ethernet_switch', self.nm.selected_project['project_id'], "/symbols/ethernet_switch.svg",self.nm.selected_machine['compute_id'])
        tmp.build()
        tmp.set_position(pos)
        return tmp

    def create_vpc(self, name, pos):
        tmp = Node(self.nm, name, 'vpcs', self.nm.selected_project['project_id'], "/symbols/computer.svg",self.nm.selected_machine['compute_id'])
        tmp.build()
        tmp.set_position(pos)
        return tmp

    def link_vpc_to_switch(self, switch: Node, switch_port, vpc: Node):
        payload = {"nodes": [{"adapter_number": 0, "node_id": switch.get_id(), "port_number": switch_port}, {"adapter_number": 0, "node_id": vpc.get_id(), "port_number": 0}]}
        response = self.nm.gns3_request_post('/projects/' + self.nm.selected_project['project_id'] + '/links', payload)

        if response.status_code != 200 and response.status_code != 201:
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)

    def link_switch_to_switch(self, switch_a, port_a, switch_b, port_b):
        payload = {"nodes": [{"adapter_number": 0, "node_id": switch_a.get_id(), "port_number": port_a},
                             {"adapter_number": 0, "node_id": switch_b.get_id(), "port_number": port_b}]}
        response = self.nm.gns3_request_post('/projects/' + self.nm.selected_project['project_id'] + '/links', payload)
        if response.status_code != 200 and response.status_code != 201:
            print(ColorOutput.DEBUG_TAG + ": port a " + str(port_a) + " port b " + str(port_b))
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)
        pass

    def create_router(self):
        response = self.nm.gns3_request_get("/templates")
        if response.status_code != 200 and response.status_code != 201 :
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)
        response = response.json()

        for i in range(0,len(response)):
            if response[i]['name'].find("BIRD") != -1:
                self.router = response[i]
        response = self.nm.gns3_request_post('/projects/' + self.nm.selected_project['project_id'] + '/templates/' + self.router['template_id'], {'x':350,'y':100})
        if response.status_code != 200 and response.status_code != 201 :
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)
        pass

    def link_lan_to_router(self):
        port_switch = self.list_switch[0].response['properties']['ports_mapping'][-1]['port_number']
        router_id = None
        for node in self.nm.get_all_nodes():
            if node['name'].find('BIRD') != -1:
                router_id = node['node_id']

        if router_id == None:
            print(ColorOutput.ERROR_TAG + ": Not found the bird router")
            exit(1)

        payload = {"nodes": [{"adapter_number": 1, "node_id": router_id, "port_number": 0},
                             {"adapter_number": 0, "node_id": self.list_switch[0].get_id(), "port_number": port_switch}]}
        response = self.nm.gns3_request_post('/projects/' + self.nm.selected_project['project_id'] + '/links', payload)

        if response.status_code != 200 and response.status_code != 201:
            print(ColorOutput.DEBUG_TAG + ": port a " + str(1) + " port b " + str(port_switch))
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)
        pass

    def create_template(self, template_name, x = 0, y = 0):
            response = self.nm.gns3_request_get("/templates")
            if response.status_code != 200 and response.status_code != 201 :
                print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
                exit(1)
            response = response.json()

            template_object = None
            found_name = []
            for i in range(0,len(response)):
                if response[i]['name'].find(template_name) != -1:
                    found_name.append(response[i]['name'])
                    template_object = response[i]

            if len(found_name) == 0:
                print(ColorOutput.ERROR_TAG + ': No occurrence of name "' + template_name + '"')
                exit(1)

            if len(found_name) > 1:
                print(ColorOutput.ERROR_TAG + ': More than 2 occurrences of name "' + template_name + '" :')
                for name in found_name:
                    print(name)
                exit(1)

            response = self.nm.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/templates/' + template_object['template_id'],{'x':x,'y':y,'compute_id':"local"}) # TODO Manage compute_id
            if response.status_code != 200 and response.status_code != 201 :
                print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
                exit(1)
            pass
            return response.json()

    def create_template_id(self, template_id, x=0, y=0):
            response = self.nm.gns3_request_get("/templates")
            if response.status_code != 200 and response.status_code != 201 :
                print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
                exit(1)
            response = response.json()

            template_object = None
            found_name = []
            for i in range(0,len(response)):
                if response[i]['template_id'].find(template_id) != -1:
                    found_name.append(response[i]['name'])
                    template_object = response[i]

            if len(found_name) == 0:
                print(ColorOutput.ERROR_TAG + ': No occurrence of id "' + template_id + '"')
                exit(1)

            if len(found_name) > 1:
                print(ColorOutput.ERROR_TAG + ': More than 2 occurrences of id "' + template_id + '" :')
                for name in found_name:
                    print(name)
                exit(1)

            response = self.nm.gns3_request_post('/projects/' + self.nm.selected_project['project_id'] + '/templates/' + template_object['template_id'],{'x':x,'y':y,'compute_id':self.nm.selected_machine['compute_id']})
            # TODO Manage compute_id
            if response.status_code != 200 and response.status_code != 201 :
                print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
                exit(1)
            pass
            return response.json()

    def link_nodes(self, id1, id2, adpt_port1 = [0,0], adpt_port2 = [0,0]):
        payload = {"nodes": [{"adapter_number": adpt_port1[0], "node_id": id1, "port_number": adpt_port1[1]},
                             {"adapter_number": adpt_port2[0], "node_id": id2, "port_number": adpt_port2[1]}]}

        response = self.nm.gns3_request_post('/projects/' + self.nm.selected_project['project_id'] + '/links',payload)
        if response.status_code != 200 and response.status_code != 201 :
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)
        return response.json()

    def simple_file_copy(self, node_id, path, text):
        response = self.nm.gns3_request_data('/projects/' + self.nm.selected_project['project_id'] + '/nodes/' + node_id + '/files/' + path, text)
        if response.status_code != 200 and response.status_code != 201 :
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)
        return response

    def start_node(self, node_id):
        response = self.nm.gns3_request_data('/projects/' + self.nm.selected_project['project_id'] + '/nodes/' + node_id + '/start', {})
        if response.status_code != 200 and response.status_code != 201 :
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)
        pass

    def delete_node(self, node_id):
        response = self.nm.gns3_request_delete('/projects/' + self.nm.selected_project['project_id'] + '/nodes/' + node_id)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 204 :
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)
        pass

    def delete_link(self, node_id):
        response = self.nm.gns3_request_delete('/projects/' + self.nm.selected_project['project_id'] + '/links/' + node_id)
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 204 :
            print(ColorOutput.ERROR_TAG + ': simple_topology: ' + str(response) + "\n-> " + response.text)
            exit(1)
        pass
