# coding=gbk
import re, string
import os
import glob

import pandas as pd
import time# 1. 获取时间元组
struct_time = time.localtime()# 2. 转换字符串格式
mi =(time.strftime('%Y%m%d%H%M%S',struct_time))

# print type(os.listdir("."))
# glob.glob('c:\\music\\_singles\\*.mp3')
# for  i  in os.listdir("."):


import mysql.connector





def deal_gptj(data_file,rq,stk_code):
    f = open(data_file, "r")
    lines = f.readlines()
    line_count = 0
    f2 = open(r"c:/data/"+rq+"/"+stk_code+".txt", "a")
    for line in lines:
        line_count = line_count + 1
        if line_count == 1:
            continue
        filds = line.split(',')

        # print (filds[0], filds[1], filds[2], filds[3], filds[4], filds[5], filds[6])
        # (FDAY,ID,TRANID,TIME,PRICE,VOLUME,SALEORDERVOLUME,BUYORDERVOLUME,TYPE,SALEORDERID,SALEORDERPRICE,BUYORDERID,BUYORDERPRICE)

    f2.write(filds + "\n")

    f2.close()
    f.close()


# 192.168.1.8

def getLastClose(rq,stk_code):
    print(rq,stk_code)
    return 32.32

def getZt(close):

    return  round(1.1*close,2)

def deal_gp(data_file,rq,stk_code):
    f = open(data_file, "r")
    lines = f.readlines()
    line_count = 0



    # 打开数据库连接
    # db = MySQLdb.connect("192.168.1.8","root","root123","ts" )
    db = mysql.connector.connect(host="127.0.0.1", user='root', password='', database='ts', use_unicode=True)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    path=r"C:/data/sql/"+rq
    if not os.path.isdir(path):
        os.makedirs(path)
    f2 = open(path+"/"+stk_code+".sql", "a")
    for line in lines:
        line_count = line_count + 1
        if line_count == 1:
            continue
        filds = line.split(',')

        # print (filds[0], filds[1], filds[2], filds[3], filds[4], filds[5], filds[6])(FDAY,ID,TRANID,TIME,PRICE,VOLUME,SALEORDERVOLUME,BUYORDERVOLUME,TYPE,SALEORDERID,SALEORDERPRICE,BUYORDERID,BUYORDERPRICE) values
        sql = " insert into    fdata values   ('" + rq + "','" + stk_code + "','" + filds[
            0].strip() + "','" + filds[1].strip() + "','" + filds[2].strip() + "','" + filds[3].strip() + "','" + filds[
                  4].strip() + "','" + filds[5].strip() + "','" + filds[6].strip() + "','" + filds[7].strip() + "','" + \
              filds[8].strip() + "','" + filds[9].strip() + "','" + filds[10].strip() + "') ;"

        # 使用execute方法执行SQL语句
        cursor.execute(sql)


        f2.write(sql + "\n")
        # print str(index)+","+name+","+stk[1:7]
        # break
    f2.close()
    db.close()
    f.close()












def deal_dir(path):
    global name, data_file
    print(path)
    index = 100
    for i in glob.glob(path):
        index = index + 1
        name = i[-10:-4]
        print(name)
        if index >= 103:
            break
        data_file = i
        deal_gp(data_file)



# for item in ():

