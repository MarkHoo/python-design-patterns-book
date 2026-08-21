# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #8：误区 1：把代理和装饰器混为一谈
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 装饰器：给对象"加功能"（不拦访问）
def shoutify(cls):
    """装饰器：把 hello 的结果喊出来"""
    original = cls.hello

    def hello(self):
        return original(self).upper() + "！"

    cls.hello = hello
    return cls

@shoutify
class Greeter:
    def hello(self):
        return "你好"

print(Greeter().hello())     # 功能被增强了：你好 → 你好！

# 代理：控制"能不能访问"（不改变功能）
class Secret:
    def hello(self):
        return "秘密内容"

class GuardProxy:
    """保护代理：权限不够就拦截"""

    def __init__(self, target, allowed):
        self._target = target
        self._allowed = allowed

    def hello(self):
        if not self._allowed:
            return "无权访问"
        return self._target.hello()

print(GuardProxy(Secret(), allowed=False).hello())
print(GuardProxy(Secret(), allowed=True).hello())
