
#!/usr/bin/python
#-*- encoding: gbk -*-
from __future__ import division
from  struct  import   *
import os,time ,datetime,string,sys,math,re,shutil,glob
import zipfile,getopt
#from readths2 import *



#############################################################
# 一个时间对应的5分钟区间段
# dt 传入参数 为一个datetime.datetime or datetime.time
# 返回datetime 或time
#############################################################
def which5min(dt):
    """5 分钟时间划分 """
    if type(dt) != datetime.datetime and  type(dt) != datetime.time:
       return None
    t = dt
    ret = None
    if type(dt) == datetime.datetime:
       t = datetime.time(dt.hour,dt.minute,dt.second)

    if t < datetime.time(9,30) : return None
    if   t < datetime.time(9,35): ret = datetime.time(9,35)
    elif t < datetime.time(9,40): ret = datetime.time(9,40)
    elif t < datetime.time(9,45): ret = datetime.time(9,45)
    elif t < datetime.time(9,50): ret = datetime.time(9,50)
    elif t < datetime.time(9,55): ret = datetime.time(9,55)
    elif t < datetime.time(10,0): ret = datetime.time(10,0)
    elif t < datetime.time(10,5): ret = datetime.time(10,5)
    elif t < datetime.time(10,10): ret = datetime.time(10,10)
    elif t < datetime.time(10,15): ret = datetime.time(10,15)
    elif t < datetime.time(10,20): ret = datetime.time(10,20)
    elif t < datetime.time(10,25): ret = datetime.time(10,25)
    elif t < datetime.time(10,30): ret = datetime.time(10,30)
    elif t < datetime.time(10,35): ret = datetime.time(10,35)
    elif t < datetime.time(10,40): ret = datetime.time(10,40)
    elif t < datetime.time(10,45): ret = datetime.time(10,45)
    elif t < datetime.time(10,50): ret = datetime.time(10,50)
    elif t < datetime.time(10,55): ret = datetime.time(10,55)
    elif t < datetime.time(11,0): ret = datetime.time(11,0)
    elif t < datetime.time(11,5): ret = datetime.time(11,5)
    elif t < datetime.time(11,10): ret = datetime.time(11,10)
    elif t < datetime.time(11,15): ret = datetime.time(11,15)
    elif t < datetime.time(11,20): ret = datetime.time(11,20)
    elif t < datetime.time(11,25): ret = datetime.time(11,25)
    elif t <= datetime.time(11,30): ret = datetime.time(11,30)
#    elif t < datetime.time(13,0): ret = datetime.time(13,0)
    elif t < datetime.time(13,5): ret = datetime.time(13,5)
    elif t < datetime.time(13,10): ret = datetime.time(13,10)
    elif t < datetime.time(13,15): ret = datetime.time(13,15)
    elif t < datetime.time(13,20): ret = datetime.time(13,20)
    elif t < datetime.time(13,25): ret = datetime.time(13,25)
    elif t < datetime.time(13,30): ret = datetime.time(13,30)
    elif t < datetime.time(13,35): ret = datetime.time(13,35)
    elif t < datetime.time(13,40): ret = datetime.time(13,40)
    elif t < datetime.time(13,45): ret = datetime.time(13,45)
    elif t < datetime.time(13,50): ret = datetime.time(13,50)
    elif t < datetime.time(13,55): ret = datetime.time(13,55)
    elif t < datetime.time(14,0): ret = datetime.time(14,0)
    elif t < datetime.time(14,5): ret = datetime.time(14,5)
    elif t < datetime.time(14,10): ret = datetime.time(14,10)
    elif t < datetime.time(14,15): ret = datetime.time(14,15)
    elif t < datetime.time(14,20): ret = datetime.time(14,20)
    elif t < datetime.time(14,25): ret = datetime.time(14,25)
    elif t < datetime.time(14,30): ret = datetime.time(14,30)
    elif t < datetime.time(14,35): ret = datetime.time(14,35)
    elif t < datetime.time(14,40): ret = datetime.time(14,40)
    elif t < datetime.time(14,45): ret = datetime.time(14,45)
    elif t < datetime.time(14,50): ret = datetime.time(14,50)
    elif t < datetime.time(14,55): ret = datetime.time(14,55)
    elif t <= datetime.time(15,0):  ret = datetime.time(15,0)
    else : return None
    if type(dt) == datetime.datetime:
       return datetime.datetime(dt.year,dt.month,dt.day,ret.hour,ret.minute,ret.second)
    else: return ret

if __name__ == '__main__':

    t = which5min(datetime.time(9,34))  #找对应5分钟的区段
    print(t)