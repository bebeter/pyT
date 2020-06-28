#!/usr/bin/python
# -*- coding: utf-8 -*-
#50
zs=[]

for i  in range(2350,3300,50):
    zs.append(i)
print (zs)

gou=[]
gu=[]
gou.append(10002421)
gou.append(10002401)
gou.append(10002402)
for i  in range(10002291,10002294):
    gou.append(i)
for i  in range(10002083,10002091):
    gou.append(i)
gou.append(10002107)

gu.append(10002422)
gu.append(10002403)
gu.append(10002404)

for i  in range(10002295,10002298):
    gu.append(i)
for i in range(10002092, 10002100):
    gu.append(i)

gu.append(10002108)

print (gou)
print (gu)

for i in range(0,len(gu)):
    print("\n{",zs[i],"}")
    print("h"+str(zs[i])+"g:=\""+str(gou[i])+"$CLOSE\"*10000;")
    print("h"+str(zs[i])+ ":=\""+str(gu[i])+"$CLOSE\"*10000;")
    print("he"+str(zs[i])+":h"+str(zs[i])+"g+h"+str(zs[i])+";" )

