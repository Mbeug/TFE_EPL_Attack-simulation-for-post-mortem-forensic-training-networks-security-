from docker_manager import DockerManager
from network_manager import NetworkManager
from node import Node


class TopologyManager:
    """
    Class to manage the topology of any network we want on the gns3 server
    """
    def __init__(self):
        self.nm = NetworkManager()
        self.dm = DockerManager()
        pass

