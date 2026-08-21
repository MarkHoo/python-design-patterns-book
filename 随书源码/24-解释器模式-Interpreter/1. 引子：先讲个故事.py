# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有解释器的世界——表达式用字符串硬凑
def calc_v1(expr: str) -> int:
    """最朴素的加法器：只认 '数字+数字' 一种格式"""
    left, right = expr.split("+")
    return int(left) + int(right)

print("3+5 =", calc_v1("3+5"))          # 还行

# 表达式稍微复杂一点，各种翻车
try:
    print("3+5+2 =", calc_v1("3+5+2"))  # 三个数？两个变量装不下
except Exception as e:
    print("3+5+2 翻车了：", type(e).__name__, "——", e)

try:
    print("10-3 =", calc_v1("10-3"))    # 减法？想都别想
except Exception as e:
    print("10-3 翻车了：", type(e).__name__, "——", e)
