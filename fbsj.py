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
print(data.head(5))  # 前5行
print(data.iloc[0, :])  # 第一行所有数据
print(data.iloc[[1, 3, 4], :])  # 第2 4 6行
#print(data.iloc[:, :])  # 所有航所有列
#print(data.loc[:, 'Time'])

print("\n\n******************")

sum_buy =0
sum_sell = 0

buy_dics ={}
sell_dics ={}

last_row_price = 0

for index, row in data.iterrows():
    #print(row['Time'], row['Volume'], type(row['SaleOrderVolume']), type(row['BuyOrderVolume'])),row['Type'],
    #print (row['Time'][:5].replace(":",""))
    #TranID	Time	Price	Volume	SaleOrderVolume	BuyOrderVolume	Type	SaleOrderID	SaleOrderPrice	BuyOrderID	BuyOrderPrice

    saleid =row['SaleOrderID']
    buyid=row['BuyOrderID']

    TranID=row['TranID']
    Time = row['Time']
    Price=row['Price']
    Volume=row['Volume']
    SaleOrderVolume=row['SaleOrderVolume']
    BuyOrderVolume=row['BuyOrderVolume']

    is_jj=0  #是否竞价

    if Time == '9:25:00' or Time == '09:25:00':
        is_jj=1

    if buyid in buy_dics:
        buy_dics[buyid]['is_jj'] = is_jj
        if TranID==buy_dics[buyid]['max_id']+1:
            buy_dics[buyid]['is_continue'] = 1
        else:
            buy_dics[buyid]['is_continued'] = 0

        buy_dics[buyid]['max_id'] = TranID

        if Price < buy_dics[buyid]['min_price'] :
            buy_dics[buyid]['min_price'] = Price

        if Price > buy_dics[buyid]['max_price']:
             buy_dics[buyid]['max_price'] = Price
             buy_dics[buyid]['price_count'] = buy_dics[buyid]['price_count']+1  #不太好确定

        if Volume < buy_dics[buyid]['min_vol'] :
            buy_dics[buyid]['min_vol'] = Volume
        if Volume > buy_dics[buyid]['max_vol']:
            buy_dics[buyid]['max_vol'] = Volume

        buy_dics[buyid]['id_count'] = buy_dics[buyid]['id_count']+1

        buy_dics[buyid]['sum_vol'] = buy_dics[buyid]['sum_vol']+Volume
        buy_dics[buyid]['avg_vol'] = buy_dics[buyid]['sum_vol']/buy_dics[buyid]['id_count']

        if SaleOrderVolume > buy_dics[buyid]['max_sale_vol']:
            buy_dics[buyid]['max_sale_vol'] = SaleOrderVolume
        if BuyOrderVolume > buy_dics[buyid]['BuyOrderVolume']:
            buy_dics[buyid]['max_buy_vol'] = BuyOrderVolume

        if buy_dics[buyid]['sale_id_count'] >1  and buy_dics[buyid]['is_continue']==1:
            buy_dics[buyid]['tran_type'] = buy_dics[buyid]['tran_type'] +'推动追买'
        else:
            buy_dics[buyid]['tran_type'] = buy_dics[buyid]['tran_type'] +'普通挂买'

    else:
        buy_dics[buyid]['is_jj']=is_jj

        buy_dics[buyid]['min_id'] = TranID
        buy_dics[buyid]['max_id'] = TranID
        buy_dics[buyid]['is_continue'] = -1

        buy_dics[buyid]['min_price'] = Price
        buy_dics[buyid]['max_price'] = Price
        buy_dics[buyid]['price_count'] = 1

        buy_dics[buyid]['start_time'] = Time
        buy_dics[buyid]['end_time'] = Time

        buy_dics[buyid]['max_vol'] = Volume
        buy_dics[buyid]['min_vol'] = Volume
        buy_dics[buyid]['sum_vol'] = Volume
        buy_dics[buyid]['avg_vol'] = Volume

        buy_dics[buyid]['max_sale_vol'] = SaleOrderVolume
        buy_dics[buyid]['max_buy_vol'] = BuyOrderVolume

        buy_dics[buyid]['sale_id_count'] = 1

        if Volume== BuyOrderVolume  and Price <= last_row_price :
            buy_dics[buyid]['tran_type'] = '普通挂买'
        elif Volume== BuyOrderVolume  and Price > last_row_price :
            buy_dics[buyid]['tran_type'] = '普通追买'
        elif Volume < BuyOrderVolume and Price > last_row_price:
            buy_dics[buyid]['tran_type'] = '推动追买'
        else:
            print(TranID)





    if saleid in sell_dics:
        sell_dics[saleid]['is_jj'] = is_jj
        if TranID == sell_dics[saleid]['max_id'] + 1:
            sell_dics[saleid]['is_continue'] = 1
        else:
            sell_dics[saleid]['is_continued'] = 0

        sell_dics[saleid]['max_id'] = TranID

        if Price < sell_dics[saleid]['min_price']:
            sell_dics[saleid]['min_price'] = Price

        if Price > sell_dics[saleid]['max_price']:
            sell_dics[saleid]['max_price'] = Price
            sell_dics[saleid]['price_count'] = sell_dics[saleid]['price_count'] + 1  # 不太好确定

        if Volume < sell_dics[saleid]['min_vol']:
            sell_dics[saleid]['min_vol'] = Volume
        if Volume > sell_dics[saleid]['max_vol']:
            sell_dics[saleid]['max_vol'] = Volume

        sell_dics[saleid]['d_count'] = sell_dics[saleid]['id_count'] + 1

        sell_dics[saleid]['sum_vol'] = sell_dics[saleid]['sum_vol'] + Volume
        sell_dics[saleid]['avg_vol'] = sell_dics[saleid]['sum_vol'] / sell_dics[saleid]['id_count']

        if SaleOrderVolume > sell_dics[saleid]['max_sale_vol']:
            sell_dics[saleid]['max_sale_vol'] = SaleOrderVolume
        if BuyOrderVolume > sell_dics[saleid]['BuyOrderVolume']:
            sell_dics[saleid]['max_buy_vol'] = BuyOrderVolume

        if sell_dics[saleid]['sale_id_count'] > 1 and sell_dics[saleid]['is_continue'] == 1:
            sell_dics[saleid]['tran_type'] = sell_dics[saleid]['tran_type'] + '推动追卖'
        else:
            sell_dics[saleid]['tran_type'] = sell_dics[saleid]['tran_type'] + '普通挂卖'

    else:
        sell_dics[saleid]['is_jj'] = is_jj

        sell_dics[saleid]['min_id'] = TranID
        sell_dics[saleid]['max_id'] = TranID
        sell_dics[saleid]['is_continue'] = -1

        sell_dics[saleid]['min_price'] = Price
        sell_dics[saleid]['max_price'] = Price
        sell_dics[saleid]['price_count'] = 1

        sell_dics[saleid]['start_time'] = Time
        sell_dics[saleid]['end_time'] = Time

        sell_dics[saleid]['max_vol'] = Volume
        sell_dics[saleid]['min_vol'] = Volume
        sell_dics[saleid]['sum_vol'] = Volume
        sell_dics[saleid]['avg_vol'] = Volume

        sell_dics[saleid]['max_sale_vol'] = SaleOrderVolume
        sell_dics[saleid]['max_buy_vol'] = BuyOrderVolume

        sell_dics[saleid]['sale_id_count'] = 1

        if Volume == BuyOrderVolume and Price <= last_row_price:
            sell_dics[saleid]['tran_type'] = '普通挂卖'
        elif Volume == BuyOrderVolume and Price > last_row_price:
            sell_dics[saleid]['tran_type'] = '普通追卖'
        elif Volume < BuyOrderVolume and Price > last_row_price:
            sell_dics[saleid]['tran_type'] = '推动追卖'
        else:
            print(TranID)

    last_row_price=Price




buy_orders={
    1000:{
"min_id":"",
"max_id":"",
"is_continue":"",

        "start_time":"",
        "end_time":"",

"min_price":"",
"max_price":"",
"price_count":0,

"max_vol":0,
"min_vol":0,
"sum_vol":0,
"avg_vol":0,

"max_sale_vol":0,
"max_buy_vol":0,

"sale_id_count":0,

        "buy_type":"",
         "":"",

    },


    2000:{

    }


}