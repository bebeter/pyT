import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import talib


def MACD(data,short_,long_,m):
    '''
    data是包含高开低收成交量的标准dataframe
    short_,long_,m分别是macd的三个参数
    返回值是包含原始数据和diff,dea,macd三个列的dataframe
    '''
    data['MACD']=data['close'].ewm(adjust=False,alpha=2/(short_+1),ignore_na=True).mean()-\
                data['close'].ewm(adjust=False,alpha=2/(long_+1),ignore_na=True).mean()
    data['MACDAvg']=data['MACD'].ewm(adjust=False,alpha=2/(m+1),ignore_na=True).mean()
    data['MACDDiff']=2*(data['MACD']-data['MACDAvg'])
    data['0'] = data['MACDDiff']*0

    return data

'''通道函数'''
def highest(data, length=20):
    data = data.rolling(length, min_periods=1).max()
    return data


def lowest(data, length=20):
    data = data.rolling(length, min_periods=1).min()
    return data



"""-----------------获取1小时数据-------------"""
df = pd.read_csv("rb000_1h.csv")[0:50000]

k_length = 4
k_A = []
"-----------4小时数据-------------"
for i in range(len(df)):
    if i % (k_length) == 0:
        k_A.append(df['close'][i])

k_df = pd.DataFrame(data=k_A, columns=['close'])

"-----------MACD------------"
macd_1 = MACD(df,12,26,9 )
macd_5 = MACD(k_df,12,26,9 )

"-----------1小时通道------------"
highest = highest(df['high'],20)
lowest = lowest(df['low'],20)

