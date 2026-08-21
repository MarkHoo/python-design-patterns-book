# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #2：3.1 经典版：用 `__new__` 拦截创建
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class ConfigManager:
    """经典单例：用 __new__ 控制实例创建"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:                    # 还没有实例？
            cls._instance = super().__new__(cls)     # 创建唯一的一个
            cls._instance._init_config()             # 只在首次创建时初始化
        return cls._instance

    def _init_config(self) -> None:
        self._config = {"theme": "light", "lang": "zh"}

    def get(self, key: str):
        return self._config.get(key)

    def set(self, key: str, value) -> None:
        self._config[key] = value


a = ConfigManager()
b = ConfigManager()
print("a is b（同一个实例吗）:", a is b)

a.set("theme", "dark")
print("b 能看到 a 的修改:", b.get("theme"))
