# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》00-导读-设计模式入门
# 代码块 #6：③ 里氏替换原则（LSP）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Bird:
    def fly(self) -> str:
        return "飞走了"


class Sparrow(Bird):  # 麻雀：会飞，没问题
    pass


# 反面教材：企鹅不会飞，硬继承 Bird 就得改写 fly
class Penguin(Bird):
    def fly(self) -> str:
        raise NotImplementedError("企鹅不会飞！")


# 正确姿势：把"会飞"拆成独立的抽象
class Bird:
    pass


class FlyingBird(Bird):
    def fly(self) -> str:
        return "飞走了"


class Penguin(Bird):
    def swim(self) -> str:
        return "游泳冠军 🐧"


def make_it_fly(bird: FlyingBird) -> None:
    print(bird.fly())


make_it_fly(Sparrow())
