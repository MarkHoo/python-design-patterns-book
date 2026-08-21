# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #8：5.1 CPython 解释器：最大的享元用户
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# CPython 解释器自己是"享元大师"：None、字面量、小整数全都共享
print("None 全局唯一:", None is None)
print("True 全局唯一:", True is True)

a = "hello"
b = "hello"
print("字符串字面量自动共享:", a is b)

c = 256
d = 256
print("小整数自动共享:", c is d)
