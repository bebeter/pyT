# -*- coding:utf-8 -*-
import requests
import json


host = "http://172.16.228.114"
url =host+'/api/v3/biz/with_reduced?sort=bk_biz_name'
url = 'http://cmdb.bk.fsg.inner/api/v3/object/classification/0/objects'
headers ={"BK_USER":"sunxiaoning","HTTP_BLUEKING_SUPPLIER_ID": "0"}



params1 = {'bk_app_code':'bk_cmdb','bk_app_secret':'e4e5482a-2037-4a89-bc21-cf8ffd04883b',"bk_username":"admin","bk_biz_id":2,"job_instance_id":28659}







params ={
    "bk_app_code": "bk_cmdb",
    "bk_app_secret": "xxxxxxx",
    "bk_username":"admin","bk_biz_id":2,
    "bk_token": "",
    "BK_USER":"admin",
    "HTTP_BLUEKING_SUPPLIER_ID": 0,
    "cc3": "MTU3OTA2MTkzM3xOd3dBTkZwTFdFZENTa00zU2xaQlZGTkVOMGswVUZJMFZWbEZOekpPVXpVMlNsTXpXVWhSTlUxRlJFb3lSRFZCV1U5VFFqUkVURUU9fC0lpyw0AsnBynithBEMWHPS3XJL"
}

resp =requests.get(url,params=params,headers=headers)
print (resp.content.decode('utf-8'))





url =host+'/api/v3/biz/simplify？sort=bk_biz_name'
params ={
    "bk_supplier_account": "123456789",
    "data": {
        "bk_biz_name": "cc_app_test",
        "bk_biz_maintainer": "admin",
        "bk_biz_productor": "admin",
        "bk_biz_developer": "admin",
        "bk_biz_tester": "admin",
        "time_zone": "Asia/Shanghai"
    }
}

resp =requests.post(url,data=params,headers=headers)
print (resp.content.decode('utf-8'))





url =host+'/api/v3/biz/create_business'
params ={
        "bk_supplier_account": "123456789",

        "life_cycle": "2",
        "language": "1",
        "bk_biz_maintainer": "admin",
        "bk_biz_name": "这个参数",
        "time_zone": "Africa/Accra",
    }


json = {
		"bk_biz_name": "测试 录入",
		"bk_biz_maintainer": "admin",
		"bk_biz_productor": "admin",
		"bk_biz_developer": "admin",
		"bk_biz_tester": "admin",
        "time_zone": "Africa/Accra",
        "language": "1",
    }




resp =requests.post(url,json=params, headers=headers)
print (resp.content.decode('utf-8'))





'''
result = json.loads(resp.content)
data =result["data"][0]["step_results"][0]["ip_logs"][0]["log_content"]
print (data)
'''















#发送get请求并得到结果
# url = 'http://api.nnzhp.cn/api/user/stu_info?stu_name=小黑马 '#请求接口
# req = requests.get(url)#发送请求
# print(req.text)#获取请求，得到的是json格式
# print(req.json())#获取请求，得到的是字典格式
# print(type(req.text))
# print(type(req.json()))

#发送post请求,注册接口
# url = 'http://api.nnzhp.cn/api/user/user_reg'
# data = {'username':'mpp0130','pwd':'Mp123456','cpwd':'Mp123456'}
# req = requests.post(url,data)#发送post请求，第一个参数是URL，第二个参数是请求数据
# print(req.json())

#入参是json
# url = 'http://api.nnzhp.cn/api/user/add_stu'
# data = {'name':'mapeipei','grade':'Mp123456','phone':15601301234}
# req = requests.post(url,json=data)
# print(req.json())

#添加header
# url = 'http://api.nnzhp.cn/api/user/all_stu'
# header = {'Referer':'http://api.nnzhp.cn/'}
# res = requests.get(url,headers=header)
# print(res.json())