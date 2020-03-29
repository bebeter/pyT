#!/usr/bin/python
# -*- coding: utf-8 -*-

zs=[]

for i  in range(3700,4700,100):
    zs.append(i)
print (zs)

gou=[]
gu=[]

for i  in range(10002351,10002360):
    gou.append(i)
gou.append(10002381)
for i  in range(10002360,10002369):
    gu.append(i)
gu.append(10002382)

print (gou)
print (gu)

for i in range(0,len(gu)):
    print("\n{",zs[i],"}")
    print("h"+str(zs[i])+"g:=\""+str(gou[i])+"$CLOSE\"*10000;")
    print("h"+str(zs[i])+ ":=\""+str(gu[i])+"$CLOSE\"*10000;")
    print("he"+str(zs[i])+":h"+str(zs[i])+"g+h"+str(zs[i])+";" )

