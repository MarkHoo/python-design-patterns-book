# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #3：3.2 粒子系统：海量粒子共享贴图
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 粒子系统：贴图/颜色是内部状态（共享），位置/速度是外部状态（每个粒子独有）
class ParticleType:
    """享元：一种粒子的贴图与颜色"""

    def __init__(self, name: str, texture: str, color: str):
        self.name = name
        self.texture = texture
        self.color = color

    def __repr__(self):
        return f"<粒子类型 {self.name} {self.color}>"

class Particle:
    """普通粒子：持有类型引用 + 自己的运动状态"""

    def __init__(self, ptype: ParticleType, x: float, y: float, vx: float, vy: float):
        self.ptype = ptype
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self) -> None:
        self.x += self.vx
        self.y += self.vy

    def draw(self) -> str:
        return f"在({self.x:.0f},{self.y:.0f}) 画 {self.ptype}"

class ParticleFactory:
    def __init__(self):
        self._types = {}

    def get_type(self, name: str, texture: str, color: str) -> ParticleType:
        key = (name, texture, color)
        if key not in self._types:
            self._types[key] = ParticleType(name, texture, color)
        return self._types[key]

factory = ParticleFactory()
explosion = factory.get_type("爆炸", "fire.png", "橙红")
spark = factory.get_type("火花", "spark.png", "金黄")

particles = [Particle(explosion, i, 0, 0.1, -1) for i in range(1000)]
particles += [Particle(spark, i, 100, 0.2, 2) for i in range(500)]

print(f"1500 个粒子，但贴图对象只有 {len(factory._types)} 种")
p = particles[0]
print(p.draw())
p.move()
print("移动后：", p.draw())
