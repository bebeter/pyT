
# coding=gbk


thisdict1 =	{
  "province": "浙江",
  "city": "杭州",
  "street": "祥符街道"
}

thisdict2 =	{
  "province": "浙江2",
  "city": "杭州2",
  "street": "祥符街道2",
    "排名":2

}

dic  = {0:{}}#1:thisdict1,5:thisdict2
if "city" in thisdict1:
  print("字典中存在'city'这个键")


if 75 in dic:
  print("字典中存在'2'这个键iiiii")


print ("dic 1",dic[1])

print ("dic 1",dic[1]['city'])

print ("dic 2",dic[5]['city'])

print ("dic 2",dic[5]['排名'])
dic[5]['排名']=1

print ("dic 2",dic[5]['排名'])


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