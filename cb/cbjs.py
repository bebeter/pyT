# coding=gbk
import random
import sys


all_account=[]#全部持股帐户 前4个为限售
gdzs=0
base_diretory="E:\\ts\\data"
hb_a=0
hb_m=0.0
dayCanBuy=[]
dayCanSell=[]
class Account:

    def __init__ (self,id,type,money,amount,day_buy_amount,day_sell_amount) :
        self.id = id
        self.type = type#操作类别
        self.money = money#当前现金
        self.amount = amount #当前总数
        self.pj_price = 0
        self.day_buy_amount =day_buy_amount;
        self.day_sell_amount =day_sell_amount;
        #self.day_can_buy = ;
        self.day_can_sell =amount-day_buy_amount-day_sell_amount;
    def setAmount(self, amount):
        self.amount = amount
    def getAmount(self):
        return self.amount


    def buy(self,buy_amount,total_money):
        print ("buy"+buy_amount )
        if(self.money>=total_money):
            self.money=self.money-total_money
            self.amount=self.amount+buy_amount
            self.day_buy_amount =self.day_buy_amount+buy_amount;

    def sell(self,sell_amount,total_money):
        print ("sell")
        if(self.day_can_sell>=0):
            self.money=self.money+total_money
            self.amount=self.amount-self.buy_amount
            self.day_sell_amount =self.day_sell_amount+sell_amount;
def createAllAccount():

   for i in range(0,30000):#20万个帐户
      id = i
      type = random.randint(1, 10),#操作类别
      money = random.randint(10000, 800000000)#当前现金
      amount = 0 #当前总数
      day_buy_amount =0;
      day_sell_amount =0;
      a = Account(id,type,money,amount,day_buy_amount,day_sell_amount)
      all_account.append(a)

#给代码加上市场字母
def marketstr(dm):
    #print dm,dm[0]
    if dm[0]==str(6):
        dm='sh'+dm
    elif dm[0]==str(3) or dm[0]==str(0):
        dm='sz'+dm
    #print dm
    return dm


def getRq(dm):
      f=open(base_diretory+"\\TXTDAY\\"+marketstr(dm)+".txt","r")
      rq= []
      for line in f.readlines():
        daydata=line[:-1].split(",")
        rq.append(daydata[0].replace("/","-"))
      f.close()
      return rq
def fen_Gu():
    global gdzs
    #print len(all_account),all_account[0]
    f=open("sg.txt","r")
    lines=f.readlines()
    line_no=0
    for line in lines:
        #print line
        line_no=line_no+1
        if line_no==1:
           hang1 = line.split(",")
           ltguben=float(hang1[0])
           fxj=float(hang1[1])#发行价
           gdzs=int(hang1[2])
           pjcg=float(hang1[3])
        else:
           shida_gudong= line.split(",")
           #print shida_gudong
           #print len(all_account),all_account[0]
           all_account[line_no-2].amount=int(float(shida_gudong[0]))*10000
           all_account[line_no-2].pj_price=(fxj)
    f.close()
    for i in range(10,int(gdzs)):
       all_account[i].amount=500
       all_account[i].pj_price=fxj
       all_account[i].money-=fxj*500
    #按股东人数分配固定股票500
    gdfp=int(float(ltguben))*10000-500*(int(gdzs)-10)-6000000
    #print "df",DF
    for k in range(0,gdfp,500):
       x= random.randint(10,int(gdzs)/20)
       while (1):
           if  all_account[x].money>=fxj*500 :
               break
           else:
              x= random.randint(10,int(gdzs)/20)
       all_account[x].amount+=500#int(gdzs) 减小一些 使得持股集中一些
       all_account[x].pj_price=fxj
       all_account[x].money-=fxj*500
def sum_gu():
    sum=0
    print (gdzs)
    for i in range(0,gdzs):
        #if i<15:
        #  print "持股 ",i,all_account[i].amount


        #if int(float(all_account[i].amount))>500:
        #    print i,int(float(all_account[i].amount))
        sum+=int(float(all_account[i].amount))





