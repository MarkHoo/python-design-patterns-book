# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #12：`@dataclass`：一行生成 `__init__`/`__repr__`/`__eq__`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    stock: int = 0


p1 = Product("键盘", 199.0, 50)
p2 = Product("键盘", 199.0, 50)
print("自动生成的 __init__ 和 __repr__：", p1)
print("自动生成的 __eq__：", p1 == p2)
