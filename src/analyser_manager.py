from network_manager import NetworkManager


class AnalyserManager:
    """
        This class is used to manage the analysis of the network
    """
    def __init__(self,networkManager:NetworkManager):
        self.nm = networkManager
        pass

    def start_nodes(self):
        """
        This method call the :py:meth:`~network_manager.start_all_nodes` method in :py:class:`network_manager`. It start all nodes of our topology.
        """
        self.nm.start_all_nodes()
        pass

    def stop_nodes(self):
        """
        This method call the :py:meth:`~network_manager.stop_all_nodes` method in :py:class:`network_manager`. It stop all nodes of our topology.
        """
        self.nm.stop_all_node()
        pass

    def start(self, node):
        """
        This method call the :py:meth:`~network_manager.start_node` method in :py:class:`network_manager`. It start a specific node of our topology.

        :param node: The specific node

        """
        self.nm.start_node(node['node_id'])
        pass

    def stop(self, node):
        """
        This method call the :py:meth:`~network_manager.stop_node` method in :py:class:`network_manager`. It stop the specific node of our topology.

        :param node: The specific node

        """
        self.nm.stop_node(node['node_id'])
        pass

    def start_all_capture(self):
        """
        This method apply on all links of our network the :py:meth:`~network_manager.start_capture_link` method of the :py:class:`network_manager`.
        It start the capture on all links.

        .. note:: The pcap file is stored in the capture directory of the GNS3 project
        """
        link_list = self.get_all_link()

        for link in link_list:
            self.nm.start_capture_link(link['link_id'])
        pass

    def stop_all_capture(self):
        """
        This method apply on all links of our network the :py:meth:`~network_manager.stop_capture_link` method of the :py:class:`network_manager`.
        It stop the capture on all links.

        .. note:: The pcap file is stored in the capture directory of the GNS3 project
        """
        link_list = self.get_all_link()
        for link in link_list:
            self.nm.stop_capture_link(link['link_id'])
        pass

    def start_capture_btw(self, nodeA, nodeB):
        """
        This method start a capture with the :py:meth:`~network_manager.start_capture_link` method of the :py:class:`network_manager`

        :param nodeA: One of the nodes
        :param nodeB: One of the nodes

        .. note:: The pcap file is stored in the capture directory of the GNS3 project
        .. warning:: nodeA and nodeB must be next to each other
        """
        link_list = self.get_all_link()
        for link in link_list:
            if (link['nodes'][0] == nodeA and link['nodes'][1] == nodeB) or (link['nodes'][0]==nodeB and link['nodes'][1]==nodeA):
                self.nm.start_capture_link(link['link_id'])
        pass

    def stop_capture_btw(self, nodeA, nodeB):#node must be next to each other
        """
        This method stop a capture with the :py:meth:`~network_manager.stop_capture_link` method of the :py:class:`network_manager`

        :param nodeA: One of the nodes
        :param nodeB: One of the nodes

        .. note:: The pcap file is stored in the capture directory of the GNS3 project
        .. warning:: nodeA and nodeB must be next to each other
        """
        link_list = self.get_all_link()
        for link in link_list:
            if (link['nodes'][0] == nodeA and link['nodes'][1] == nodeB) or (link['nodes'][0]==nodeB and link['nodes'][1]==nodeA):
                self.nm.stop_capture_link(link['link_id'])
        pass

    def start_capture_node(self, node):
        """
        This method start a capture on all links of one specific node with :py:meth:`~network_manager.start_capture_link` in :py:class:`network_manager`

        :param node: The specific node

        .. note:: The pcap file is stored in the capture directory of the GNS3 project
        """
        link_list = self.nm.get_link_node(node['node_id'])
        for link in link_list:
            self.nm.start_capture_link(link['link_id'])
        pass

    def stop_capture_node(self, node):
        """
        This method stop a capture on all links of one specific node with :py:meth:`~network_manager.stop_capture_link` in :py:class:`network_manager`

        :param node: The specific node

        .. note:: The pcap file is stored in the capture directory of the GNS3 project
        """
        link_list = self.nm.get_link_node(node['node_id'])
        for link in link_list:
            self.nm.stop_capture_link(link['link_id'])
        pass

    def get_all_link(self):
        """
        This method allows you to retrieve all the links of the topology.

        :return: A list of all links
        """
        list_link = []
        for node in self.nm.get_all_nodes():
            tmp = self.nm.get_link_node(node['node_id'])
            for link in tmp:
                skip = False
                for present_link in list_link:
                    if present_link['link_id'] == link['link_id']:
                        skip = True
                if not skip :
                    list_link.append(link)
        return list_link
