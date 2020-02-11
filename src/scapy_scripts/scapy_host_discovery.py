from scapy.all import *

TIMEOUT = 1
conf.verb = 0
for ip in range(0, 256):
    packet = IP(dst="10.0.0." + str(ip), ttl=5)/ICMP()
    reply = sr1(packet, timeout=TIMEOUT)
    if not (reply is None):
         print(reply.src, "is online")
    else:
         print("Timeout waiting for %s" % packet[IP].dst)
