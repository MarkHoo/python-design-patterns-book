# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》20-备忘录模式-Memento
# 代码块 #10：练习 2：用"命令 + 备忘录"实现带撤销的加减法计算器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class Calculator:
    """发起人：计算结果本身"""

    def __init__(self):
        self.value = 0
        self._history = []       # 快照栈（管理者内嵌）

    def apply(self, op: str, n: int) -> None:
        self._history.append(copy.deepcopy(self.value))   # 操作前存档
        if op == "+":
            self.value += n
        elif op == "-":
            self.value -= n
        elif op == "*":
            self.value *= n

    def undo(self) -> bool:
        if not self._history:
            return False
        self.value = self._history.pop()
        return True


calc = Calculator()
calc.apply("+", 10)
calc.apply("*", 3)
calc.apply("-", 5)
print("当前结果：", calc.value)      # (0+10)*3-5 = 25
calc.undo()
print("撤销 1 次：", calc.value)     # 回到 -5 之前 = 30
calc.undo()
print("撤销 2 次：", calc.value)     # 回到 *3 之前 = 10
