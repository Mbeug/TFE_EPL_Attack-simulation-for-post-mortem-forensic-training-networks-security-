from colorOutput import ColorOutput
from newtwork_manager import NetworkManager


class Node:
    def __init__(self, network: NetworkManager, name, node_type, project_id, symbol, pos='none', compute_id='local', console_type='none'):
        self.network = network
        self.name = name
        self.type = node_type
        self.compute_id = compute_id
        self.project_id = project_id
        self.console_type = console_type
        self.symbol = symbol
        self.payload = {"name": self.name, "node_type": self.type, "compute_id": self.compute_id, "console_type":self.console_type, "symbol":self.symbol}
        self.response = None
        self.build(pos)
        self.console = self.get_console()
        self.console_host = self.get_console_host()
        self.id = self.get_id()
        self.properties = self.get_properties()
        self.status = self.get_status()
        self.position = self.get_position()

    def build(self, pos='none'):
        if pos != 'none':
            self.set_position(pos)
        response = self.node_request(self.payload)
        if response.status_code != 200 and response.status_code != 201:
            print(ColorOutput.ERROR_TAG + ': network_manager: ' + str(response) + "\n-> " + response.text)
            exit(1)
        self.response = response.json()
        pass

    def node_request(self, payload):
        response = self.network.gns3_req_param('/projects/' + self.project_id + '/nodes', payload)
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

    def set_console(self, console):
        self.payload.update({'console': console})
        self.build()
        pass

    def set_console_host(self, console_host):
        self.payload.update({'console_host': console_host})
        self.build()
        pass

    def set_console_type(self, console_type):
        self.payload.update({'console_type': console_type})
        self.build()
        pass

    def set_id(self, node_id):
        self.payload.update({'node_id': node_id})
        self.build()
        pass

    def set_properties(self, properties):
        self.payload.update({'properties': properties})
        self.build()
        pass

    # def set_status(self, status):
    #     self.payload.update({'status': status})
    #     self.build()
    #     pass

    def set_position(self, pos):
        self.payload.update({'x': pos[0], 'y': pos[1]})
        # self.build()
        pass