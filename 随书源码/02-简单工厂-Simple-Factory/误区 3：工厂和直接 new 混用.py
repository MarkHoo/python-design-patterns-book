# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #12：误区 3：工厂和直接 new 混用
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Logger:
    def __init__(self, level: str = "INFO"):
        self.level = level

    def log(self, msg: str):
        print(f"[{self.level}] {msg}")


def create_logger(level: str = "INFO"):
    """工厂：以后想统一给 logger 加时间戳，改这里就行"""
    return Logger(level)


logger_a = create_logger("DEBUG")   # 模块 A：老老实实走工厂
logger_b = Logger("INFO")           # 模块 B：图省事直接 new

logger_a.log("A 的日志")
logger_b.log("B 的日志")
print("两个 logger 配置是否一致：", logger_a.level == logger_b.level)
