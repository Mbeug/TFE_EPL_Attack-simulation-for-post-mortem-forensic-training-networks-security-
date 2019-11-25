import requests
import os

gns3_user = 'admin'
gns3_password = 'TSRq4lxcZ2FaM9z1Otlu9jLW0wdTyyKzAJc9eaocSLlsIQAxMVH4bAEVN2mFdB4o'
gns3_host = 'localhost'
gns3_port = '3080'

gns3_url = 'http://'+gns3_user+':'+gns3_password+'@'+gns3_host+':'+gns3_port+'/v2'

def gns3_request(endpoint):
    return requests.get(gns3_url+endpoint)

def gns3_req_param(endpoint, payload):
    return requests.post(gns3_url+endpoint, json = payload)

# print(response.json()['version']))

print('List of projects:')

projects = gns3_request('/projects').json()
for id_project in range(len(projects)):
    print('[',id_project,'] ',projects[id_project]['name'],' ',projects[id_project]['project_id'])
selected_proj = int(input('Choose your project \n'))
    
nb_vpcs = int(input('How many VPCS ? (max 10)\n'))

print('Creating nodes...')
list_vpcs = []
gns3_y = int(nb_vpcs*-80/2)
for vpcs in range(nb_vpcs):
    vpc_payload = {"name": "VPCS1", "node_type": "vpcs", "compute_id": "local", "x" : 230, "y": gns3_y}
    response = gns3_req_param('/projects/'+projects[selected_proj]['project_id']+'/nodes', vpc_payload)
    if response.status_code != 200 and response.status_code != 201:
        print(response)
        print(response.text)
        exit()
    gns3_y += 80
    list_vpcs.append(response.json()["node_id"])

print('Linking nodes...')
switch_port = 1
for vpcs_id in list_vpcs:
    vpc_payload = {"nodes": [{"adapter_number": 0, "node_id": "6c6d9661-c311-42e3-8ddc-554286dc6afc", "port_number": switch_port}, {"adapter_number": 0, "node_id": vpcs_id, "port_number": 0}]}
    response = gns3_req_param('/projects/'+projects[selected_proj]['project_id']+'/links', vpc_payload)

    os.mkdir("../GNS3/projects/simpleRemote/project-files/vpcs/"+vpcs_id)
    f = open("../GNS3/projects/simpleRemote/project-files/vpcs/"+vpcs_id+"/startup.vpc", "x")
    f.write("ip 192.168.2."+str(switch_port)+"\n ping 192.168.2.254")
    f.close()

    switch_port += 1


print('Starting nodes and capture...')
gns3_req_param('/projects/'+projects[selected_proj]['project_id']+'/nodes/start',{})
gns3_req_param('/projects/'+projects[selected_proj]['project_id']+'/links/cac46ed1-27e8-40eb-bf38-81781cb7c65e/start_capture',{})
