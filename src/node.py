from colorOutput import ColorOutput
from network_manager import NetworkManager


class Node:
    def __init__(self, network: NetworkManager, name, node_type, project_id, symbol, compute_id, pos='none', console_type='none'):
        self.network = network
        self.name = name
        self.type = node_type
        self.compute_id = compute_id
        self.project_id = project_id
        self.console_type = console_type
        self.symbol = symbol
        self.payload = {"name": self.name, "node_type": self.type, "compute_id": self.compute_id, "console_type":self.console_type, "symbol":self.symbol}
        self.response = None
        # self.build(pos)
        self.console = None
        self.flag_console_updated = False
        self.console_host = None
        self.flag_console_host_updated = False
        self.id = None
        self.flag_id_updated = False
        self.properties = None
        self.flag_properties_updated = False
        self.status = None
        self.flag_status_updated = False
        self.position = pos
        self.flag_position_updated = False
        self.list_ports = None
        self.flag_list_ports_updated = False

    def build(self):
        response = self.node_request(self.payload)
        if response.status_code != 200 and response.status_code != 201:
            print(ColorOutput.ERROR_TAG + ': network_manager: ' + str(response) + "\n-> " + response.text)
            exit(1)
        self.response = response.json()
        self.console = self.get_console()
        self.console_host = self.get_console_host()
        self.console_type = self.get_console_type()
        self.id = self.get_id()
        self.properties = self.get_properties()
        self.status = self.get_status()
        self.position = self.get_position()
        self.list_ports = self.get_list_ports()
        pass

    def node_request(self, payload, id='none'):
        if id != 'none':
            response = self.network.gns3_request_put('/projects/' + self.project_id + '/nodes/' + str(id), payload)
        else :
            response = self.network.gns3_request_post('/projects/' + self.project_id + '/nodes', payload)
        return response

    def get_console(self):
        return self.response['console']

    def get_console_host(self):
        return self.response['console_host']

    def get_console_type(self):
        return self.response['console_type']

    def get_id(self):
        return self.response['node_id']

    def get_properties(self):
        return self.response['properties']

    def get_status(self):
        return self.response['status']

    def get_position(self):
        return self.response['x'], self.response['y']

    def get_list_ports(self):
        if 'ports' in self.response :
            return self.response['ports']
        else :
            return None

    def set_console(self, console):
        self.console = console
        self.flag_console_updated = True
        self.update_node()
        pass

    def set_console_host(self, console_host):
        self.console_host = console_host
        self.flag_console_host_updated = True
        self.update_node()
        pass

    def set_console_type(self, console_type):
        self.payload = console_type
        self.update_node()
        pass

    def set_id(self, node_id):
        self.payload = node_id
        self.flag_id_updated = True
        self.update_node()
        pass

    def set_properties(self, properties):
        self.payload = properties
        self.flag_position_updated = True
        self.update_node()
        pass

    def set_status(self, status):
        self.status = status
        self.flag_status_updated = True
        self.update_node()
        pass

    def set_position(self, pos):
        self.position = pos
        self.flag_position_updated = True
        self.update_node()
        pass

    def set_ports(self,list_ports):
        if  'ports' in self.response :
            self.list_ports = list_ports
            self.flag_list_ports_updated = True
            self.update_node()
        pass

    def update_node(self):
        if self.flag_console_updated :
            self.payload.update({'console':self.console})
            self.flag_console_updated = False
        elif self.flag_console_host_updated :
            self.payload.update({'console_host': self.console_host})
            self.flag_console_host_updated = False
        elif self.flag_id_updated :
            self.payload.update({'node_id':self.id})
            self.flag_id_updated = False
        elif self.flag_properties_updated :
            self.payload.update({'properties':self.properties})
            self.flag_properties_updated = False
        elif self.flag_status_updated :
            self.payload.update({'status':self.status})
            self.flag_status_updated = False
        elif self.flag_position_updated :
            self.payload.update({
                'x' : self.position[0],
                'y' : self.position[1]
            })
            self.flag_position_updated = False
        elif self.flag_list_ports_updated :
            self.payload.update({'properties' : self.list_ports})
            self.flag_list_ports_updated = False
        else:
            pass

        response = self.node_request(self.payload,self.id)
        if response.status_code != 200 and response.status_code != 201:
            if response.status_code != 200 and response.status_code != 201:
                print(ColorOutput.ERROR_TAG + ': node: ' + str(response) + "\n-> " + response.text)
                exit(1)
        pass