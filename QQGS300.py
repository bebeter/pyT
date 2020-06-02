#!/usr/bin/python
# -*- coding: utf-8 -*-
#50
zs=[]

for i  in range(3300,4400,100):
    zs.append(i)
print (zs)

gou=[]
gu=[]

for i  in range(10002451,10002460):
    gou.append(i)
gou.append(10002473)
gou.append(10002519)


for i  in range(10002460,10002469):
    gu.append(i)
gu.append(10002474)
gu.append(10002520)

print (gou)
print (gu)

for i in range(0,len(gu)):
    print("\n{",zs[i],"}")
    print("h"+str(zs[i])+"g:=\""+str(gou[i])+"$CLOSE\"*10000;")
    print("h"+str(zs[i])+ ":=\""+str(gu[i])+"$CLOSE\"*10000;")
    print("he"+str(zs[i])+":h"+str(zs[i])+"g+h"+str(zs[i])+";" )