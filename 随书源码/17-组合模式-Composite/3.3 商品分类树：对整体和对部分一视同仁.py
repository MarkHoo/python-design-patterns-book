# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #4：3.3 商品分类树：对整体和对部分一视同仁
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Category:
    """分类节点：叶子（具体商品）和容器（分类）的统一接口"""

    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return ()

    def sales(self) -> int:
        raise NotImplementedError


class Product(Category):
    """叶子：具体商品，自带销量"""

    def __init__(self, name: str, sales: int):
        super().__init__(name)
        self._sales = sales

    def sales(self) -> int:
        return self._sales


class CategoryNode(Category):
    """容器：分类，销量 = 所有子分类/商品销量之和"""

    def __init__(self, name: str):
        super().__init__(name)
        self._children = []

    @property
    def children(self):
        return self._children

    def add(self, child: Category) -> None:
        self._children.append(child)

    def sales(self) -> int:
        return sum(child.sales() for child in self._children)


root = CategoryNode("服装")
men = CategoryNode("男装")
men.add(Product("T恤", 120))
men.add(Product("牛仔裤", 80))
women = CategoryNode("女装")
women.add(Product("连衣裙", 300))
root.add(men)
root.add(women)

print("男装销量:", men.sales())
print("女装销量:", women.sales())
print("全站服装销量:", root.sales())     # 一条调用，递归算到底
