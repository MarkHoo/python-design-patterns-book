# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #9：标准库：`logging.getLogger`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import logging

# getLogger 内部维护了一张 {名字: logger} 的表，
# 同名返回同一个对象——这就是单例思想（每个名字一个实例）
app_logger_a = logging.getLogger("my_app")
app_logger_b = logging.getLogger("my_app")
other_logger = logging.getLogger("other_app")

print("同名 logger 是同一个对象:", app_logger_a is app_logger_b)
print("不同名 logger 各自独立:", app_logger_a is other_logger)
