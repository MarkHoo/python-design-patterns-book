# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #6：4.1 模块即单例（Python 社区最推崇的方式）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 把下面代码存成 settings.py，任何地方写 `from settings import settings`
# 拿到的都是同一个实例——这是 Python 里最地道的"单例"
class Settings:
    def __init__(self):
        self.debug: bool = True
        self.host: str = "127.0.0.1"

    def __repr__(self):
        return f"<Settings debug={self.debug} host={self.host}>"


# 模块顶层只执行一次，这就是那个"独一份"
settings = Settings()

# 模拟两个调用方各自 import（真实项目里就是 from settings import settings）
caller_a = settings
caller_b = settings
print("两边是同一个对象:", caller_a is caller_b)
print(caller_b)
