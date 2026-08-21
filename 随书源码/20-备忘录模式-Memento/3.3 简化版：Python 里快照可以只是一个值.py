# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》20-备忘录模式-Memento
# 代码块 #4：3.3 简化版：Python 里快照可以只是一个值
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class BankAccount:
    """银行账户：余额 + 流水，快照就是一个 (余额, 流水) 元组"""

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.transactions.append(("存入", amount))

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("余额不足！")
        self.balance -= amount
        self.transactions.append(("取出", amount))

    def snapshot(self) -> tuple:
        """拍快照：余额 + 流水的深拷贝"""
        return (self.balance, copy.deepcopy(self.transactions))

    def restore(self, snap: tuple) -> None:
        """回滚：把快照内容搬回来"""
        self.balance, self.transactions = copy.deepcopy(snap)


acc = BankAccount("小明", 1000)
acc.deposit(500)
acc.withdraw(200)
print("正常操作后：余额", acc.balance)

snap = acc.snapshot()          # 拍个快照
acc.withdraw(999)              # 手滑取多了
print("手滑后：余额", acc.balance)

acc.restore(snap)              # 回滚！
print("回滚后：余额", acc.balance)
