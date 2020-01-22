# coding=gbk
import re, string
import os
import glob

# print type(os.listdir("."))
# glob.glob('c:\\music\\_singles\\*.mp3')
# for  i  in os.listdir("."):


import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("172.16.228.50","root","root123","ts" )

# 使用cursor()方法获取操作游标
cursor = db.cursor()




f2 = open(r"f:/day_alldata.sql", "w")

rq = '2020-01-16'

path =r"F:/BaiduYunDownload/2020-01-16/"+rq+"/*.csv"

print (path)
index = 100
for i in glob.glob(path ):
    index = index + 1
    name = i[-10:-4]
    print (name)
    if index>=103:
       break
    f = open(i, "r")
    lines = f.readlines()

    line_count = 0
    for line in lines:
        line_count = line_count+1
        if line_count==1:
            continue
        filds = line.split(',')


        #print (filds[0], filds[1], filds[2], filds[3], filds[4], filds[5], filds[6])(FDAY,ID,TRANID,TIME,PRICE,VOLUME,SALEORDERVOLUME,BUYORDERVOLUME,TYPE,SALEORDERID,SALEORDERPRICE,BUYORDERID,BUYORDERPRICE) values
        sql = " insert into    fdata values   ('" + rq + "','" + name + "','" + filds[
            0].strip() + "','" + filds[1].strip() + "','" + filds[2].strip() + "','" + filds[3].strip() + "','" + filds[
                  4].strip() + "','" + filds[5].strip() + "','" + filds[6].strip() + "','" + filds[7].strip() + "','" + filds[8].strip() + "','" + filds[9].strip() + "','" + filds[10].strip() +"') ;"

        # 使用execute方法执行SQL语句
        cursor.execute(sql)


        f2.write(sql + "\n")
        # print str(index)+","+name+","+stk[1:7]
        # break
# for item in ():









# 使用execute方法执行SQL语句
#cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据库。
#data = cursor.fetchone()

#print("Database version : %s " % data)

# 关闭数据库连接
db.close()




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