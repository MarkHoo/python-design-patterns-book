# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #14：练习 3：让分类树支持 `for` 和 `len`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：容器实现 __iter__/__len__，叶子返回空迭代
class Category:
    def __init__(self, name: str):
        self.name = name

    @property
    def price(self):
        return None          # 容器没有价格

    def __iter__(self):
        return iter(())      # 叶子：迭代为空

    def __len__(self):
        return 0


class Product(Category):
    def __init__(self, name: str, price: float):
        super().__init__(name)
        self._price = price

    @property
    def price(self):
        return self._price


class CategoryNode(Category):
    def __init__(self, name: str):
        super().__init__(name)
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)


digital = CategoryNode("数码")
digital.add(Product("手机", 4999))
digital.add(Product("耳机", 999))
digital.add(CategoryNode("配件"))

print("数码分类下有", len(digital), "个直接子分类/商品")
for item in digital:
    price = item.price
    suffix = f"（{price} 元）" if price is not None else "（子分类）"
    print(f" - {item.name}{suffix}")
