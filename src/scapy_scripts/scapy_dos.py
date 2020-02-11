from scapy.all import *

# Not working
while True:
        send( IP(src="10.0.0.65",dst="10.0.0.14")/TCP(flags="S", dport=(80)) )