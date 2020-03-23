from colorOutput import ColorOutput
from docker_manager import DockerManager
from network_manager import NetworkManager
from node import Node


class TopologyManager:
    """
    Class to manage the topology of any network we want on the gns3 server
    must be done:
        add n docker
        link to switch (with n interfaces)
        add router
        add server
        add creator netconfig
        manage the position
        add NAT

    """
    def __init__(self):
        self.nm = NetworkManager(0,{
                "compute_id": "vm",
                "name": "GNS3 VM (GNS3 VM)"
            })
        self.dm = DockerManager('vm')
        self.max_x = 1000  # That's means we have 10 columns
        #self.max_y = 10000 # That's means we have 100 rows
        self.list_pcs= []
        pass


    def set_max_x(self, new_x:int):
        self.max_x = new_x
        pass

    def set_max_y(self, new_y:int):
        self.max_y = new_y
        pass

    def create_n_node(self, n:int, template_name: str = None, docker_name: str = None, docker_img:str =None):
        if template_name == None and docker_img == None:
            print(ColorOutput.ERROR_TAG+': Please fill arg template_name or docker_name with its image')
            exit(1)

        switch = self.nm.create_template_by_name("Ethernet switch",self.max_x - 100, int(n * 100 / 2))
        nb_add_port = n - 7
        if nb_add_port > 0:
            for i in range(8, 8 + nb_add_port):
                switch['properties']['ports_mapping'].append(
                    {'name': 'Ethernet' + str(i), 'port_number': i, 'type': 'access', 'vlan': 1})

        self.nm.put_node(switch['node_id'],{'properties':switch['properties']})

        if template_name!= None:
            for i in range(n):
                current_pc = self.nm.create_template_by_name(template_name,self.max_x,i*100)
                self.nm.link_nodes(switch['node_id'],current_pc['node_id'],[0,i+1],[0,0])
                self.list_pcs.append(current_pc)

        if docker_name != None and docker_img == None :
            print(ColorOutput.ERROR_TAG+': Please give the docker\'s image')
        if docker_name != None and docker_img != None:
            for i in range(n):
                current_docker = self.nm.create_docker_template(docker_name, docker_img)
                self.nm.link_nodes(switch['node_id'],current_docker['node_id'],[0,i],[0,0])
                self.list_pcs.append(current_docker)

        pass

    def create_router(self):
        switch= self.nm.get_one_node_by_name("Switch")

        router =  self.nm.create_template_by_name("BIRD",switch['x']-100,switch['y'])

        self.nm.link_nodes(switch['node_id'],router['node_id'],[0,0],[0,0])
        pass

    def clean(self):
        list_nodes = self.nm.get_all_nodes()
        for node in list_nodes:
            self.nm.delete_node(node['node_id'])