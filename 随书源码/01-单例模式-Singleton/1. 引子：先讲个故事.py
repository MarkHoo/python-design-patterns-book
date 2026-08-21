# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有单例的世界——配置文件各改各的
class ConfigManager:
    def __init__(self):
        self._config = {"theme": "light"}

    def set(self, key, value):
        self._config[key] = value

    def get(self, key):
        return self._config.get(key)


# 模块 A：想换主题
config_a = ConfigManager()
config_a.set("theme", "dark")

# 模块 B：完全不知情，拿到的还是旧配置
config_b = ConfigManager()
print("模块 B 看到的主题：", config_b.get("theme"))  # 还是 light，A 白改了
