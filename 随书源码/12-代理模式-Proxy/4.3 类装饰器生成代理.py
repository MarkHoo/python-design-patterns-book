# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #7：4.3 类装饰器生成代理
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def logging_proxy(cls):
    """类装饰器：把类的所有方法包上一层日志，返回一个代理类"""
    class Proxy:
        def __init__(self, *args, **kwargs):
            self._real = cls(*args, **kwargs)

        def __getattr__(self, name):
            attr = getattr(self._real, name)
            if callable(attr):
                def wrapper(*a, **kw):
                    print(f"[日志] 调用 {name}({a}{kw})")
                    return attr(*a, **kw)
                return wrapper
            return attr
    return Proxy

@logging_proxy
class Calculator:
    def add(self, x, y):
        return x + y

calc = Calculator()
print("add 结果：", calc.add(3, 4))
