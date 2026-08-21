# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #4：3.3 报表生成版：同一份账本，不同口径出不同报表
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 报表访问者：账本节点不变，会计/税务两套口径各自实现
class Income:
    def __init__(self, amount: float):
        self.amount = amount

    def accept(self, visitor):
        return visitor.visit_income(self)

class Expense:
    def __init__(self, amount: float):
        self.amount = amount

    def accept(self, visitor):
        return visitor.visit_expense(self)

class Accountant:
    """会计口径：收入减支出"""

    def visit_income(self, node: Income) -> float:
        return node.amount

    def visit_expense(self, node: Expense) -> float:
        return -node.amount

class TaxOfficer:
    """税务口径：收入全额计税，支出只有一半能抵扣"""

    def visit_income(self, node: Income) -> float:
        return node.amount

    def visit_expense(self, node: Expense) -> float:
        return -node.amount * 0.5

ledger = [Income(10000.0), Expense(3000.0)]
print("会计口径利润：", round(sum(e.accept(Accountant()) for e in ledger), 2))
print("税务口径税基：", round(sum(e.accept(TaxOfficer()) for e in ledger), 2))
