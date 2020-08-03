from tqsdk import TqApi, TqAccount

api = TqApi(TqAccount("华鑫期货", "910890802", "1503p.o."), auth="论坛邮箱账户,论坛密码")
order = api.insert_order("DCE.i2009-C-520", "BUY", "OPEN", 1,110)

while True:
    api.wait_update()
    if order.status == "FINISHED" and order.volume_left == 0:
        print("权限已开通，订单已完成")
        break

api.close()