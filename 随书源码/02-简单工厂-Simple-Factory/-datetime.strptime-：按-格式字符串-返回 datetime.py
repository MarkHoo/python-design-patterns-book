# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #8：`datetime.strptime`：按"格式字符串"返回 datetime
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from datetime import datetime

d1 = datetime.strptime("2024-01-15 10:30:00", "%Y-%m-%d %H:%M:%S")
d2 = datetime.strptime("15/01/2024", "%d/%m/%Y")
print("第一种格式解析：", d1)
print("第二种格式解析：", d2)
