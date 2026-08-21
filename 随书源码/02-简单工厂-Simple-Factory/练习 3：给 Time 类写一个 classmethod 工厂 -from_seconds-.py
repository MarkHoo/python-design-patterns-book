# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #15：练习 3：给 Time 类写一个 classmethod 工厂 `from_seconds`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Time:
    def __init__(self, hour: int, minute: int, second: int):
        self.hour, self.minute, self.second = hour, minute, second

    @classmethod
    def from_seconds(cls, total: int):
        """工厂：把总秒数换算成 时:分:秒 再构造"""
        hour, rem = divmod(total, 3600)
        minute, second = divmod(rem, 60)
        return cls(hour, minute, second)

    def __repr__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"


t = Time.from_seconds(3725)
print(t)
