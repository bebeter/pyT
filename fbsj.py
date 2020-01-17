#!/usr/bin/env python
#-*- coding: GBK -*-


from pandas import read_csv


import socket
from pyquery import PyQuery as pq
from lxml import etree
import urllib2
import re
import json


import sys
import urllib
import time
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
reload(sys)
sys.setdefaultencoding( "GBK" )




fn = r"d:\603888.csv"
f = open(fn)
print "\n\n-----------------------------------"

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
print(data.head(5))  # 前5行
print(data.iloc[0, :])  # 第一行所有数据
print(data.iloc[[1, 3, 4], :])  # 第2 4 6行
#print(data.iloc[:, :])  # 所有航所有列
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
