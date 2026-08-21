# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》11-建造者模式-Builder
# 代码块 #8：误区 1：把 Builder 写成"带默认参数的大构造函数"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面教材：这只是一个"带默认参数的大构造函数"，不是 Builder
class Config:
    def __init__(self, host="localhost", port=8080, timeout=30, debug=False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.debug = debug

# Builder 的意义在于"分步"和"命名清晰"
class ConfigBuilder:
    def __init__(self):
        self.host = "localhost"
        self.port = 8080
        self.timeout = 30
        self.debug = False

    def with_timeout(self, t):
        self.timeout = t
        return self

    def debug_on(self):
        self.debug = True
        return self

    def build(self):
        return Config(self.host, self.port, self.timeout, self.debug)

c = (ConfigBuilder().with_timeout(60).debug_on().build())
print(f"host={c.host} port={c.port} timeout={c.timeout} debug={c.debug}")
