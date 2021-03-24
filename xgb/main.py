# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import scipy as sp
import statsmodels.tsa.stattools as sts
import matplotlib.pyplot as plt
import statsmodels.api as sm
import talib
import datetime
'''
etf ="510050.XSHG"
startdte='2003-1-1'
enddte='2019-10-30'
train_end='2016-12-31'

print('#########################开始计算'+enddte+'策略################################')
print('开始下载并分析'+instruments(etf).symbol+'...')
price=get_price(etf,start_date=startdte, end_date=enddte,fields=['high','low','close','open','volume'])
print(price.index[0])
'''




def devfea(df,high,low,close,open,volume):
    df['AD']=talib.AD(high,low,close,volume)
    df['CCI']=talib.CCI(high,low,close)
    df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df['ATR'] = talib.ATR(high, low, close, timeperiod=14)
    df['ADOSC']=talib.ADOSC(high,low,close,volume)
    df['ADX']=talib.ADX(high,low,close)
    df['BBANDS_upper'],df['BBANDS_mid'],df['BBANDS_lower']=talib.BBANDS(close)
    df['RSI']=talib.RSI(close)
    df['MA5']=talib.MA(close,5)
    df['MA10']=talib.MA(close,10)
    df['MA20']=talib.MA(close,20)
    df['OBV']=talib.OBV(close,volume)
    df['SAR']=talib.SAR(high, low)
    df['lgvol']=np.log(volume)
    #上影线
    df['upshadow']=np.abs(high-((open+close)+(np.abs(open-close)))/2)
    #下影线
    df['downshadow']=np.abs(low-((open+close)-(np.abs(open-close)))/2)
    return df

def devfea_roll(df,cols,ndays):
    fea=df[cols].rolling(ndays).agg(['mean','max','min','std','var','median'])
    fea.columns=["_".join(col) for col in fea.columns]
    fea.columns=fea.columns+'_rl_'+str(ndays)+'D'
    res=pd.merge(df,fea,left_index=True,right_index=True,how='inner')
    return res

def devfea_diff(df,cols,ndays):
    fea=df[cols].diff(ndays)
    fea.columns=fea.columns+'_diff_'+str(ndays)+'D'
    res=pd.merge(df,fea,left_index=True,right_index=True,how='inner')
    return res

def devfea_diff2(df,cols):
    fea=df[cols].diff(1).diff(1)
    fea.columns=fea.columns+'_diff2'
    res=pd.merge(df,fea,left_index=True,right_index=True,how='inner')
    return res

def devfea_lag(df,cols,ndays):
    fea=df[cols].shift(ndays)
    fea.columns=fea.columns+'_lag_'+str(ndays)+'D'
    res=pd.merge(df,fea,left_index=True,right_index=True,how='inner')
    return res




# In[44]:


def cumulative_returns_plot(StockReturns):
    CumulativeReturns = ((1+StockReturns).cumprod()-1)
    CumulativeReturns.plot()
    #print(str(CumulativeReturns[-1]))
    plt.legend()
    plt.show()




















