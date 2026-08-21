# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #5：4.1 `sys.intern`：字符串驻留
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# sys.intern：把运行时拼出来的字符串"收编"进驻留表，共享一份
import sys

# 运行时拼出来的字符串：默认各自独立
s1 = "".join(["设", "计", "模", "式"])
s2 = "".join(["设", "计", "模", "式"])
print("运行时拼接，s1 is s2:", s1 is s2)          # False

# intern 之后：指向同一份
i1 = sys.intern(s1)
i2 = sys.intern(s2)
print("intern 之后，i1 is i2:", i1 is i2)          # True
print("内容相等:", i1 == i2)
