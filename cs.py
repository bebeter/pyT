#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

N=10


je = [0]*N

sj_zf = [2,2,2,2,2,0,0,0,0,0]  # 10次随机

zje = 1000000

mcgdje = [2000]*10

tz_zsr_list =[]

def tz():
    sj_zf_index = random.sample(range(0, 10), 10)
    pj_je = zje /500.0
    for i in range(0,len(je)):
        je[i] = pj_je
    zsr  = 0

    bjsy = zje
    ztr= 0

    for i in range(0,len(je)):


        yljc = zsr/5  #  总收入的一半
        if yljc>10000:
            yljc = 10000

        zsr =zsr - yljc  # 剩余的总收入

        bcsr  =  sj_zf[sj_zf_index[i]]*(mcgdje[i]+yljc )  #  本次盈利

        zsr = zsr+bcsr # 当前的总收入

        bjsy = bjsy - mcgdje[i]

        ztr =ztr +mcgdje[i]


        print(i,"投入固定金额" + str(mcgdje[i]) +"赢利加仓金额" ,yljc," 本次涨幅：", sj_zf[sj_zf_index[i]] ,"倍 本次收入:", bcsr  )
    print ("\n总收入：",str(zsr),"总投入:",ztr  , "总资产：" ,- ztr +zsr )
    tz_zsr_list.append(- ztr +zsr)




def main():
    for i in range(0,100):
        print (i)
        tz()

    new_list = sorted(tz_zsr_list)


    print( "\n\n\n\n")

    for i in range(0, 100):
        print( new_list[i],"\n")










if __name__ == '__main__':
    main()



