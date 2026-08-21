# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #6：4.2 `__getattr__` 自动转发：万能适配器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class LegacyAPI:
    """老接口：一堆方法，名字各不相同"""

    def get_user_name(self):
        return "小明"

    def get_user_age(self):
        return 18

class AutoForwardAdapter:
    """万能适配器：自己不认识的调用，全部转发给被适配对象"""

    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        # 只在属性查找失败时触发：把请求转发给被适配对象
        return getattr(self._target, name)

adapter = AutoForwardAdapter(LegacyAPI())
print(adapter.get_user_name())   # 适配器自己没这个方法 → 自动转发
print(adapter.get_user_age())
