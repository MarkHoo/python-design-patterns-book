# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #4：3.3 函数式适配器：适配"签名"不匹配
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 老代码：返回 (数值, 单位) 元组
def read_temperature():
    return 98.6, "F"

# 新代码：只收一个纯数值
def show_celsius(value):
    print(f"当前体温：{value:.1f} ℃")

# 函数式适配：包一层，把元组"翻译"成纯数值
def adapt_read():
    value, unit = read_temperature()
    if unit == "F":
        value = (value - 32) * 5 / 9
    return value

show_celsius(adapt_read())
