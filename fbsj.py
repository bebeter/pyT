#!/usr/bin/env python
#-*- coding: GBK -*-


from pandas import read_csv


import socket

import re
import json


import sys
import urllib
import time
import os

import sys





fn = r"d:\603888.csv"
f = open(fn)
print ("\n\n-----------------------------------")

#f2 = r"d:\fd.sql"
#fw = open(f2,"w")

tm = []
price = []
volume =[]
salevolume=[]
buyvolume=[]
mmtype=[]
saleid=[]
saleprice=[]
buyid=[]
buyprice=[]


for line in f.readlines():
    #print line
    line = line.strip()
    data = line.split(",")


f.close()

data = read_csv(fn)
print(data)
print(data.describe())
print(data.head(5))  # ǰ5��
print(data.iloc[0, :])  # ��һ����������
print(data.iloc[[1, 3, 4], :])  # ��2 4 6��
#print(data.iloc[:, :])  # ���к�������
#print(data.loc[:, 'Time'])

print("\n\n******************")

sum_buy =0
sum_sell = 0
for index, row in data.iterrows():
    #print(row['Time'], row['Volume'], type(row['SaleOrderVolume']), type(row['BuyOrderVolume'])),row['Type'],
    #print (row['Time'][:5].replace(":",""))
    if row['Type']=="B":
        sum_buy = sum_buy+row['Volume']
    else:
        sum_sell = sum_sell+row['Volume']


print ("sum_buy:",sum_buy  ,"sum_sell:",sum_sell)