def fen_mb(price,amount,money):
    #print "\n\nfen_mb:",price,amount,money
    global hb_a,hb_m
    hb_a +=amount
    hb_m +=money
    nowBuyAmount = amount # 买单当前大小
    nowSellAmount =amount # 卖单当前大小
    nowBuyMoney = money
    nowSellMoney = money
    deal_sell_amount =0
    deal_buy_amount =0
    #处理卖
    while(nowSellAmount>0):
        #print "len(dayCanSell)",len(dayCanSell)

        sellId = dayCanSell[ random.randint(0, len(dayCanSell)-1)]
        canSell = int(all_account[sellId].amount -all_account[sellId].day_buy_amount)
        #print "nowSellAmount:",nowSellAmount,"canSell",canSell
        if(canSell>=nowSellAmount):
            deal_sell_amount+=nowSellAmount
            #print "\n\n!!sell am0",all_account[sellId].amount
            all_account[sellId].amount-=nowSellAmount
            #print "\nsell am1",nowSellAmount,all_account[sellId].amount
            all_account[sellId].money+=nowSellMoney
            canSell-=nowSellAmount
            nowSellAmount=0

        else:
            deal_sell_amount+=canSell
            all_account[sellId].money+=price*canSell
            #print "\n\n!!sell am3",all_account[sellId].amount
            all_account[sellId].amount-=canSell
            #print "\n\n!!sell am4",canSell,all_account[sellId].amount
            nowSellAmount -= canSell
            canSell=0
        if canSell==0:
                dayCanSell.remove(sellId)
    #print "deal_sell_amount:",deal_sell_amount
    #处理买单
    while(nowBuyAmount>0):
            #buyId=5500
            #while(buyId>5000):
            buyId = dayCanBuy[ random.randint(0, (len(dayCanBuy)-1))] #随机生成一个要买的帐号

            canBuy = int(all_account[buyId].money/price)#计算该账户能买的手数
            #print "nowBuyAmount:",nowBuyAmount,"canBuy:",canBuy
            #print "buy",len(dayCanBuy),nowBuyAmount,canBuy
            if(canBuy>=nowBuyAmount): #能买手数 大于要处理的买单 直接消化买单
                deal_buy_amount+=nowBuyAmount
                buyed_money = all_account[buyId].pj_price * all_account[buyId].amount + nowBuyMoney

                buyed_amount = all_account[buyId].amount + nowBuyAmount

                all_account[buyId].pj_price =round(buyed_money / buyed_amount,2)#计算帐户持仓 平均价格

                #print "\n\n!!buy am0",all_account[buyId].amount
                all_account[buyId].amount+=nowBuyAmount  #记入帐户总股数
                #print "\n\n!!buy am1",nowBuyAmount,all_account[buyId].amount
                all_account[buyId].money-=nowBuyMoney #当前帐号现金
                all_account[buyId].day_buy_amount +=nowBuyAmount #设置当日买的数量
                canBuy-= nowBuyAmount
                nowBuyAmount=0#设置当前买单大小为0 跳出循环

            else: #帐户能买的手数 小于 单子的剩余量
                deal_buy_amount+=canBuy
                buyed_money = all_account[buyId].pj_price * all_account[buyId].amount + price * canBuy
                buyed_amount = all_account[buyId].amount + canBuy
                all_account[buyId].pj_price =round( buyed_money / buyed_amount,2)
                #print "\n\n!!buy am3",all_account[buyId].amount
                all_account[buyId].amount += canBuy #帐户拥有的数量
                #print "\n\n!!buy am4",canBuy,all_account[buyId].amount
                all_account[buyId].day_buy_amount +=canBuy #设置当日买的数量
                all_account[buyId].money-=price*canBuy #处理帐户剩下的资金
                nowBuyAmount-=canBuy
                canBuy= 0  #能买的全买

            if canBuy==0:
                    dayCanBuy.remove(buyId);
    #print "deal_buy_amount",deal_buy_amount
    #print amount
    '''
    if(deal_sell_amount!=deal_buy_amount):
        print "not eq :",amount,deal_buy_amount,deal_buy_amount
    if not qs_day():
        print "XXXXXXXXXXXXX"
        sys.exit(0)
    else:
        print "$$$$$$$$$$$$$"
    '''



def fen_fs(price,amount,money):
    #print "\n\n\n原单1：" ,price,amount,money
    while(amount>1):
       # print "剩余数量：",amount,money
        b_amount = random.randint(1, amount) #1手或
        b_money  = b_amount*price
        fen_mb(price,b_amount,round(b_money,2))
        #print "分割：",price,b_amount,b_money
        amount -=b_amount
        money-=b_money
    #print "原单2：" ,price,amount,money
    if(amount==1):
       fen_mb(price,round(amount,2),round(money,2))
