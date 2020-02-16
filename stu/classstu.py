# __init__() method 方法 function(函数)
# attribute 属性
# method 方法


class People:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def sayhi(self):
        print("Hi, my name is {}, and I'm {}".format(self.name, self.age))


# class instance 类的实例化

someone = People(name='Jack', age=20)  # 类的实例化
print(someone.name)  # 通过对象访问类的name成员: Jack
print(someone.age)  # 通过对象访问类的age成员: 20
someone.sayhi()  # 通过对象访问类的sayhi方法: Hi, my name is Jack, and I'm 20
_is_geo_chart: bool = False

print (_is_geo_chart)


print(abs(-9))