def deal_gp_fb(data_file, rq, stk_code):
    fn = data_file
    lastClose = getLastClose(rq, stk_code)
    zt_price = getZt(lastClose)



    df = pd.read_csv(fn, header=0) #, index_col=0
    print(df.head(5))
    #TranID = df['TranID']
    Time = df['Time']
    #Price= df("Price")
    #Volume= df("Volume")
    #print(df.index[0])
    #print(Time[1])

    #print(df.loc[ 1 ])
    #print(df.loc[df.index[0]])

    sum_buy = 0
    sum_sell = 0

    buy_dics = {0:{}}
    sell_dics = {0:{}}

    last_row_price = 0

    for index, row in df.iterrows():
        # print(row['Time'], row['Volume'], type(row['SaleOrderVolume']), type(row['BuyOrderVolume'])),row['Type'],
        # print (row['Time'][:5].replace(":",""))
        # TranID	Time	Price	Volume	SaleOrderVolume	BuyOrderVolume	Type	SaleOrderID	SaleOrderPrice	BuyOrderID	BuyOrderPrice

        saleid = row['SaleOrderID']
        buyid = row['BuyOrderID']

        TranID = row['TranID']
        Time = row['Time']
        Price = row['Price']
        Volume = row['Volume']
        SaleOrderVolume = row['SaleOrderVolume']
        BuyOrderVolume = row['BuyOrderVolume']

        is_jj = 0  # 是否竞价

        if Time == '9:25:00' or Time == '09:25:00':
            is_jj = 1

        if buyid in buy_dics:
            buy_dics[buyid]['buyid'] = buyid
            buy_dics[buyid]['is_jj'] = is_jj
            if TranID == buy_dics[buyid]['max_id'] + 1:
                buy_dics[buyid]['is_continue'] = 1
            else:
                buy_dics[buyid]['is_continue_break'] = 1
                buy_dics[buyid]['is_continue'] = 0

            buy_dics[buyid]['max_id'] = TranID

            if Price < buy_dics[buyid]['min_price']:
                buy_dics[buyid]['min_price'] = Price

            if Price > buy_dics[buyid]['max_price']:
                buy_dics[buyid]['max_price'] = Price
                buy_dics[buyid]['price_count'] = buy_dics[buyid]['price_count'] + 1  # 不太好确定

            buy_dics[buyid]['end_time'] = Time

            if Volume < buy_dics[buyid]['min_vol']:
                buy_dics[buyid]['min_vol'] = Volume
            if Volume > buy_dics[buyid]['max_vol']:
                buy_dics[buyid]['max_vol'] = Volume

            buy_dics[buyid]['id_count'] = buy_dics[buyid]['id_count'] + 1

            buy_dics[buyid]['sum_vol'] = buy_dics[buyid]['sum_vol'] + Volume
            buy_dics[buyid]['avg_vol'] = round(buy_dics[buyid]['sum_vol'] / buy_dics[buyid]['id_count'],2)


            if SaleOrderVolume > buy_dics[buyid]['max_sale_vol']:
                buy_dics[buyid]['max_sale_vol'] = SaleOrderVolume
            if BuyOrderVolume > buy_dics[buyid]['max_buy_vol']:
                buy_dics[buyid]['max_buy_vol'] = BuyOrderVolume

            buy_dics[buyid]['amount'] = buy_dics[buyid]['amount'] + Price * Volume


            if zt_price == Price:
                buy_dics[buyid]['tran_type2'] = '推动追买'
            elif  (buy_dics[buyid]['id_count'] > 1 and buy_dics[buyid]['is_continue'] == 1 and Price == last_row_price) or Price > last_row_price:
                buy_dics[buyid]['tran_type2'] =  '推动追买'
            else:

                buy_dics[buyid]['tran_type1'] = '普通挂买'

        else:
            buy_dics[buyid]={}
            buy_dics[buyid]['buyid'] = buyid
            buy_dics[buyid]['is_jj'] = is_jj

            buy_dics[buyid]['min_id'] = TranID
            buy_dics[buyid]['max_id'] = TranID
            buy_dics[buyid]['is_continue'] = -1   #第一单
            buy_dics[buyid]['is_continue_break'] = 0


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

            buy_dics[buyid]['amount'] =  Price * Volume

            buy_dics[buyid]['id_count'] = 1

            buy_dics[buyid]['tran_type0'] = ''

            buy_dics[buyid]['tran_type1'] = ''
            buy_dics[buyid]['tran_type2'] = ''

            if zt_price == Price:
                buy_dics[buyid]['tran_type2'] = '推动追买'
            elif  Price <= last_row_price:
                buy_dics[buyid]['tran_type1'] = '普通挂买'
            elif Volume == BuyOrderVolume and Price > last_row_price:
                buy_dics[buyid]['tran_type2'] = '推动追买'
            elif Volume < BuyOrderVolume and Price > last_row_price:
                buy_dics[buyid]['tran_type2'] = '推动追买'
            else:
                buy_dics[buyid]['tran_type0'] = '买'
                #print(TranID)

        if saleid in sell_dics:
            sell_dics[saleid]['buyid'] = saleid
            sell_dics[saleid]['is_jj'] = is_jj
            if TranID == sell_dics[saleid]['max_id'] + 1:
                sell_dics[saleid]['is_continue'] = 1
            else:
                sell_dics[saleid]['is_continue_break'] = 1
                sell_dics[saleid]['is_continue'] = 0

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

            sell_dics[saleid]['id_count'] = sell_dics[saleid]['id_count'] + 1  #笔数

            sell_dics[saleid]['end_time'] = Time

            sell_dics[saleid]['sum_vol'] = sell_dics[saleid]['sum_vol'] + Volume
            sell_dics[saleid]['avg_vol'] = round(sell_dics[saleid]['sum_vol'] / sell_dics[saleid]['id_count'],2)

            if SaleOrderVolume > sell_dics[saleid]['max_sale_vol']:
                sell_dics[saleid]['max_sale_vol'] = SaleOrderVolume
            if BuyOrderVolume > sell_dics[saleid]['max_buy_vol']:
                sell_dics[saleid]['max_buy_vol'] = BuyOrderVolume

            sell_dics[saleid]['amount'] = sell_dics[saleid]['amount'] + Price * Volume

            if zt_price==Price:
                    sell_dics[saleid]['tran_type2'] = '推动追卖'
            elif ( sell_dics[saleid]['is_continue'] == 1 and Price == last_row_price) or  Price < last_row_price:
                sell_dics[saleid]['tran_type2'] = '推动追卖,'
            else:
                sell_dics[saleid]['tran_type1'] = '普通挂卖,'

        else:
            sell_dics[saleid]={}
            sell_dics[saleid]['buyid'] = saleid
            sell_dics[saleid]['is_jj'] = is_jj

            sell_dics[saleid]['min_id'] = TranID
            sell_dics[saleid]['max_id'] = TranID
            sell_dics[saleid]['is_continue'] = -1 #第一单
            sell_dics[saleid]['is_continue_break'] = 0

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

            sell_dics[saleid]['amount']=Price*Volume

            sell_dics[saleid]['id_count'] = 1

            sell_dics[saleid]['tran_type0']=''

            sell_dics[saleid]['tran_type1']=''
            sell_dics[saleid]['tran_type2']=''
            if zt_price == Price:
                sell_dics[saleid]['tran_type2'] = '推动追卖'
            elif  Price >= last_row_price:
                sell_dics[saleid]['tran_type1'] = '普通挂卖,'
            elif Volume == BuyOrderVolume and Price < last_row_price:
                sell_dics[saleid]['tran_type2'] = '推动追卖,'
            elif Volume < BuyOrderVolume and Price < last_row_price:
                sell_dics[saleid]['tran_type2'] = '推动追卖,'
            else:
                sell_dics[saleid]['tran_type0'] = '卖,'
                #print(TranID)

        last_row_price = Price

        if row['Type'] == "B":
            sum_buy = sum_buy + row['Volume']

        else:
            sum_sell = sum_sell + row['Volume']

    #print("sum_buy:", sum_buy, "sum_sell:", sum_sell)



    rows = ceate_rows(sell_dics)
    df = pd.DataFrame(rows, columns=['id', 'is_jj', 'min_id', 'max_id', 'is_continue', 'is_continue_break', 'min_price',
                                     'max_price', 'price_count', 'start_time', 'end_time', 'max_vol', 'min_vol',
                                     'sum_vol', 'avg_vol', 'max_sale_vol', 'max_buy_vol','amount','id_count', 'tran_type0',
                                     'tran_type1', 'tran_type2'])
    df.to_csv("sale"+mi+".csv")

    rows = ceate_rows(buy_dics)
    df = pd.DataFrame(rows, columns=['id', 'is_jj', 'min_id', 'max_id', 'is_continue', 'is_continue_break', 'min_price',
                                     'max_price', 'price_count', 'start_time', 'end_time', 'max_vol', 'min_vol',
                                     'sum_vol', 'avg_vol', 'max_sale_vol', 'max_buy_vol','amount', 'id_count', 'tran_type0',
                                     'tran_type1', 'tran_type2'])
    df.to_csv("buy_"+mi+".csv")


