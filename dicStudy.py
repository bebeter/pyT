
# coding=gbk


thisdict1 =	{
  "province": "�㽭",
  "city": "����",
  "street": "����ֵ�"
}

thisdict2 =	{
  "province": "�㽭2",
  "city": "����2",
  "street": "����ֵ�2",
    "����":2

}

dic  = {0:{}}#1:thisdict1,5:thisdict2
if "city" in thisdict1:
  print("�ֵ��д���'city'�����")


if 75 in dic:
  print("�ֵ��д���'2'�����iiiii")


print ("dic 1",dic[1])

print ("dic 1",dic[1]['city'])

print ("dic 2",dic[5]['city'])

print ("dic 2",dic[5]['����'])
dic[5]['����']=1

print ("dic 2",dic[5]['����'])


buy_orders={
    1000:{
"min_id":"",
"max_id":"",
"is_continue":"",

        "start_time":"",
        "end_time":"",

"min_price":"",
"max_price":"",
"price_count":0,

"max_vol":0,
"min_vol":0,
"sum_vol":0,
"avg_vol":0,

"max_sale_vol":0,
"max_buy_vol":0,

"sale_id_count":0,

        "buy_type":"",
         "":"",

    },


    2000:{

    }


}

print (buy_orders[1000])