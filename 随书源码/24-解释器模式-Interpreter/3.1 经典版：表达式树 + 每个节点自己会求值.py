# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #2：3.1 经典版：表达式树 + 每个节点自己会求值
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 解释器经典版：表达式树 + 每个节点自己会求值
class Expr:
    """抽象表达式：所有节点的基类"""

    def evaluate(self) -> int:
        raise NotImplementedError

class Number(Expr):
    """终结符：数字"""

    def __init__(self, value: int):
        self.value = value

    def evaluate(self) -> int:
        return self.value

class Add(Expr):
    """非终结符：加法"""

    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self) -> int:
        return self.left.evaluate() + self.right.evaluate()

class Multiply(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self) -> int:
        return self.left.evaluate() * self.right.evaluate()

# 3 + 5 * 2：乘法节点挂在加法下面，优先级天然正确
expr = Add(Number(3), Multiply(Number(5), Number(2)))
print("3 + 5 * 2 =", expr.evaluate())

# (3 + 5) * 2：换括号就是换树形
expr2 = Multiply(Add(Number(3), Number(5)), Number(2))
print("(3 + 5) * 2 =", expr2.evaluate())
