# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #7：5.1 `re` 模块：正则表达式就是一门小语言
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 正则表达式：一门"字符匹配语言"，re 模块就是它的解释器
import re

pattern = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
m = pattern.search("会议日期：2026-05-01，请准时参加")
if m:
    print("年：", m.group("year"))
    print("月：", m.group("month"))
    print("日：", m.group("day"))

text = "客服 138-0000-1111，售后 139-0000-2222"
print("电话号码：", re.findall(r"\d{3}-\d{4}-\d{4}", text))
