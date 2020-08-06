# coding=gbk
import re, string
import os
import glob
import math
import random


import pandas as pd
import time# 1. 获取时间元组
struct_time = time.localtime()# 2. 转换字符串格式
mi =(time.strftime('%Y%m%d%H%M%S',struct_time))

cm_dics    = {}     #    0: {'2000-01-01',100}
today_dics = {}

base_diretory="data\\"




def get_weight_hl (  hl):
        weight_hl = 0 #获利的权重
        weight_hsl = 0  # 换手率的权重

        weight= 0
        if (hl<0 and hl>=-5):
            weight_hl=(0.5,0.8)
        elif(hl< -5 and hl>=-10 ):
            weight_hl = (0.3, 0.5)
        elif(hl< -10 and hl>=-20 ):
            weight_hl = (0.1, 0.2)
        elif(hl<-20 and hl>=-30 ):
            weight_hl = (0.05, 0.08)
        elif(hl< -30 ):
            weight_hl = (0.01, 0.02)
        elif(hl< 5 and hl>=0 ):
            weight_hl = (0.85, 0.9)
        elif (hl < 10 and hl >= 5):
            weight_hl = (0.65, 0.8)
        elif (hl < 15 and hl >= 10):
            weight_hl = (0.3, 0.5)
        elif (hl < 20 and hl >= 15):
            weight_hl = (0.1, 0.2)
        elif (hl < 30 and hl >= 20):
            weight_hl = (0.05, 0.08)
        elif ( hl >=30):
            weight_hl = (0.01, 0.03)
        return weight_hl

def get_weight_day(day):
        weight_day = 0
        if (day < 3 and day >= 0):
            weight_day = (0.6, 0.8)
        elif(day< 5 and day>=3 ):
            weight_day = (0.5, 0.6)
        elif (day < 10 and day >= 5):
            weight_day = (0.4, 0.7)
        elif (day < 15 and day >= 10):
            weight_day = (0.3, 0.5)
        elif (day < 20 and day >= 15):
            weight_day = (0.1, 0.2)
        elif (day < 30 and day >= 20):
            weight_day = (0.06, 0.08)
        elif (day < 50 and day >= 30):
            weight_day = (0.03, 0.05)
        elif ( day >= 50):
            weight_day = (0.01, 0.02)
        return weight_day

def get_weight_hsl(hsl):
        weight_hsl= 0
        if (hsl < 3 and hsl >= 0):
            weight_hsl = (0.03, 0.05)
        elif(hsl< 5 and hsl>=3 ):
            weight_hsl = (0.06, 0.08)
        elif (hsl < 10 and hsl >= 5):
            weight_hsl = (0.08, 0.12)
        elif (hsl < 15 and hsl >= 10):
            weight_hsl = (0.15, 0.3)
        elif (hsl < 20 and hsl >= 15):
            weight_hsl = (0.3, 0.5)
        elif (hsl < 30 and hsl >= 20):
            weight_hsl = (0.5, 0.6)
        elif (hsl < 50 and hsl >= 30):
            weight_hsl = (0.7, 0.8)
        elif ( hsl >= 50):
            weight_hsl = (0.9, 0.95)
        return weight_hsl




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

        #卖方筹码衰减
        can_sell_price = []
        can_sell_rq = []

        #如果是第一天
        #近期的赋值 大的概率抽奖 卖出




        #买方筹码累计

        if Price in today_dics:
            if rq  in today_dics [Price]  :
                today_dics[Price][rq] =today_dics[Price][rq]+ Volume
            else:
                today_dics[Price][rq] = Volume
        else:
            today_dics[Price]={}
            today_dics[Price][rq] =  Volume




        can_sell_price = today_dics.keys()
        can_sell_rq = []

    print(today_dics)




#转换存储的目录
def get_dir(rq):
   return rq[:7].replace("-","")


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
    aa= get_weight_hsl(3.5)

    print(aa[0], aa[1])
    a=random.randint(aa[0] * 100, aa[1] * 100) / 100
    print(a)

    bb=get_weight_day(13)
    print(bb[0], bb[1])
    b=random.randint(bb[0] * 100, bb[1] * 100) / 100
    print()




    cc=get_weight_hl(17)
    print(cc[0], cc[1])
    c=random.randint(cc[0] * 100, cc[1] * 100) / 100
    print(c)

    print(a*b*c)










    ''' 
    dm="300842"
    rq=getRq(dm)
    print(rq)
    ltp = get_ltp(dm)
    print( ltp )
   
  
    print(get_dir(rq[0]))
    
    '''