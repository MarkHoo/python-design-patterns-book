# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #9：误区 1：命令对象里塞了太多业务逻辑
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class BankAccount:
    """接收者：业务逻辑应该住在这里"""

    def __init__(self, balance: float):
        self.balance = balance

    def withdraw(self, amount: float) -> None:
        if self.balance < amount:
            raise ValueError(f"余额不足（余额 {self.balance}）")
        self.balance -= amount
        print(f"扣款 {amount}，余额 {self.balance}")


# 反面教材：命令复制了一份业务逻辑，以后改规则要改两处
class BadPayCommand:
    def __init__(self, account: BankAccount, amount: float):
        self.account = account
        self.amount = amount

    def execute(self) -> None:
        if self.account.balance < self.amount:      # ← 业务逻辑复制粘贴
            raise ValueError("余额不足")
        self.account.balance -= self.amount
        print(f"扣款 {self.amount}，余额 {self.account.balance}")


# 正确姿势：命令只做"转发"
class GoodPayCommand:
    def __init__(self, account: BankAccount, amount: float):
        self.account = account
        self.amount = amount

    def execute(self) -> None:
        self.account.withdraw(self.amount)          # ← 只转发，不实现


account = BankAccount(100)
BadPayCommand(account, 30).execute()
GoodPayCommand(account, 20).execute()