def qs_day(rq):
    sum_amount=0
    sum_money =0.0
    #day_money =0.0
    #day_amount=0
    sum_person_count=0

    sum20f_person_count=0
    sum20f_amount=0
    sum20f_money=0
    for i in range(4,len(all_account)):#i 对应帐号的编号
            sum_amount += all_account[i].amount
            sum_money += all_account[i].pj_price*all_account[i].amount
            if(i<(len(all_account)-1)/20):
                sum20f_person_count+=1
                sum20f_amount+= all_account[i].amount
                sum20f_money+= all_account[i].pj_price*all_account[i].amount

            '''
            if all_account[i].day_buy_amount >0: # 当日买入平均价格
                 day_mony   += all_account[i].day_buy_amount * all_account[i].day_buy_pj_price
                 day_amount += all_account[i].day_buy_amount
            '''
            if all_account[i].amount>0:
                sum_person_count+=1
            #sum_amount,sum_money,
    print rq,"帐户持仓:","均价",round(sum_money/sum_amount,2),"持股人数：",sum_person_count,"平均持股",round(sum_amount/sum_person_count,2)#,"人数",sum20f_person_count,sum20f_amount,round(sum20f_money/sum20f_amount,2),round(sum20f_amount/sum20f_person_count,2)
    f = open("jjjs.txt","a")
    f.write(pstr(rq,"帐户持仓","均价",round(sum_money/sum_amount,2),"持股人数",sum_person_count,"平均持股",round(sum_amount/sum_person_count,2),"\n"))
    f.close()
    '''
    if int(sum_amount)-20000000.0<0 :
        print "0000",int(sum_amount)-20000000.0
        return False
    else:
        print "1111"
        return True
    '''
def dealDayBS():
    for i in range(4,len(all_account)):#i 对应帐号的编号
        all_account[i].day_buy_amount=0
        if int(float(all_account[i].amount))>=100:
            dayCanSell.append(i)
        if int(float(all_account[i].money))>=100*35:
            dayCanBuy.append(i)

def pstr(*args):
    mystr=""
    for arg in  args:
        mystr = mystr+str(arg)+","
    return mystr

def cbjs():
#   a = Account(1,1,300000,550,1000,500)
#   print a.getAmount()
#   print a.type
#   print a.money
#   print a.day_buy_amount
#   print a.day_sell_amount

   #生成20万个帐户 帐户金额随机生成 >10000
   createAllAccount()
   #print len(all_account)

   fen_Gu()#分配抽中的新股
   sum_gu()
   dm="002680"
   rq=getRq(dm)
   print rq
   for k in range(0,len(rq)-1):
       print k,rq[k]
       hb_a =0
       hb_m =0

       #if k>3 :
       #    break

       #初始化当日可以买卖的帐户
       dealDayBS()
       #加载当日成交分笔数据
       f=open(base_diretory+"\\sina\\"+rq[k]+"\\"+dm+".txt","r")
       dayfb=[]
       for line in f.readlines():
         fbdata=line[:-1].split("\t")
         #print fbdata
         dayfb.append(fbdata)
       f.close()
       test_amount=0.0
       test_money=0.0
       for b in range(len(dayfb)-1,0,-1):# 倒着按时间来
            if(k>25 and b<1500):
               continue

            #if b>len(dayfb)-15:
            #    continue
            #if b<len(dayfb)-10:
            #    break
            b_money = float(dayfb[b][4] )
            amount= float(dayfb[b][3])*100
            b_price = float(dayfb[b][1])

            b_amount = int(round(b_money/b_price,0))

            #if(b_amount!=amount):
                #print b_amount ,amount
            test_amount+=b_amount
            test_money+=b_money
            
            #print b,b_amount,float(dayfb[b][3])*100,b_money
            fen_fs(b_price,b_amount,b_money)
       #print rq[k]#,"当日成交:",test_amount,test_money,round(test_money/test_amount,2)
       qs_day(rq[k])#清算当日数据 计算帐户金额 股数 平均价格
               #计算总计持仓成本
       k+=1
   #print "当日成交",hb_a,hb_m,round(hb_m/hb_a,2)



if __name__ == "__main__":

    #for i in range(0,10):
    #    print i,"次计算"
        cbjs()