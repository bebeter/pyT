# coding=gbk
import re, string
import os
import glob
import math
import pandas as pd
import time# 1. 获取时间元组
struct_time = time.localtime()# 2. 转换字符串格式
mi =(time.strftime('%Y%m%d%H%M%S',struct_time))

cm_dics    = {}     #    0: {'2000-01-01',100}
today_dics = {}

base_diretory="data\\"



def deal_gp_fb(data_file, rq, stk_code):
    fn = data_file
    #lastClose = getLastClose(rq, stk_code)
    #+zt_price = getZt(lastClose)

    print(fn)
    print(rq)



    df = pd.read_csv(fn, header=0) #, index_col=0
    print(df.head(5))
    sale_df = df.groupby("SaleOrderID")['Volume'].sum()

    print(sale_df.head(10))
    for row in sale_df.values:
        print(row)


    for index, row in df.iterrows():
        #if index >50000000000:
        #    break
        TranID = row['TranID']
        Time = row['Time']
        Price = row['Price']
        Volume = row['Volume']
        SaleOrderVolume = row['SaleOrderVolume']
        BuyOrderVolume = row['BuyOrderVolume']

        #print(index,row)


        #买方筹码累计

        if Price in today_dics:
            if rq  in today_dics [Price]  :
                today_dics[Price][rq] =today_dics[Price][rq]+ Volume
            else:
                today_dics[Price][rq] = Volume
        else:
            today_dics[Price]={}
            today_dics[Price][rq] =  Volume

        #卖方筹码衰减
        can_sell_price = []
        can_sell_rq = []


        can_sell_price = today_dics.keys()
        can_sell_rq = []

    print(today_dics)








def main():
    rq = '2020-07-13'
    stk_code = '002074'

    #path = r"C:/data/csv/" + rq + "/"
    path = r"C:/l2data/202007/" + rq + "/"

    data_file = path+ stk_code + ".csv"
    #deal_gp(data_file,rq,stk_code)

    deal_gp_fb(data_file, rq, stk_code)

#给代码加上市场字母
def marketstr(dm):
    #print dm,dm[0]
    if dm[0]==str(6):
        dm='sh'+dm
    elif dm[0]==str(3) or dm[0]==str(0):
        dm='sz'+dm
    #print dm
    return dm

def get_ltp (dm):
    f = open(base_diretory +   "info.csv", "r")
    ltp =0
    for line in f.readlines():
        data = line.strip().split(",")
        #print(data)
        if (data[0]==dm):
            ltp =  data[2]
            break
    f.close()
    return float(ltp) *100000000


def getRq(dm):
    f = open(base_diretory  + marketstr(dm) + ".txt", "r")
    rq = []
    index =0
    for line in f.readlines():
        if index==0:
            index=index+1
            continue
        daydata = line.split(",")
        rq.append(daydata[0].replace("/", "-"))
    f.close()
    return rq

if __name__ == '__main__':
    #main()
    dm="300842"
    rq=getRq(dm)
    print(rq)
    ltp = get_ltp(dm)
    print( ltp )