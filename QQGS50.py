#!/usr/bin/python
# -*- coding: utf-8 -*-
#50
zs=[]

for i  in range(2450,3000,50):
    zs.append(i)
print (zs)

gou=[]
gu=[]
gou.append(10002469)
for i  in range(10002433,10002442):
    gou.append(i)
gou.append(10002471)

gu.append(10002470)
for i  in range(10002442,10002451):
    gu.append(i)
gu.append(10002472)

print (gou)
print (gu)

for i in range(0,len(gu)):
    print("\n{",zs[i],"}")
    print("h"+str(zs[i])+"g:=\""+str(gou[i])+"$CLOSE\"*10000;")
    print("h"+str(zs[i])+ ":=\""+str(gu[i])+"$CLOSE\"*10000;")
    print("he"+str(zs[i])+":h"+str(zs[i])+"g+h"+str(zs[i])+";" )

