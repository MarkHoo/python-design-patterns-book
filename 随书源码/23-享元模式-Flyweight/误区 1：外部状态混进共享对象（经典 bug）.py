# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #10：误区 1：外部状态混进共享对象（经典 bug）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 误区：把外部状态写进共享对象——一个粒子改颜色，全体跟着变
class ParticleType:
    def __init__(self, texture: str):
        self.texture = texture
        self.color = "白色"    # 共享的"默认颜色"

class Particle:
    def __init__(self, ptype: ParticleType, x: float, y: float):
        self.ptype = ptype
        self.x = x
        self.y = y

    def set_color(self, color: str) -> None:
        self.ptype.color = color   # 错误！改的是共享对象

explosion = ParticleType("fire.png")
p1 = Particle(explosion, 1, 1)
p2 = Particle(explosion, 2, 2)

p1.set_color("红色")               # p1 想把自己染红
print("p1 看到的颜色：", p1.ptype.color)
print("p2 看到的颜色：", p2.ptype.color, "← 被 p1 连累了！")
