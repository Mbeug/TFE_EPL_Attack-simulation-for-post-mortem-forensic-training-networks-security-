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
        self.nm = NetworkManager()
        self.dm = DockerManager()
        pass

