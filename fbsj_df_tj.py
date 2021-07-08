# coding=gbk

import glob
import os
import time  # 1. 获取时间元组

import numpy as np
import pandas as pd




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
    #C:\l2data\202007\2020-07-13
    f2 = open(r"c:/l2data/202007/"+rq+"/"+stk_code+".csv", "a")
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
    #lastClose = getLastClose(rq, stk_code)
    #zt_price = getZt(lastClose)



    df = pd.read_csv(fn, header=0,dtype={'Time':str}) #, index_col=0
    ''' 
    print(df.head(5))
    dict_m1={'Price':'min','Price':'max','Price':'count'}
    dd= df.groupby(df['SaleOrderID']).agg(dict_m1)#count(df['Price'])
    print(dd.head(15))
    # means=df['Price'].groupby([df['SaleOrderID']]).count()
    sale_count = df.groupby('SaleOrderID').agg({'Price': pd.Series.nunique})
    print(sale_count[sale_count['Price']>1])  #成交了两个价格的卖单
    '''
    df['vol']=df['Price']*df['Volume']
    sale_df = df.groupby('SaleOrderID').agg({'Time':[('time_min','min'),('time_max','max')],'vol':'sum','Price': [pd.Series.nunique,'mean'],'SaleOrderVolume': 'max','Volume':['sum','mean','max'],'BuyOrderID':'count'}).sort_values(by=[('Time','time_min')],ascending=[True])
    print(sale_df)  #成交了两个价格的卖单"大于10w股的主动卖单："+
    #print(sale_df['Time']['time_min'])
    #print(sale_df.iloc[:,3:6])   #['Volume']['sum'>100000]
    #print(sale_df[sale_df.iloc[:,2]>1])
    #成交价格有1个的单子
    df1= sale_df[sale_df[('Price','nunique')]<=1]
    print(" 一个价位成交的金额总计：")
    print(df1[('vol','sum')].sum() )
    df2= df1[df1[('Volume','sum')]<100000]
    print("小于10w手 一个价位 金额总计：")
    print(df2[('vol','sum')].sum() )
    #成交股数大有10w股的
    df2= df1[df1[('Volume','sum')]>=100000]
    #print(df2)
    print("大于10w手 一个价位 金额总计：")
    print(df2[('vol','sum')].sum() )




    #成交价格有多个的单子
    df1= sale_df[sale_df[('Price','nunique')]>1]
    #print(df1)
    print("成交价格有多个的单子 金额总计：")
    print(df1[('vol','sum')].sum() )

    ''' 
    df2= df1[df1[('Volume','sum')]<100000]
    print("小于10w手 多个价位 金额总计：")
    print(df2[('vol','sum')].sum() )
    #成交股数大有10w股的
    df2= df1[df1[('Volume','sum')]>=100000]
    #print(df2)
    print("大于10w手 多个价位 金额总计：")
    print(df2[('vol','sum')].sum() )
    
    '''
    sale_df.to_csv("sale_df_"+mi+".csv")


    data = df1[[('Time','time_min'),('vol','sum')]]  #df1.iloc[:,0,2]
    print(data)
    data1= data['Time']
    print(data1)
    data2= data['vol']
    print(data2)
    data3 = (pd.merge(data1,data2,on='SaleOrderID'))
    #data3['tm'] = pd.to_numeric(data3['time_min'].apply(str).replace(":",'')) #

    #散点图
    #data3['tm'] =  data3['time_min'].str.replace(":",'').astype('int')
    #print(data3)
    #print(data3.dtypes)
    #data3.plot.scatter(x="tm",y="sum",color="red",alpha=0.3)
    #plt.show()



    #buy_df = df.groupby('BuyOrderID').agg({'Time':'min','Price': pd.Series.nunique,'SaleOrderVolume': np.max,'Volume':'sum','SaleOrderID':'count'})
    buy_df = df.groupby('BuyOrderID').agg({'Time':[('time_min','min'),('time_max','max')],'vol':'sum','Price':[pd.Series.nunique,'mean'],'BuyOrderVolume': 'max','Volume':['sum','mean','max'],'SaleOrderID':'count'}).sort_values(by=[('Time','time_min')],ascending=[True])
    buy_df.to_csv("buy_df_"+mi+".csv")
    print(buy_df)  #成交了两个价格的卖单









def main():
    start =  time.perf_counter()
    rq = '2021-05-12'
    stk_code = '600733'
    fn = r"C:\Users\sun\Documents\2020-11-27\600733.csv"

    path = "C:/l2data/" +rq[0:4]+rq[5:7]+ "/" + rq+"/"

    data_file = path+ stk_code + ".csv"
    #deal_gp(data_file,rq,stk_code)
    #data_file = r"C:\Users\sun\Documents\2020-11-27\600733.csv"
    deal_gp_fb(data_file, rq, stk_code)
    end = time.perf_counter()
    print ("time:   "+str(end-start))










    stk_code='*'
    path = r"C:/Users/sun/Documents/" + rq + "/" + stk_code + ".csv"
    #deal_dir(path)








if __name__ == '__main__':
    main()