k_list_MACD = []
k_list_MACDAvg = []
k_list_MACDDiff = []
k_list_0 = []
for i in range(len(macd_1)):

    if i % k_length == 0:
        k_list_MACD.append(macd_5['MACD'][i // k_length])
        k_list_MACDAvg.append(macd_5['MACDAvg'][i // k_length])
        k_list_MACDDiff.append(macd_5['MACDDiff'][i // k_length])
        k_list_0.append(0)

    if len(macd_1) - i > 0 and i % k_length != 0:
        k_list_MACD.append(k_list_MACD[-1])
        k_list_MACDAvg.append(k_list_MACDAvg[-1])
        k_list_MACDDiff.append(k_list_MACDDiff[-1])
        k_list_0.append(k_list_0[-1])

k_macd_value = pd.DataFrame(data=k_list_MACD,columns=['MACD'] )
k_macd_value['k_list_MACDAvg'] = k_list_MACDAvg
k_macd_value['k_list_MACDDiff'] = k_list_MACDDiff
k_macd_value['k_list_0'] = k_list_0


"------------空头信号------------"
Sellshort = []
for i in range(len(df)):

    if i ==0:
        Sellshort.append(0)

    if i >0:
        if df['low'][i]<lowest[i-1] and k_macd_value['k_list_MACDAvg'][i-1]<0:
            Sellshort.append(-1)
        elif df['high'][i]>highest[i-1]:
            Sellshort.append(1)
        else:
            Sellshort.append(0)

    if Sellshort[i] == 0:
        Sellshort[i]=Sellshort[i-1]


"------------多头信号------------"
buy = []
for i in range(len(df)):

    if i == 0:
        buy.append(0)

    if i > 0:
        if df['high'][i] > highest[i - 1] and k_macd_value['k_list_MACDAvg'][i - 1] > 0:
            buy.append(1)
        elif df['low'][i] < lowest[i - 1]:
            buy.append(-1)
        else:
            buy.append(0)

    if buy[i] == 0:
        buy[i] = buy[i - 1]

"------------多空开仓价格------------"
buy_entry = []
buy_exit = []
for i in range(len(df)):

    if buy[i]==1 and buy[i-1] == 0:
        buy_entry.append(highest[i]+1)

    if buy[i]==1 and buy[i-1] == -1:
        buy_entry.append(highest[i]+1)

    if buy[i] == -1 and buy[i - 1] == 1:
        buy_exit.append(lowest[i-1] - 1)

Sellshort_entry = []
Sellshort_exit = []
for i in range(len(df)):

    if Sellshort[i]==-1 and Sellshort[i-1] == 0:
        Sellshort_entry.append(lowest[i]-1)

    if Sellshort[i]==-1 and Sellshort[i-1] == 1:
        Sellshort_entry.append(lowest[i]-1)

    if Sellshort[i] == 1 and Sellshort[i - 1] == -1:
        Sellshort_exit.append(highest[i-1] + 1)
# print('----多头开平价格-------')
# print(buy_entry)
# print(buy_exit)
#
# print('----空头开平价格-------')
# print(Sellshort_entry)
# print(Sellshort_exit)
"------------多空累积盈亏、胜率、盈亏比------------"
buy_win_times =0
buy_fail_times =0
buy_win_profit =0
buy_fail_profit =0

sellshort_win_times =0
sellshort_fail_times =0
sellshort_win_profit =0
sellshort_fail_profit =0

buy_profit = []
sellshort_profit =[]
S = 0
B = 0

"-----统计空头累积盈亏-----"
for i in range(min(len(Sellshort_entry),len(Sellshort_exit) )):

    S = S + (Sellshort_entry[i] - Sellshort_exit[i]) #-------"空总盈亏"
    sellshort_profit.append(Sellshort_entry[i] - Sellshort_exit[i]) #-------"空单笔盈亏"

    if sellshort_profit[i]>0:
        sellshort_win_times = sellshort_win_times + 1 #-------"空盈利次数"
        sellshort_win_profit = sellshort_win_profit + sellshort_profit[i]

    if sellshort_profit[i]<=0:
        sellshort_fail_times = sellshort_fail_times + 1 #-------"空亏损次数"
        sellshort_fail_profit = sellshort_fail_profit + sellshort_profit[i]



"-----统计多头累积盈亏-----"
for i in range(min(len(buy_entry),len(buy_exit) )):

    B = B + (-buy_entry[i] + buy_exit[i]) #-------"多总盈亏"
    buy_profit.append(-buy_entry[i] + buy_exit[i]) #-------"多单笔盈亏"

    if buy_profit[i]>0:
        buy_win_times = buy_win_times + 1 #-------"多盈利次数"
        buy_win_profit = buy_win_profit + buy_profit[i]

    if buy_profit[i]<=0:
        buy_fail_times = buy_fail_times + 1 #-------"多亏损次数"
        buy_fail_profit = buy_fail_profit + buy_profit[i]


# print('----多头累积盈亏-------')
# print(B)
#
# print('----多头单笔盈亏-------')
# print(buy_profit)
#
#
# print('----多头盈利和亏损次数-------')
# print(buy_win_times)
# print(buy_fail_times)
#
# print('----多头总盈利和多头总亏损-------')
# print(buy_win_profit)
# print(buy_fail_profit)



win_times_all = sellshort_win_times+buy_win_times
fail_times_all = sellshort_fail_times+buy_fail_times

win_profit_all =sellshort_win_profit+buy_win_profit
fail_profit_all =sellshort_fail_profit+buy_fail_profit

胜率 = win_times_all/(win_times_all+fail_times_all)
盈亏比 = win_profit_all /-fail_profit_all

print('累积盈亏:', win_profit_all+fail_profit_all)
print('胜率:', 胜率)
print('盈亏比:', 盈亏比)
print('盈利次数:', win_times_all)
print('亏损次数:', fail_times_all)
print('总盈利:', win_profit_all)
print('总亏损:', fail_profit_all)


"""-----------------可视化-------------"""
fig,(ax1,ax2,ax3,ax4) = plt.subplots(4,1,figsize=(10,10))

ax1.plot(df[['close']])
ax1.plot(highest)
ax1.plot(df['low'])
ax1.plot(df['high'])
ax1.plot(lowest)

#ax2.plot(Sellshort,'g')
ax2.plot(buy,'r')
#
# ax3.plot(macd_1['MACD'])
# ax3.plot(macd_1['MACDAvg'])
# ax3.plot(macd_1['MACDDiff'])

# ax3.plot(k_list_MACD)
ax3.plot(k_list_MACDAvg)
# ax3.plot(k_list_MACDDiff)
ax3.plot(k_list_0,'gray')
ax3.legend(['MACDAvg'])
ax3.legend([''])
plt.show()