# 策略中必须有init方法
def init(context):
    # 订阅浦发银行的分钟bar行情
    context.symbol = 'SHSE.510050'
    subscribe(symbols=context.symbol, frequency='1d')
    start_date = '2016-03-01'  # SVM训练起始时间
    end_date = '2021-03-20'  # SVM训练终止时间
    enddte='2019-10-30'
    train_end='2016-12-31'
    # 用于记录工作日
    # 获取目标股票的daily历史行情
    price = history(context.symbol, frequency='1d', start_time=start_date, end_time=end_date,fields='high,low,close,open,volume', fill_missing='last',
                          df=True)
    print(price)
    print(price.index)
    #days_value = price['bob'].values
    #days_close = price['close'].values
    days = []

    cols=price.pipe(devfea,price['high'],price['low'],price['close'],price['open'],price['volume']).columns
    print(type(price['high'][1]))
    result=(price.pipe(devfea,price['high'],price['low'],price['close'],price['open'],price['volume'])
                .pipe(devfea_roll,cols,5)
                .pipe(devfea_roll,cols,10)
                .pipe(devfea_roll,cols,20)
                .pipe(devfea_roll,cols,30)
                .pipe(devfea_roll,cols,60)
                .pipe(devfea_diff,cols,1)
                .pipe(devfea_diff,cols,5)
                .pipe(devfea_diff,cols,10)
                .pipe(devfea_diff,cols,20)
                .pipe(devfea_diff,cols,30)
                .pipe(devfea_diff,cols,60)
                .pipe(devfea_lag,cols,1)
                .pipe(devfea_lag,cols,2)
                .pipe(devfea_lag,cols,3)        
                .pipe(devfea_lag,cols,5)
                .pipe(devfea_diff2,cols)
        )

    result['long_MA5_flag']=(result['close']>result['MA5'])*1
    result['long_MA10_flag']=(result['close']>result['MA10'])*1
    result['long_MA20_flag']=(result['close']>result['MA20'])*1
    result['long_MA5_MA10']=(result['MA5']>result['MA10'])*1
    result['long_MA5_MA20']=(result['MA5']>result['MA20'])*1
    #alpha001 量价协方差，量价背离#
    result['aphla001']=result['close'].rolling(10).corr(result['volume'])
    #Alpha002 开盘缺口
    result['alpha002']=result['open']/result['close']
    #Alpha003 异常交易量
    result['alpha003']=-1*result['volume']/talib.MA(result['volume'],20)
    #Alpha004 量幅背离
    result['alpha004']=(result['high']/result['close']).rolling(10).corr(result['volume'])
    #Alpha005 近10日价格排序值
    def ts_rank(x):
        return pd.Series(x).rank().tail(1)
    result['alpha005']=result['close'].rolling(10,min_periods=10).apply(ts_rank)
    #Alpha006 近10日价格排序值中10的个数
    def ts_rankeq10(x):
        res=(x==10)*1
        return res.sum()
    result['alpha006']=result['alpha005'].rolling(10,min_periods=10).apply(ts_rankeq10)
    #Alpha007 最高价是近10日最高
    result['alpha007']=(result['high']==result['high_max_rl_10D'])*1
    #Alpha008 最高价是近20日最高
    result['alpha008']=(result['high']==result['high_max_rl_20D'])*1
    #Alpha009 最高价是近10日最高
    result['alpha009']=(result['low']==result['low_min_rl_10D'])*1
    #Alpha010 最高价是近20日最高
    result['alpha010']=(result['low']==result['low_min_rl_20D'])*1


    # In[11]:


    StockReturns = price['close'].pct_change(1).dropna()
    StockReturns.name='return'
    #print(StockReturns.head(5))
    StockReturns.index=price.index[0:-1]


    # In[42]:


    X_Matrix=pd.merge(result,StockReturns,left_index=True,right_index=True,how='inner')

    #Train and Test data
    X=X_Matrix[0:300][result.columns]
    y=X_Matrix[0:300]['return']
    #valid data
    x_valid=X_Matrix[300:][result.columns]
    y_valid_return=X_Matrix[300:]['return']


    from sklearn.model_selection import train_test_split
    import xgboost as xgb
    from sklearn import metrics
    from sklearn.model_selection import ShuffleSplit

    # 参数设置
    params = {
        'booster': 'gbtree',
        'objective': 'reg:linear',
    #'eval_metric': 'auc',
        'gamma': 0,
        'max_depth': 8,
        'subsample': 0.7,
        'colsample_bytree': 0.7,
        'min_child_weight': 6,
        'silent': 1,
        'eta': 0.007,
        'seed': 1000,  
        'nthread': 6,
    }

    rs = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
    model=[]
    for train_index, test_index in rs.split(X):
        X_train, X_test = X.iloc[train_index,:], X.iloc[test_index,:]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        dtrain = xgb.DMatrix(X_train, label = y_train)
        dtest = xgb.DMatrix(X_test,label=y_test)
        watchlist = [(dtrain,'Train'),(dtest,'Val')]
        bst=xgb.train(params,dtrain,num_boost_round=3000,evals=watchlist, early_stopping_rounds=500)
        model.append(bst)


    yvalid_list=[]
    for m in model:
        dvalid = xgb.DMatrix(x_valid)
        yvalid_list.append(m.predict(dvalid))
    yvalid=np.array([i for i in yvalid_list]).mean(axis=0)


    y_valid=(yvalid>0)*1
    cumulative_returns_plot(y_valid_return*y_valid)
    cumulative_returns_plot(y_valid_return)


    y_valid=(yvalid>=0.001)*1
    cumulative_returns_plot(y_valid_return*y_valid)
    cumulative_returns_plot(y_valid_return)


    # save model to file
    import pickle
    pickle.dump(model, open("model_50etf_20191109.dat", "wb"))

    pickle.dump(result.columns, open("col_50etf_20191109.dat", "wb"))




if __name__ == '__main__':
    '''
        strategy_id策略ID, 由系统生成
        filename文件名, 请与本文件名保持一致
        mode运行模式, 实时模式:MODE_LIVE回测模式:MODE_BACKTEST
        token绑定计算机的ID, 可在系统设置-密钥管理中生成
        backtest_start_time回测开始时间
        backtest_end_time回测结束时间
        backtest_adjust股票复权方式, 不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
        backtest_initial_cash回测初始资金
        backtest_commission_ratio回测佣金比例
        backtest_slippage_ratio回测滑点比例
        '''
    run(strategy_id='65141f42-8be6-11eb-a1d3-b4a9fc1573f9',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='3ecaffcc418c72f212efe835d5a8fa35f1df32f5',
        backtest_start_time='2020-11-01 08:00:00',
        backtest_end_time='2020-11-10 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=10000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001)

