from scapy.all import *

# Scan port of 10.0.0.14
ans, unans = sr( IP(dst="10.0.0.14")/TCP(flags="S", dport=(1,1024)) )
#ans.summary( lambda sr: r.sprintf("%TCP.sport% \t %TCP.flags%") )

# Show opened ports
print('Ports open')
ans.summary(lfilter = lambda s_r: s_r[1].sprintf("%TCP.flags%") == "SA",prn=lambda s_r:s_r[1].sprintf("%TCP.sport% is open"))

