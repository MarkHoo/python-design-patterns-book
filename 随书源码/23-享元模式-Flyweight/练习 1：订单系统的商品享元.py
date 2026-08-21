# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #12：练习 1：订单系统的商品享元
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：商品信息共享，订单行各自只存数量
class Product:
    def __init__(self, sku: str, name: str, price: float):
        self.sku = sku
        self.name = name
        self.price = price

class OrderLine:
    def __init__(self, product: Product, qty: int):
        self.product = product
        self.qty = qty

    def total(self) -> float:
        return self.product.price * self.qty

class ProductFactory:
    def __init__(self):
        self._pool = {}

    def get(self, sku: str, name: str, price: float) -> Product:
        if sku not in self._pool:
            self._pool[sku] = Product(sku, name, price)
        return self._pool[sku]

factory = ProductFactory()
lines = []
for i in range(1000):
    lines.append(OrderLine(factory.get("A001", "机械键盘", 399), i % 3 + 1))
    lines.append(OrderLine(factory.get("B002", "鼠标垫", 29), i % 5 + 1))

print("订单行数：", len(lines))
print("商品对象数：", len(factory._pool))
print("第一条订单金额：", lines[0].total())
