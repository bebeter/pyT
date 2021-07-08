#!/usr/bin/python
# -*- coding: utf-8 -*-
#50
zs=[]

for i  in range(3800,5000,100):  #range 第二个数字 不算
    zs.append(i)
print (zs)

gou=[]
gu=[]

for i  in range(10002603,10002612):#range 第二个数字 不算
    gou.append(i)
gou.append(10002631)
gou.append(10002647)
gou.append(10002663)

for i  in range(10002612,10002621):#range 第二个数字 不算
    gu.append(i)
gu.append(10002632)
gu.append(10002648)
gu.append(10002664)

print (gou)
print (gu)

for i in range(0,len(gu)):
    print("\n{",zs[i],"}")
    print("h"+str(zs[i])+"g:=\""+str(gou[i])+"$CLOSE\"*10000;")
    print("h"+str(zs[i])+ ":=\""+str(gu[i])+"$CLOSE\"*10000;")
    print("he"+str(zs[i])+":h"+str(zs[i])+"g+h"+str(zs[i])+";" )