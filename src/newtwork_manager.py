import configparser
import os

import requests

from colorOutput import ColorOutput

home_dir = os.path.expanduser("~")
config_server = configparser.ConfigParser()
config_server.read_file(open(home_dir+"/.config/GNS3/2.2/gns3_server.conf"))

section = "Server"
gns3_user = config_server.get(section, "user")
gns3_password = config_server.get(section, "password")
gns3_host = config_server.get(section, "host")
gns3_port = config_server.get(section, "port")
gns3_url = 'http://'+gns3_user+'@'+gns3_host+':'+gns3_port+'/v2'
print(ColorOutput.INFO_TAG+": you are connected to "+gns3_url)


class NetworkManager:

    def __init__(self):
        self.projects = self.get_all_project()
        self.selected_project = self.set_current_project()
        self.list_machines = self.get_all_machines()
        self.list_gns3vm = self.get_all_gns3vm()
        self.list_nodes = self.get_all_nodes()
        self.selected_machines = self.set_current_machine()
    def gns3_request(self, endpoint):
        return requests.get(gns3_url+endpoint, auth=(gns3_user, gns3_password))

    def gns3_req_param(self, endpoint, payload):
        return requests.post(gns3_url+endpoint, json=payload, auth=(gns3_user, gns3_password))

    def get_all_project(self):
        return self.gns3_request('/projects').json()

    def get_all_gns3vm(self):
        return self.gns3_request('/gns3vm/engines').json()

    def get_all_machines(self):
        return self.gns3_request('/computes').json()

    def get_one_machine(self, compute_id):
        res = {}
        for machine in self.list_machines:
            if compute_id == machine.compute_id:
                res = machine
        return res

    def get_all_nodes(self):
        return self.gns3_request('/projects/' + self.selected_project['project_id'] + '/nodes')

    def get_one_node(self, node_id):
        res = {}
        for node in self.list_nodes:
            if node_id == node.node_id:
                res = node
        return res

    def set_current_project(self):
        print("List of projects:")
        for id_project in range(len(self.projects)):
            print('[', id_project, '] ', self.projects[id_project]['name'], ' ',
                  self.projects[id_project]['project_id'])

        return self.projects[int(input('Choose your project \n'))]

    def set_current_machine(self):
        print("List of machines:")
        for id_machine in range(len(self.list_machines)):
            print('[', id_machine, ']', self.list_machines[id_machine]['name'], ' ',
                  self.list_machines[id_machine]['compute_id'])
            return self.list_machines[int(input("choose the machine\n"))]
        pass

    def start(self):
        self.gns3_req_param('/projects/' + self.selected_project['project_id'] + '/nodes/start', {})
        pass

    def stop(self):
        self.gns3_req_param('/projects/' + self.selected_project['project_id'] + '/nodes/stop', {})
        pass

