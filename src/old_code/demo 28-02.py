import time

from colorOutput import ColorOutput
from old_code.simple_topology import SimpleTopology
from docker_manager import DockerManager

st = SimpleTopology()
dm = DockerManager('local')
# TODO Create templates if they don't exist
internet = st.create_template("NAT",100)
dns = st.create_template("DNS", 400)
st.link_nodes(internet["node_id"],dns["node_id"])

net_config_dns = '''# Static config
auto eth0
iface eth0 inet static
	address 192.168.122.10
	netmask 255.255.255.0
	gateway 192.168.122.1
	up echo nameserver 8.8.8.8 > /etc/resolv.conf
auto eth1
iface eth1 inet static
	address 10.0.0.1
	netmask 255.255.255.0'''
st.simple_file_copy(dns["node_id"], "/etc/network/interfaces", net_config_dns)

st.start_node(dns["node_id"]) # TODO Check if node is started
print("Configuring DNS and DHCP...")
time.sleep(2)

dm.exec_to_docker(dns["properties"]["container_id"],"apt update") # Warning apt doesnt have a stable cli 
dm.exec_to_docker(dns["properties"]["container_id"],"apt install iptables -y")
dm.exec_to_docker(dns["properties"]["container_id"],"iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
dm.copy_to_docker("./config_files/dns/dnsmasq.conf",dns["properties"]["container_id"],"/etc/")
dm.copy_to_docker("./config_files/dns/hosts",dns["properties"]["container_id"],"/etc/")
dm.exec_to_docker(dns["properties"]["container_id"],"service dnsmasq restart")
print("Configuration done")

switch1 = st.create_template("Ethernet switch", 600)
user1 = st.create_template("Firefox", 500,100)
user2 = st.create_template("Alpine", 700,100)
server1 = st.create_template("Ubuntu Docker", 500, 200)
server2 = st.create_template("Ubuntu Docker", 700, 200)

st.link_nodes(switch1["node_id"],dns["node_id"], [0,0], [1,0])
st.link_nodes(switch1["node_id"],user1["node_id"], [0,1])
link1 = st.link_nodes(switch1["node_id"],user2["node_id"], [0,2])
st.link_nodes(switch1["node_id"],server1["node_id"], [0,3])
st.link_nodes(switch1["node_id"],server2["node_id"], [0,4])

net_config_dhcp='''# DHCP
auto eth0
iface eth0 inet dhcp
'''

st.simple_file_copy(user1["node_id"], "/etc/network/interfaces", net_config_dhcp)
st.simple_file_copy(user2["node_id"], "/etc/network/interfaces", net_config_dhcp)

switch2 = st.create_template("Ethernet switch", 800)
st.link_nodes(switch2["node_id"],switch1["node_id"], [0,0], [0,7])

for i in range(2,6):
    user = st.create_template("Alpine", 900, i*100-200)
    st.link_nodes(switch2["node_id"], user["node_id"], [0,i])
    st.simple_file_copy(user["node_id"], "/etc/network/interfaces", net_config_dhcp)

st.nm.start()

st.delete_link(link1["link_id"])
st.delete_node(user2["node_id"])

switch3 = st.create_template("Ethernet switch", 800, 300)
user_python = st.create_template("alpine-python", 600, 300)
user_scapy = st.create_template("alpine-scapy", 600, 400)
st.link_nodes(switch2["node_id"],switch3["node_id"], [0,1])
st.link_nodes(switch3["node_id"],user_python["node_id"], [0,1])
st.link_nodes(switch3["node_id"],user_scapy["node_id"], [0,2])

st.simple_file_copy(user_python["node_id"], "/etc/network/interfaces", net_config_dhcp)
st.simple_file_copy(user_scapy["node_id"], "/etc/network/interfaces", net_config_dhcp)

print(ColorOutput.INFO_TAG + "DONE")