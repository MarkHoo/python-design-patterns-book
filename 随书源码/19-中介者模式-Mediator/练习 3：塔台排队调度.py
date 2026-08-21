# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》19-中介者模式-Mediator
# 代码块 #11：练习 3：塔台排队调度
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 练习 3 答案：塔台按请求顺序排队放行，跑道一次只服务一架
class Tower:
    def __init__(self):
        self._queue = []
        self._busy = False
    def register(self, plane):
        plane.tower = self
    def request_landing(self, plane):
        self._queue.append(plane)
        self._serve()
    def _serve(self):
        if self._busy or not self._queue:
            return
        self._busy = True
        plane = self._queue.pop(0)
        print(f"塔台：允许 {plane.name} 降落")
        print(f"{plane.name}：正在降落……")
        print(f"塔台：{plane.name} 已落地，跑道空闲")
        self._busy = False
        self._serve()   # 继续处理下一架


class Plane:
    def __init__(self, name):
        self.name = name
        self.tower = None
    def land(self):
        print(f"{self.name}：请求降落")
        self.tower.request_landing(self)


tower = Tower()
planes = [Plane(n) for n in ("A320", "B737", "C919")]
for p in planes:
    tower.register(p)

for p in planes:
    p.land()
