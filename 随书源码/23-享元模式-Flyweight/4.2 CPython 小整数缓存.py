# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #6：4.2 CPython 小整数缓存
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# CPython 小整数缓存：-5~256 常驻，谁用都是同一份
base = 100
a = base + 156      # 运行时算出 256
b = base + 156
print("运行时 256 is 256:", a is b)    # True：命中缓存

c = base + 157      # 运行时算出 257
d = base + 157
print("运行时 257 is 257:", c is d)    # False：超出缓存，各自新建

e = base - 105      # -5
f = base - 105
print("运行时 -5 is -5:", e is f)      # True：下边界之内

g = base - 106      # -6
h = base - 106
print("运行时 -6 is -6:", g is h)      # False：越界
