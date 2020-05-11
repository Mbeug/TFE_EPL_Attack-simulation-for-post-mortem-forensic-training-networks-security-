import configparser
import os

import requests

from colorOutput import ColorOutput
from utility import Utility

home_dir = os.path.expanduser("~")
config_server = configparser.ConfigParser()
config_server.read_file(open(home_dir+"/.config/GNS3/2.2/gns3_server.conf"))

section = "Server"
gns3_user = config_server.get(section, "user")
gns3_password = config_server.get(section, "password")
gns3_host = config_server.get(section, "host")
gns3_port = config_server.get(section, "port")
gns3_url = 'http://'+gns3_user+'@'+gns3_host+':'+gns3_port+'/v2'
print(ColorOutput.INFO_TAG+": you are connected to "+gns3_url+"\n")


class NetworkManager:
    """
    Class to communicate with the gns3 server.
    """
    selected_machine: dict

    def __init__(self, id_project=None, id_machine = None):
        self.projects = self.get_all_project()
        self.selected_project = self.set_current_project(id_project)
        self.list_machines = self.get_all_machines()
        self.list_gns3vm = self.get_all_gns3vm()
        self.list_nodes = self.get_all_nodes()
        self.selected_machine = self.set_current_machine(id_machine)

    ####################################################################################################################
    #                                              HTTP REQUEST                                                        #
    ####################################################################################################################
    def gns3_request_get(self, endpoint):
        """
        Request GET on the gns3 server.

        :param endpoint: the endpoint's path where the request GET is to be made
        :type endpoint: str
        :return: Response from the requests class of the GET request at the endpoint
        :rtype: `requests.models.Response`

        Example::

            >>> gns3_request_get('/gns3vm/engines')
            >>> gns3_request_get('path/unknown')
            # when the path is unknown by the server the response is 400

        This will output:

        .. code-block:: none

            <Response [200]>
            <Response [400]>
        """
        return requests.get(gns3_url+endpoint, auth=(gns3_user, gns3_password))

    def gns3_request_post(self, endpoint, payload):
        """
        Request POST on the gns3 server.

        :param endpoint: the endpoint's path where the request POST is to be made
        :param payload: the data in json format
        :type endpoint: str
        :type payload: dict
        :return: Response from the requests class of the POST request at the endpoint
        :rtype: : `requests.models.Response`

        Example::

            >>> self.gns3_request_post('/projects/project_id/nodes',{'somedata':data})

        Output::

             <Response [200]>

        """
        return requests.post(gns3_url+endpoint, json=payload, auth=(gns3_user, gns3_password))

    def gns3_request_data(self, endpoint, payload):
        """
        Request POST on the gns3 server.

        :param endpoint: the endpoint's path where the request POST is to be made
        :param payload: the data in str format
        :type endpoint: str
        :type payload: str
        :return: Response from the requests class of the POST request at the endpoint
        :rtype: :`requests.models.Response`
        """
        return requests.post(gns3_url+endpoint, data=payload, auth=(gns3_user, gns3_password))

    def gns3_request_put(self, endpoint, payload):
        """
        Request PUT on the gns3 server.

        :param endpoint: the endpoint's path where the request PUT is to be made
        :param payload: the data in json format
        :type endpoint: str
        :type payload: dict
        :return: Response from the requests class of the PUT request at the endpoint
        :rtype: :`requests.models.Response`

        Example::

            >>> gns3_request_put('/projects/project_id/nodes/node_id',{'data':newData})

        Output ::
            <Response [200]>

        """
        return requests.put(gns3_url+endpoint, json=payload, auth=(gns3_user, gns3_password))

    def gns3_request_delete(self, endpoint):
        """
        Request DELETE on the gns3 server.

        :param endpoint: the endpoint's path where the request DELETE is to be made
        :type endpoint: str
        :return: Response from the requests class of the DELETE request at the endpoint
        :rtype: :`requests.models.Response`

        Example::

            >>> gns3_request_delete('/projects/project_id/nodes/node_id')

        Output::

            <Response [200]>

        """
        return requests.delete(gns3_url+endpoint, auth=(gns3_user, gns3_password))


    ####################################################################################################################
    #                                           ENDPOINT METHOD                                                        #
    ####################################################################################################################

    # ENDPOINT APPLIANCE/TEMPLATE
    def create_docker_template(self, name, image):
        """
        Method create a docker template

        :param name: is the name of docker we want
        :param image:  is the image of docker we want
        :type name: str
        :type image: str
        :return:

        payload example ::

            payload = { 'default_name_format': '{name}-{0}',
                        'usage': '',
                        'symbol': ':/symbols/docker_guest.svg',
                        'category': 'guest',
                        'start_command': '',
                        'name': 'ubuntu',
                        'image': 'ubuntu:latest',
                        'adapters': 1,
                        'custom_adapters': [],
                        'environment': '',
                        'console_type': 'telnet',
                        'console_auto_start': False,
                        'console_resolution': '1024x768',
                        'console_http_port': 80,
                        'console_http_path': '/',
                        'extra_hosts': '',
                        'extra_volumes': [],
                        'compute_id': 'local',
                        'template_id': 'e8912fbb-2e50-43a3-8328-9e748dec1f89',
                        'template_type': 'docker'
                        }

        """
        for template in self.get_all_templates():
            if template["name"] == name:
                print(ColorOutput.INFO_TAG + ' Template "'+name+'" already exist, not created again')
                return None
        response = self.gns3_request_post('/templates',payload = {'name': name, 'image': image,'compute_id': self.selected_machine['compute_id'], 'template_type': 'docker'})
        self.check_reponse(response)
        return response.json()

    def get_all_templates(self):
        """
        Request the gns3 server a list of all templates

        :return: list of all templates
        :rtype: array of dict
        """
        response = self.gns3_request_get("/templates")
        if response.status_code != 200 and response.status_code != 201:
            print(ColorOutput.ERROR_TAG + ': NetworkManager (L:141): ' + str(response) + "\n-> " + response.text)
            exit(1)
        return response.json()

    def create_template_by_name(self, template_name, x = 0, y = 0):
        """
        Create a specific template by its name

        :param template_name: the name of the template asked
        :param x: abscissa coordinate
        :param y: ordinate coordinate
        :type template_name: str
        :type x: int
        :type y: int
        :return: the response of the template post request
        :rtype: : `requests.models.Response`
        """
        list_templates = self.get_all_templates()
        template_object = None
        found_name = []
        for i in range(0,len(list_templates)):
            if list_templates[i]['name'].find(template_name) != -1:
                found_name.append(list_templates[i]['name'])
                template_object = list_templates[i]

        if len(found_name) == 0:
            print(ColorOutput.ERROR_TAG + ': No occurrence of name "' + template_name + '"')

            if Utility.ask_user_boolean("If is a docker template, do you want to add '"+template_name+"' to the project templates?") :
                template_object = self.create_docker_template(template_name,template_name)
            else :
                exit(1)

        if len(found_name) > 1:
            print(ColorOutput.ERROR_TAG + ': More than 2 occurrences of name "' + template_name + '" :')
            for name in found_name:
                print(name)
            exit(1)

        response = self.post_template(template_object,x,y)
        return response

    def create_template_by_id(self, template_id, x=0, y=0):
        """
        Create a specific template by its name

        :param template_id: the id of the template asked
        :param x: abscissa coordinate
        :param y: ordinate coordinate
        :type template_name: str
        :type x: int
        :type y: int
        :return: the response of the template post request
        :rtype: dict
        """
        list_templates= self.get_all_templates()
        template_object = None
        found_name = []
        for i in range(0, len(list_templates)):
            if list_templates[i]['template_id'].find(template_id) != -1:
                found_name.append(list_templates[i]['name'])
                template_object = list_templates[i]

        if len(found_name) == 0:
            print(ColorOutput.ERROR_TAG + ': No occurrence of id "' + template_id + '"')
            exit(1)

        if len(found_name) > 1:
            print(ColorOutput.ERROR_TAG + ': More than 2 occurrences of id "' + template_id + '" :')
            for name in found_name:
                print(name)
            exit(1)

        response = self.post_template(template_object,x,y)
        return response

    def post_template(self,template_object,x,y):
        """
        This method add to the project the template with the post method

        :param template_object: the object template
        :param x: abscissa coordinate
        :param y: ordinate coordinate
        :type template_object: dict
        :type x: int
        :type y: int
        :return: the response of the post server request
        :rtype: dict
        """
        response = self.gns3_request_post(
            '/projects/' + self.selected_project['project_id'] + '/templates/' + template_object['template_id'],
            {'x': x, 'y': y, 'compute_id': self.selected_machine['compute_id']})
        self.check_reponse(response)
        return response.json()

    # ENDPOINT COMPUTE/VM
    def get_all_gns3vm(self):
        """
        This method list all gsn3vm

        :return: a list of the all gns3 vm
        :rtype: list
        """
        response = self.gns3_request_get('/gns3vm/engines').json()
        vms = list(map(lambda tmp: {'compute_id':tmp['engine_id'],'name':tmp['name']}, response))
        return vms

    # ENDPOINT GNS3 VM
    def get_all_machines(self):
        """
        This method list all machines

        :return: a list of the all machines
        :rtype: list
        """
        response = self.gns3_request_get('/computes').json()
        pcs = list(map(lambda tmp: {'compute_id': tmp['compute_id'], 'name': tmp['name']}, response))
        return pcs

    def get_one_machine_by_id(self, compute_id):
        """
        This method get one machine by id

        :param compute_id: the compute's id
        :return: the object of the specific compute
        :rtype: dict
        """
        list_machines = self.get_all_machines()
        res = {}
        for machine in list_machines:
            if compute_id == machine['compute_id']:
                res = machine
        return res

    def get_one_machine_by_name(self,name):
        """
        This method get one machine by name

        :param name: the compute's name
        :return: the object of the specific compute
        :rtype: dict
        """
        list_machines = self.get_all_machines()
        res = {}
        for machine in list_machines:
            if name == machine['name']:
                res = machine
        return res

    #
    def set_current_machine(self, machine=None):
        """
        This method set the current machine is using

        :param machine: if is None the user must be choose the machine else this parameter specifies the machine
        :return: assign the value to .. self.selected_machine
        """
        if machine is None :
            print("List of machines:")
            for id_machine in range(len(self.list_machines)):
                print('[', id_machine, ']', self.list_machines[id_machine]['name'], ' ',
                      self.list_machines[id_machine]['compute_id'])

            for id_vm in range(len(self.list_machines),len(self.list_machines)+len(self.list_gns3vm)):
                print('[',id_vm,']',self.list_gns3vm[id_vm-len(self.list_machines)]['name'],' ',self.list_gns3vm[id_vm-len(self.list_machines)]['compute_id'])

            return self.list_machines[int(input("choose the machine\n"))]
        else:
            for id_machine in range(len(self.list_machines)):

                  if machine == self.list_machines[id_machine]['compute_id']:
                      return self.list_machines[id_machine]

            for id_vm in range(len(self.list_machines)):
                if machine == self.list_gns3vm[id_vm]['compute_id']:
                    return self.list_gns3vm[id_vm]

            return machine
        pass


    # ENDPOINT DRAWING
    def get_all_drawings(self):
        """
        This method ask to the gsn3 server all drawings

        :return: list of all drawings in the current project
        :rtype: array of dict
        """
        response = self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/drawings')
        self.check_reponse(response)
        return response.json()

    def post_drawing(self, payload:dict):
        """
        This method send the drawing to the gns3 server

        :param payload: the custom payload for the drawing
        :return: response from post request to the server

        Payload example:

        .. code-block :: javascript

            {
                "svg": '<svg height="210" width="500">
                <line x1="0" y1="0" x2="200" y2="200" style="stroke:rgb(255,0,0);stroke-width:2" /></svg>',
                "x":10,
                "y":20,
                "z": 0
            }

        """
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/drawings', payload)
        self.check_reponse(response)

    def get_drawing(self,drawing_id):
        """
        This method ask to the gns3 server a specific drawing.

        :param drawing_id: the id of specific drawing
        :return: the data about the specific drawing
        :rtype: dict
        """
        response = self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/drawings/'+drawing_id)
        self.check_reponse(response)
        return response.json()

    def put_drawing(self,drawing_id, payload):
        """
        This method update with the `payload` a specific drawing.

        :param drawing_id: the id of specific drawing
        :param payload: data structure containing the update of the drawing
        :return: update the specific drawing with the payload
        """
        response = self.gns3_request_put('/projects/' + self.selected_project['project_id'] + '/drawings/'+drawing_id,payload)
        self.check_reponse(response)

    def delete_drawing(self,drawing_id):
        """
        This method delete a specific drawing.

        :param drawing_id: the id of specific drawing
        :return: delete the specific drawing
        """
        response = self.gns3_request_delete('/projects/' + self.selected_project['project_id'] + '/drawings/'+drawing_id)
        self.check_reponse(response)

    # ENDPOINT LINK
    def link_nodes(self, id1, id2, adapter_port1=None, adapter_port2=None):
        """
        This method link two nodes together

        :param id1: first id node
        :param id2: second id node
        :param adapter_port1: first adapter port node
        :param adapter_port2: second adapter port node
        :return: the response of the post request on gns3 server
        :rtype: dict
        """
        if adapter_port2 is None:
            adapter_port2 = [0, 0]
        if adapter_port1 is None:
            adapter_port1 = [0, 0]

        payload = {"nodes": [{"adapter_number": adapter_port1[0], "node_id": id1, "port_number": adapter_port1[1]},
                             {"adapter_number": adapter_port2[0], "node_id": id2, "port_number": adapter_port2[1]}]}
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/links', payload)
        self.check_reponse(response)
        return response.json()

    def delete_link(self, link_id):
        """
        This method delete the specific link

        :param link_id: the id of link must be deleted
        :return: the response of the gns3 server of the delete request
        :rtype: : `requests.models.Response`
        """
        response = self.gns3_request_delete('/projects/' + self.selected_project['project_id'] + '/links/' + link_id)
        self.check_reponse(response)
        return response

    def get_all_links(self):
        """
        This method list all links in the current project

        :return: list of all links
        :rtype: array of dict

        """
        response = self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/links')
        self.check_reponse(response)
        return response.json()

    def get_one_link(self,link_id):
        """
        This method get one specific link in the current project

        :param link_id: the id of the specific link
        :return: the response of the get method with the specific link
        :rtype: dict
        """
        response = self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/links/'+link_id)
        self.check_reponse(response)
        return response.json()

    def get_pcap_link(self,link_id):
        """
        Stream the pcap capture file.

        :param link_id: Link UUID
        :return: Response from the :func:`network_manager.gns3_request_get()`
        """
        response = self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/links/'+link_id+'/pcap')
        self.check_reponse(response)
        return response

    def start_capture_link(self,link_id):
        """
        Start capture on a link instance. By default we consider it as an Ethernet link

        :param link_id: Link UUID
        :return: Response from the :func: `network_manager.gns3_request_get()` and start the capture packets
        """
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/links/'+link_id+'/start_capture',{})
        self.check_reponse(response)
        return response

    def stop_capture_link(self,link_id):
        """
        Stop capture on a link instance.

        :param link_id: Link UUID
        :return: Response from the :func:`network_manager.gns3_request_get()` and stop the capture packets
        """
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/links/'+link_id+'/stop_capture',{})
        self.check_reponse(response)
        return response

    # ENDPOINT NODE
    def get_all_nodes(self):
        """
        This method ask the gns3 server to get the node repository

        :return: A list of all nodes of the current project (`selected_project`)
        """
        response = self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/nodes')
        self.check_reponse(response)
        response= response.json()
        return  list(map(lambda tmp : {"node_id" : tmp['node_id'],"name" : tmp["name"]}, response))

    def get_one_node_by_id(self, node_id):
        """
        This method get a specific node by its id

        :param node_id: The node's id
        :return: The specific node and none if the node isn't founded
        :rtype: dict
        """
        list_nodes = self.get_all_nodes()
        for node in list_nodes:
            if node["node_id"] == node_id:
                response = self.gns3_request_get('/projects/'+self.selected_project['project_id']+"/nodes/"+node_id)
                self.check_reponse(response)
                return response.json()
        print(ColorOutput.INFO_TAG+": Node is not in the list of nodes")
        return None

    def get_one_node_by_name(self,name):
        """
        This method get a specific node by its name

        :param name: The node's name
        :return: The specific node and none if the node isn't founded
        :rtype: dict
        """
        list_nodes = self.get_all_nodes()
        for node in list_nodes:
            if name in node['name']:
                response = self.gns3_request_get('/projects/'+self.selected_project['project_id']+"/nodes/"+node["node_id"])
                self.check_reponse(response)
                return response.json()
        print(ColorOutput.INFO_TAG + ": Node is not in the list of nodes")
        return None

    def put_node(self,node_id, payload : dict):
        """
        This method put the payload on the specific node

        :param node_id: The node's id of the specific node
        :param payload: the payload of the update of the specific node
        :return: update the node on the gns3 server
        """
        response = self.gns3_request_put('/projects/'+self.selected_project['project_id']+"/nodes/"+node_id, payload)
        self.check_reponse(response)
        return response

    def delete_node(self, node_id):
        """
        This method make the delete request to the gns3 server

        :param node_id: The id of the node must be deleted
        :return: delete the specific node
        """
        response = self.gns3_request_delete('/projects/' + self.selected_project['project_id'] + '/nodes/' + node_id)
        self.check_reponse(response)
        pass
    def duplicate_node(self,node_id, pos):
        """
        This method make a request to the gns3 server to duplicate the specific node

        :param node_id: the id of the specific node
        :param pos: the position where the duplicated node must be positioned
        :return: duplicate the specific node
        """
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/nodes/' + node_id + '/duplicate',pos)
        self.check_reponse(response)
        pass

    def start_node(self, node_id):
        """
        The method start the specific node

        :param node_id: the id of the specific node
        :return: start the specific node
        """
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/nodes/' + node_id + '/start', {})
        self.check_reponse(response)
        pass

    def stop_node(self, node_id):
        """
        The method stop the specific node

        :param node_id: the id od the specific node
        :return: stop the specific node
        """
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/nodes/' + node_id + '/stop', {})
        self.check_reponse(response)
        pass

    def start_all_nodes(self):
        """
        The method start all node in the current project

        :return: start all node
        """
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/nodes/start', {})
        self.check_reponse(response)
        pass

    def stop_all_node(self):
        """
        The method stop all node in the current project

        :return: stop all nodes
        """
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/nodes/stop', {})
        self.check_reponse(response)
        pass

    def reload_all_node(self):
        """
        The method reload all nodes

        :return: reload all nodes
        """
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] + '/nodes/reload', {})
        self.check_reponse(response)
        pass

    def add_file_to_node(self, node_id, path, text):
        """
        This method give a file to a specific node.

        :param node_id: the id of the specific node
        :param path: the path where the file must be put
        :param text: the content file
        :return: the response of gns3 server
        :rtype: : `requests.models.Response`
        """
        response = self.gns3_request_data('/projects/' + self.selected_project['project_id'] + '/nodes/' + node_id + '/files/' + path, text)
        self.check_reponse(response)
        return response

    def get_link_node(self,node_id):
        """
        The method give all link of a specific node.

        :param node_id: The id of the specific node
        :return: a list of all link
        :rtype: dict's array
        """
        response = self.gns3_request_get('/projects/' + self.selected_project['project_id'] + '/nodes/' + node_id + '/links')
        self.check_reponse(response)
        return response.json()


    # ENDPOINT PROJECT
    def get_all_project(self):
        """
        This method make a get request to the gns3 server to get all project

        :return: a list of all projects
        """
        response = self.gns3_request_get('/projects')
        self.check_reponse(response)
        return response.json()

    def set_current_project(self, id_project=None):
        """
        This method set the current project

        :param id_project: the id of the project we want to work
        :return: set the `selected_project`
        """
        if id_project is None:
            print("List of projects:")
            for id_project in range(len(self.projects)):
                print('[', id_project, '] ', self.projects[id_project]['name'], ' ',
                  self.projects[id_project]['project_id'])
            return self.projects[int(input('Choose your project \n'))]
        else:
            return self.projects[id_project]

    # ENDPOINT SNAPSHOT
    def get_all_snapshots(self):
        """
        This method make a get request to the gns3 server to get all snapshots.

        :return: a list of all snapshots
        """
        response = self.gns3_request_get('/projects/' + self.selected_project['project_id'] +'/snapshots')
        self.check_reponse(response)
        return response.json()

    def post_snapshot(self,payload):
        """
        This method add a snapshot to the current project.

        :param payload: data about the snapshot
        :type payload: dict
        :return:

        An example of payload:

        .. code-block :: javascript

            {
                "name": "snap1"
            }

        """
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] +'/snapshots',payload)
        self.check_reponse(response)
        return response

    def delete_snapshot(self,snapshot_id):
        """
        This method delete a specific snapshot.

        :param snapshot_id: the id of snapshot
        :return: delete the wondered snapshot
        """
        response = self.gns3_request_delete('/projects/' + self.selected_project['project_id'] +'/snapshots/'+snapshot_id)
        self.check_reponse(response)
        return response

    def restore_snapshot(self,snapshot_id):
        """
        This method ask to gns3 server to restore the specific snapshot
        :param snapshot_id: the id of the snapshot
        :return: restore the snapshot
        """
        response = self.gns3_request_post('/projects/' + self.selected_project['project_id'] +'/snapshots/'+ snapshot_id +'/restore',{})
        self.check_reponse(response)
        return response

    ####################################################################################################################
    #                                            METHOD AUXILIARY                                                      #
    ####################################################################################################################
    def check_reponse(self, response):
        """
        This method check the code of  gns3 server's response

        :param response: the response of gns3 server's request
        :type response: `requests.models.Response`
        :return: nothing or error message if the status code is different of 200 or 201
        """
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 204 :
            print(ColorOutput.ERROR_TAG + ': network_manager  ' + str(response) + "\n-> " + response.text)
            exit(1)
        pass

