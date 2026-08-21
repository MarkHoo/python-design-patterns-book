# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #14：练习 3：给森林游戏划分内外状态
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：把共享的"树种"抽成享元，坐标留给每棵树自己
class TreeType:
    """享元：树种（贴图、颜色）"""

    def __init__(self, name: str, texture: str, color: str):
        self.name = name
        self.texture = texture
        self.color = color

class Tree:
    """外部状态：每棵树自己的位置"""

    def __init__(self, tree_type: TreeType, x: float, y: float):
        self.tree_type = tree_type
        self.x = x
        self.y = y

    def draw(self) -> str:
        return f"{self.tree_type.name} 种在 ({self.x}, {self.y})"

class TreeFactory:
    def __init__(self):
        self._pool = {}

    def get(self, name: str, texture: str, color: str) -> TreeType:
        if name not in self._pool:
            self._pool[name] = TreeType(name, texture, color)
        return self._pool[name]

factory = TreeFactory()
forest = [Tree(factory.get("橡树", "oak.png", "绿"), i, i % 10) for i in range(500)]
forest += [Tree(factory.get("枫树", "maple.png", "红"), i, i % 7) for i in range(500)]
print("1000 棵树，树种对象只有", len(factory._pool), "种")
print(forest[0].draw())
