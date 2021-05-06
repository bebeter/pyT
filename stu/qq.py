#!/usr/bin/env python
# coding:utf-8
from PoboAPI import *
import datetime
import time
import numpy as np
#日线级别
#开始时间，用于初始化一些参数
def OnStart(context) :
    print("I\'m starting...")
    #设定一个全局变量品种,本策略交易50ETF期权
    g.code = "510050.SHSE"
    #登录交易账号，需在主页用户管理中设置账号，并把回测期权替换成您的账户名称
    context.myacc = None
    if "回测期权" in context.accounts :
        print("登录交易账号[回测期权]")
        if context.accounts["回测期权"].Login() :
            context.myacc = context.accounts["回测期权"]

def OnMarketQuotationInitialEx(context,exchange,daynight):
    if exchange!='SHSE':
        return
    #     #订阅实时数据，用于驱动OnQuote事件
    #     SubscribeQuote(g.code)
    #订阅日线级别K线数据，用于驱动OnBar事件
    SubscribeBar(g.code,BarType.Day)

#自定义函数， 用于获取当月虚值一档的认购和认沽期权
def Getop(code):
    #获取实时行情
    dyndata = GetQuote(code)
    #获取最新价
    now1 = dyndata.now
    #获取虚值一档价格
    now50 = round(now1,1) + 0.05
    #获取当前时间
    cutime = GetCurrentTime()
    #获取当月期权到期时间
    #若当前时间处于当月15号之后，则到期月份向后推一个月
    if cutime.day >15 and cutime.month<12:
        tim = cutime.month + 1
        month_time = datetime.datetime(month=tim, year=cutime.year,day = 20)
    #若当前时间处于12.15之后，则取下一年的1.20为到期时间
    elif cutime.day >15 and cutime.month==12:
        tim = 1
        yea = cutime.year + 1
        month_time = datetime.datetime(month=tim, year=yea,day = 20)
    #若当前时间处于上半月，则取当前时间
    else:
        month_time = cutime
    #获取当月虚值一档的认购和认沽期权
    atmopc = GetAtmOptionContract(code,month_time,now50,0)
    atmopp =  GetAtmOptionContractByPos( code, "now", 3, 1, None ) #GetAtmOptionContract(code,month_time,now50,1)
    #返回获取到的认购认沽
    return atmopc,atmopp

#自定义函数，用于计算合约截至到期剩余天数
def stime(op):
    #获取合约信息
    info1 = GetContractInfo(op)
    #获取该合约的行权到期日
    kill = info1['行权到期日']
    #获取当前时间
    cutime = GetCurrentTime()
    #获取当前时间的日期
    c = cutime.date()
    #计算当前日期与行权到期日相差天数
    n = (kill - c).days
    print(n)
    #返回合约截至到期剩余天数
    return n

#K线事件
def OnBar(context,code,bar_type):
    #过滤掉不需要的行情通知
    if code != g.code :
        return

    #获取最新行情
    dyndata = GetQuote(g.code)
    if dyndata :
        #.now指最新价，详细属性见API文档i
        now1 = dyndata.now
        #打印最新价，和对应时间
        log.info("最新价: " + str(dyndata.now) + str(dyndata.time))
    #获取持仓信息
    posi = context.myacc.GetPositions()
    #打印持仓合约支数
    print(len(posi))

    #获取历史信息
    b = CreateCalcObj()#建立一个参数对象，对历史信息进行筛选
    option = PBObj()
    option.EndDate = GetCurrentTime()#获取截至目前的历史信息
    option.Count = 60 #一共获取60条历史信息
    #获取最近60天的收盘价列表
    klist = GetHisDataByField(g.code, BarType.Day, "close", option)
    #计算历史波动率
    if len(klist)>0:
        Kl = np.array(klist, dtype=np.double)
        c=b.GetVolatility(Kl)
        print("历史波动率")
        print(c)
    #若没有持仓，并且历史波动率小于0.35，则开仓

    day_count = stime(opp)
    cutime = GetCurrentTime()

    if len(posi) == 0 and cutime.day >20 and day_count>20 and day_count<30 :
        opc,opp = Getop(g.code)
        print(str(opc))
        #获取期权的实时行情
        dync = GetQuote(opc)
        dynp = GetQuote(opp)
        if dync != None:
            #打印期权最新价
            log.info("最新价2: " + str(dync.now))
            log.info("最新价3: " + str(dynp.now))
            #使用最新价做空各50手认购和认沽期权
            #context.myacc.InsertOrder(opc, BSType.SellOpen, dync.now, 250)
            context.myacc.InsertOrder(opp, BSType.SellOpen, dynp.now, 250)




    #若有持仓，进行平仓处理
    elif len(posi) >1:
        print(len(posi))
        #获取持仓合约
        opcode1 = posi[0].contract
        #opcode2 = posi[1].contract
        #获取持仓合约的最新价
        dyn1 = GetQuote(opcode1)
        #dyn2 = GetQuote(opcode2)
        #获取持仓合约的行权价格和到期日
        info1 = GetContractInfo(opcode1)
        pr1 = info1['行权价格']
        ki1 = info1['行权到期日']
        #info2 = GetContractInfo(opcode2)
        #pr2 = info2['行权价格']
        #计算合约截至目前剩余天数
        sy = stime(opcode1)
        print(str(pr1) + '行权价格')
        #print(str(pr2) + '行权价格2')
        print(sy)
        #若距离到期日不足3天，则使用最新价平仓
        if sy<1:
            context.myacc.InsertOrder(opcode1, BSType.BuyClose, dyn1.now, 250)
            #context.myacc.InsertOrder(opcode2, BSType.BuyClose, dyn2.now, 250)
        #若最新价大于行权价或者最新价小于行权价的85%， 则用最新价平仓
        elif now1 >= pr1 or now1 <= (pr1-0.15):
            context.myacc.InsertOrder(opcode1, BSType.BuyClose, dyn1.now, 250)
            #context.myacc.InsertOrder(opcode2, BSType.BuyClose, dyn2.now, 250)

#委托回报事件，当有委托回报时调用
def OnOrderChange(context, AccountName, order) :
    #打印委托信息，id是编号，volume是数量，详细见API文档
    print("委托编号： " + order.id + "   账号名称： " + AccountName)
    print("Vol: " + str(order.volume) + " Price: " + str(order.price))

