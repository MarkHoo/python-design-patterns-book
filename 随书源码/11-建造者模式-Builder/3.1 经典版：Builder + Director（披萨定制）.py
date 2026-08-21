# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》11-建造者模式-Builder
# 代码块 #2：3.1 经典版：Builder + Director（披萨定制）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Pizza:
    """产品：披萨"""

    def __init__(self):
        self.size = None
        self.toppings = []
        self.cheese = None
        self.sauce = None

    def __repr__(self):
        return f"<披萨 {self.size}寸 配料={'、'.join(self.toppings)} 奶酪={self.cheese} 酱料={self.sauce}>"

class PizzaBuilder:
    """建造者：分步提供配置项（经典版，方法不返回 self）"""

    def __init__(self):
        self._pizza = Pizza()

    def set_size(self, size):
        self._pizza.size = size

    def add_topping(self, topping):
        self._pizza.toppings.append(topping)

    def set_cheese(self, cheese):
        self._pizza.cheese = cheese

    def set_sauce(self, sauce):
        self._pizza.sauce = sauce

    def build(self):
        """最后一步：交货"""
        pizza = self._pizza
        self._pizza = Pizza()      # 构建完重置，防止下次复用脏数据
        return pizza

class PizzaDirector:
    """导演：封装常见"配方"，控制构建顺序"""

    def __init__(self, builder):
        self._builder = builder

    def make_meat_lover(self):
        b = self._builder
        b.set_size(12)
        b.add_topping("培根")
        b.add_topping("香肠")
        b.set_cheese("马苏里拉")
        b.set_sauce("番茄酱")
        return b.build()

    def make_veggie(self):
        b = self._builder
        b.set_size(10)
        b.add_topping("蘑菇")
        b.add_topping("青椒")
        b.set_cheese("素食奶酪")
        b.set_sauce("蒜香酱")
        return b.build()

director = PizzaDirector(PizzaBuilder())
print(director.make_meat_lover())
print(director.make_veggie())
