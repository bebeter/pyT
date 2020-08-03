import random
def random_weight(weight_data):
    total = sum(weight_data.values())    # 权重求和
    ra = random.uniform(0, total)   # 在0与权重和之前获取一个随机数
    curr_sum = 0
    ret = None
    #keys = weight_data.iterkeys()    # 使用Python2.x中的iterkeys
    keys = weight_data.keys()        # 使用Python3.x中的keys
    for k in keys:
        curr_sum += weight_data[k]             # 在遍历中，累加当前权重值
        if ra <= curr_sum:          # 当随机数<=当前权重和时，返回权重key
            ret = k
            break
    return ret
weight_data = {'a': 10, 'b': 15, 'c': 50}
count=[0,0,0]
for _ in range(10000):
   ch  = random_weight(weight_data)
   print (ch)
   if ch=='a' :
       count[0]=count[0]+1
   if ch == 'b':
       count[1] = count[1] + 1
   if ch == 'c':
       count[2] = count[2] + 1
print (count)