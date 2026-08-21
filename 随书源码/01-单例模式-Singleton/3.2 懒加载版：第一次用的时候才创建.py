# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #3：3.2 懒加载版：第一次用的时候才创建
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class BigResource:
    def __init__(self):
        print("BigResource 创建了（很贵的资源，比如数据库连接）")


_resource = None

def get_resource() -> BigResource:
    """懒加载：第一次调用才真正创建"""
    global _resource
    if _resource is None:
        _resource = BigResource()
    return _resource


print("模块已导入，但资源还没有创建")
r1 = get_resource()   # 这一刻才创建
r2 = get_resource()   # 直接返回已有的
print("r1 is r2:", r1 is r2)
