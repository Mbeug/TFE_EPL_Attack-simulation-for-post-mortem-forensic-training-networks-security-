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
        """
               Description
               -----------
               Class to communicate with the gns3 server.
        """
        self.projects = self.get_all_project()
        self.selected_project = self.set_current_project()
        self.list_machines = self.get_all_machines()
        self.list_gns3vm = self.get_all_gns3vm()
        self.list_nodes = self.get_all_nodes()
        self.selected_machine = self.set_current_machine()

    ####################################################################################################################
    #                                              HTTP REQUEST                                                        #
    ####################################################################################################################
    def gns3_request_get(self, endpoint):
        """
        The method request GET
        ===========
        Request GET on the gns3 server.

        :param endpoint: the endpoint's path where the request GET is to be made
        :type endpoint: str
        :return: Response from the requests class of the GET request at the endpoint
        :rtype : requests.models.Response

        :Example:
        >>> self.gns3_request_get('/gns3vm/engines')
        <Response [200]>
        >>> self.gns3_request_get('path/unknown') # when the path is unknown by the server the response is 400
        <Response [400]>
        """
        return requests.get(gns3_url+endpoint, auth=(gns3_user, gns3_password))

    def gns3_request_post(self, endpoint, payload):
        """
        The method request POST
        =======================
        Request POST on the gns3 server.

        :param endpoint: the endpoint's path where the request POST is to be made
        :param payload: the data in json format
        :type endpoint: str
        :type payload: dict
        :return: Response from the requests class of the POST request at the endpoint
        :rtype: requests.models.Response

        :Example:

        .. todo:: Add the example to the doc
        """
        return requests.post(gns3_url+endpoint, json=payload, auth=(gns3_user, gns3_password))

    def gns3_request_data(self, endpoint, payload):
        """
        The method request POST
        =======================
        Request POST on the gns3 server.

        :param endpoint: the endpoint's path where the request POST is to be made
        :param payload: the data in str format
        :type endpoint: str
        :type payload: str
        :return: Response from the requests class of the POST request at the endpoint
        :rtype: requests.models.Response

        :Example:

        .. todo:: Add the example to the doc
        """
        return requests.post(gns3_url+endpoint, data=payload, auth=(gns3_user, gns3_password))

    def gns3_request_put(self, endpoint, payload):
        """
        The method request PUT
        ======================
        Request PUT on the gns3 server.

        :param endpoint: the endpoint's path where the request PUT is to be made
        :param payload: the data in json format
        :type endpoint: str
        :type payload: dict
        :return: Response from the requests class of the PUT request at the endpoint
        :rtype: requests.models.Response

        :Example:

        .. todo:: Add the example to the doc
        """
        return requests.put(gns3_url+endpoint, json=payload, auth=(gns3_user, gns3_password))

    def gns3_request_delete(self, endpoint):
        """
        The method request DELETE
        ===========================
        Request DELETE on the gns3 server.

        :param endpoint: the endpoint's path where the request DELETE is to be made
        :type endpoint: str
        :return: Response from the requests class of the DELETE request at the endpoint
        :rtype: requests.models.Response

        :Example:

        .. todo:: Add the example to the doc
        """
        return requests.delete(gns3_url+endpoint, auth=(gns3_user, gns3_password))


    ####################################################################################################################
    #                                           ENDPOINT METHOD                                                        #
    ####################################################################################################################

    # ENDPOINT APPLIANCE/TEMPLATE
    ## TODO

    # ENDPOINT COMPUTE
    def get_all_gns3vm(self):
        response = self.gns3_request_get('/gns3vm/engines').json()
        vms = list(map(lambda tmp: {'compute_id':tmp['engine_id'],'name':tmp['name']}, response))
        return vms

    # ENDPOINT GNS3 VM
    def get_all_machines(self):
        response = self.gns3_request_get('/computes').json()
        pcs = list(map(lambda tmp: {'compute_id': tmp['compute_id'], 'name': tmp['name']}, response))
        return pcs

    def get_one_machine(self, compute_id):
        res = {}
        for machine in self.list_machines:
            if compute_id == machine.compute_id:
                res = machine
        return res

    def set_current_machine(self):
        print("List of machines:")
        for id_machine in range(len(self.list_machines)):
            print('[', id_machine, ']', self.list_machines[id_machine]['name'], ' ',
                  self.list_machines[id_machine]['compute_id'])
        for id_vm in range(len(self.list_machines),len(self.list_machines)+len(self.list_gns3vm)):
            print('[',id_vm,']',self.list_gns3vm[id_vm-len(self.list_machines)]['name'],' ',self.list_gns3vm[id_vm-len(self.list_machines)]['compute_id'])

        return self.list_machines[int(input("choose the machine\n"))]

    # ENDPOINT DRAWING
    ## TODO

    # ENDPOINT LINK
    def link_nodes(self, id1, id2, adpt_port1=[0, 0], adpt_port2=[0, 0]):
        payload = {"nodes": [{"adapter_number": adpt_port1[0], "node_id": id1, "port_number": adpt_port1[1]},
                             {"adapter_number": adpt_port2[0], "node_id": id2, "port_number": adpt_port2[1]}]}
        response = self.nm.gns3_request_post('/projects/' + self.nm.selected_project['project_id'] + '/links', payload)
        if response.status_code != 200 and response.status_code != 201:
            print(ColorOutput.ERROR_TAG + ': network_manager : ' + str(response) + "\n-> " + response.text)
            exit(1)
        return response.json()

    def get_all_links(self):

        return self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/links')

    def get_one_links(self,link_id):

        return self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/links/'+link_id)

    def get_pcap_link(self,link_id):
        """
        The PCAP method
        ===============
        Stream the pcap capture file.

        :param link_id: Link UUID
        :return: Response from the gns3_request_get()
        """
        return self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/links/'+link_id+'/pcap')

    def start_capture_link(self,link_id):
        """
        The start capture link method.
        =======================
        Start capture on a link instance. By default we consider it as an Ethernet link

        :param link_id: Link UUID
        :return: Response from the gns3_request_get()
        """
        return self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/links/'+link_id+'/start_capture')

    def stop_capture_link(self,link_id):
        """
        The stop capture link
        ======================
        Stop capture on a link instance.

        :param link_id:
        :return:
        """
        response = self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/links/'+link_id+'/stop_capture')
        self.check_reponse(response)
        return response

    # ENDPOINT NODE
    def get_all_nodes(self):
        response = self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/nodes')
        self.check_reponse(response)
        response= response.json()
        return  list(map(lambda tmp : {"node_id" : tmp['node_id'],"name" : tmp["name"]}, response))

    def get_one_node_by_id(self, node_id):
        for node in self.list_nodes:
            if node["node_id"] == node_id:
                response = self.gns3_request_get('/projects/'+self.selected_project['project_id']+"/nodes/"+node_id)
                self.check_reponse(response)
                return response.json()
        print(ColorOutput.INFO_TAG+": Node is not in the list of nodes")
        return None

    def get_one_node_by_name(self,name):
        for node in self.list_nodes:
            if node["name"] == name:
                response = self.gns3_request_get('/projects/'+self.selected_project['project_id']+"/nodes/"+node["node_id"])
                self.check_reponse(response)
                return response.json()
        print(ColorOutput.INFO_TAG + ": Node is not in the list of nodes")
        return None

    def put_node(self,node_id, payload : dict):
        response = self.gns3_request_put('/projects/'+self.selected_project['project_id']+"/nodes/"+node_id, payload)
        self.check_reponse(response)
        pass

    def delete_node(self, node_id):
        response = self.gns3_request_delete('/projects/' + self.selected_project['project_id'] + '/nodes/' + node_id)
        self.check_reponse(response)
        pass
    def duplicate_node(self,node_id, pos):
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/nodes/' + node_id + '/duplicate',pos)
        self.check_reponse(response)
        pass

    def start_node(self, node_id):
        response = self.gns3_request_data('/projects/' + self.selected_project['project_id'] + '/nodes/' + node_id + '/start', {})
        self.check_reponse(response)
        pass

    def start_all_node(self):
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/nodes/start', {})
        self.check_reponse(response)
        pass

    def stop_all_node(self):
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/nodes/stop', {})
        self.check_reponse(response)
        pass

    def reload_all_node(self):
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/nodes/reload', {})
        self.check_reponse(response)
        pass

    def add_file_to_node(self, node_id, path, text):
        response = self.gns3_request_data('/projects/' + self.nm.selected_project['project_id'] + '/nodes/' + node_id + '/files/' + path, text)
        self.check_reponse(response)
        return response
    def get_link_node(self,node_id):
        response = self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/nodes/' + node_id + '/links')
        self.check_reponse(response)
        response = response.json()
        # TODO check the response and construct an appropiate dict
        return list(map(lambda tmp: {"node_id": tmp['node_id'], "name": tmp["name"]}, response))


    # ENDPOINT PROJECT
    def get_all_project(self):
        response = self.gns3_request_get('/projects')
        self.check_reponse(response)
        return response.json()

    def set_current_project(self):
        print("List of projects:")
        for id_project in range(len(self.projects)):
            print('[', id_project, '] ', self.projects[id_project]['name'], ' ',
                  self.projects[id_project]['project_id'])

        return self.projects[int(input('Choose your project \n'))]

    # ENDPOINT OTHER (server, snapshot, symbol)
    ## TODO if time

    ####################################################################################################################
    #                                            METHOD AUXILIARY                                                      #
    ####################################################################################################################
    def check_reponse(self, response):
        if response.status_code != 200 and response.status_code != 201 :
            print(ColorOutput.ERROR_TAG + ': network_manager  ' + str(response) + "\n-> " + response.text)
            exit(1)
        pass

