# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #4：3.3 通用享元池：一个 dict 搞定
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 通用享元池：把任意"构造逻辑"变成享元工厂
class FlyweightFactory:
    """按参数键去重：同一个键只创建一次"""

    def __init__(self, builder):
        self._builder = builder
        self._pool = {}

    def get(self, *args):
        if args not in self._pool:
            self._pool[args] = self._builder(*args)
            print(f"新建并缓存：{args}")
        return self._pool[args]

def make_user(name: str, dept: str):
    """真实的"昂贵"对象构造（这里用 dict 模拟）"""
    return {"name": name, "dept": dept}

users = FlyweightFactory(make_user)
u1 = users.get("小明", "研发部")
u2 = users.get("小明", "研发部")
u3 = users.get("小红", "研发部")
print("同名同部门是同一个对象:", u1 is u2)
print("不同名字各自独立:", u1 is not u3)
print("池子大小:", len(users._pool))
