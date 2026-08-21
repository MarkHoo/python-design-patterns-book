# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》19-中介者模式-Mediator
# 代码块 #4：3.3 机场塔台：多架飞机排队降落
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class ControlTower:
    """中介者：机场塔台，统一调度飞机起降"""
    def __init__(self):
        self.planes = []
        self.runway_busy = False
    def register(self, plane):
        self.planes.append(plane)
        plane.tower = self
        print(f"塔台：{plane.name} 已登记")
    def request_landing(self, plane):
        if self.runway_busy:
            print(f"塔台：{plane.name}，跑道繁忙，请在空中盘旋等待")
            return False
        self.runway_busy = True
        print(f"塔台：{plane.name}，跑道已清空，允许降落")
        return True
    def finish_landing(self, plane):
        self.runway_busy = False
        print(f"塔台：{plane.name} 已落地，跑道空闲")


class Plane:
    """同事：飞机不直接跟其他飞机通话，都找塔台"""
    def __init__(self, name):
        self.name = name
        self.tower = None
    def land(self):
        print(f"{self.name}：请求降落")
        if self.tower.request_landing(self):
            self.tower.finish_landing(self)


tower = ControlTower()
p1 = Plane("A320")
p2 = Plane("B737")
tower.register(p1)
tower.register(p2)
p1.land()
p2.land()
