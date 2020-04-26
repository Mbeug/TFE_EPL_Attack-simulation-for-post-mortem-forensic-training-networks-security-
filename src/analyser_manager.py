from network_manager import NetworkManager


class AnalyserManager:
    def __init__(self,networkManager:NetworkManager):
        self.nm = networkManager
        pass

    def start_nodes(self):
        self.nm.start_all_nodes()
        pass

    def stop_nodes(self):
        self.nm.stop_all_node()
        pass

    def start(self, node):
        self.nm.start_node(node['node_id'])
        pass

    def stop(self, node):
        self.nm.stop_node(node['node_id'])
        pass

    def start_all_capture(self):
        link_list = self.get_all_link()

        for link in link_list:
            self.nm.start_capture_link(link['link_id'])
        pass

    def stop_all_capture(self):
        link_list = self.get_all_link()
        for link in link_list:
            self.nm.stop_capture_link(link['link_id'])
        pass

    def start_capture_btw(self, nodeA, nodeB):
        link_list = self.get_all_link()
        for link in link_list:
            if (link['nodes'][0] == nodeA and link['nodes'][1] == nodeB) or (link['nodes'][0]==nodeB and link['nodes'][1]==nodeA):
                self.nm.start_capture_link(link['link_id'])
        pass

    def stop_capture_btw(self, nodeA, nodeB):
        link_list = self.get_all_link()
        for link in link_list:
            if (link['nodes'][0] == nodeA and link['nodes'][1] == nodeB) or (link['nodes'][0]==nodeB and link['nodes'][1]==nodeA):
                self.nm.stop_capture_link(link['link_id'])
        pass

    def get_all_link(self):
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
