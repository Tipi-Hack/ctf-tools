from scapy.all import *
from binascii import unhexlify

print "hi"
s=unhexlify("FIXME_HEX_PAYLOAD")
packet = Ether()/IP(dst="10.13.37.70")/UDP(sport=500,dport=500)/Raw(load=s)

sendp(packet, iface='eth0')