def ceate_rows(my_dics):
    rows = []
    for key in my_dics.keys():
        #print(key, my_dics[key])

        data_row = []
        count = 0
        for key1 in my_dics[key]:
            data_row.append(my_dics[key][key1])
            count = count + 1
        rows.append(data_row)
        #print(count)
    # for item in rows:
    #    print(item)
    #print(rows[0:2])
    # df = pd.DataFrame(sell_dics)
    # df = df.stack()
    rows = rows[1:]
    return rows


def main():
    rq = '2020-01-15'
    stk_code = '603888'

    path = r"C:/data/csv/" + rq + "/"


    data_file = path+ stk_code + ".csv"
    #deal_gp(data_file,rq,stk_code)

    deal_gp_fb(data_file, rq, stk_code)











    stk_code='*'
    path = r"C:/Users/sun/Documents/" + rq + "/" + stk_code + ".csv"
    #deal_dir(path)








if __name__ == '__main__':
    main()


###
'''
# create table FDATA
# (
#   JDAY            VARCHAR2(10),
#   ID              VARCHAR2(10),
#   TRANID          VARCHAR2(10),
#   FBTIME          VARCHAR2(10),
#   PRICE           NUMBER,
#   VOLUME          NUMBER,
#   SALEORDERVOLUME NUMBER,
#   BUYORDERVOLUME  NUMBER,
#   FBTYPE          VARCHAR2(10),
#   SALEORDERID     VARCHAR2(10),
#   SALEORDERPRICE  VARCHAR2(10),
#   BUYORDERID      VARCHAR2(10),
#   BUYORDERPRICE   NUMBER
#   
# )


select t.buyorderid ,count(distinct t.fbtype),sum(t.volume) ,count( distinct t.buyordervolume),min(t.buyordervolume),max(t.buyordervolume) 
from  fdata t
group by  buyorderid 
having count( distinct t.buyordervolume) > 1
order by  count( distinct t.buyordervolume)  desc



select t.id,t.jday,   buyorderid  ,count(*),count(distinct t.fbtype),sum(t.volume) ,count( distinct t.buyordervolume),min(t.buyordervolume),max(t.buyordervolume) 
from  fdata t
group by  t.id,t.jday,   buyorderid 
having count(*) > 1  
order by  count( distinct t.buyordervolume)  desc



  create table FDATA
 (
   JDAY            VARCHAR(10),
   ID              VARCHAR(10),
   TRANID          VARCHAR(10),
   FBTIME          VARCHAR(10),
   PRICE           double,
   VOLUME          double,
   SALEORDERVOLUME double,
   BUYORDERVOLUME  double,
   FBTYPE          VARCHAR(10),
   SALEORDERID     VARCHAR(10),
   SALEORDERPRICE  VARCHAR(10),
   BUYORDERID      VARCHAR(10),
   BUYORDERPRICE   double
   ) 
   
   
   

# '''
###


# 使用execute方法执行SQL语句
#cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据库。
#data = cursor.fetchone()

#print("Database version : %s " % data)

# 关闭数据库连接

