from scapy.all import *

p = rdpcap('wKnHiu4fiaxkllT80tFB.pcap')
for i in range(0,len(p)):
  if not p[i].haslayer(DNS):
    continue
  if DNSQR in p[i]:
    if DNSRR in p[i] and len(p[i][DNSRR].rdata)>0: # downstream/server
      print "S[%i]: %r" % (i,p[i][DNSRR].rdata)
    else: # upstream/client
      print "C[%i]: %r" % (i,p[i][DNSQR].qname)