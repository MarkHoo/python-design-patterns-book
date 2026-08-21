# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #3：3.2 保护代理：该拦的拦（权限检查）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class BankAccount:
    """真实对象：银行账户"""

    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance

    def withdraw(self, amount):
        if amount > self._balance:
            print(f"余额不足：只有 {self._balance} 元")
            return
        self._balance -= amount
        print(f"取款 {amount} 元成功，剩余 {self._balance} 元")

class AccountProxy:
    """保护代理：先检查权限，再放行"""

    def __init__(self, account, user):
        self._account = account
        self._user = user

    def withdraw(self, amount):
        if self._user != self._account.owner:
            print(f"拒绝：{self._user} 不是账户主人，无权取款")
            return
        self._account.withdraw(amount)

account = BankAccount("小明", 1000)
proxy = AccountProxy(account, "小红")
proxy.withdraw(500)          # 小红想取钱 → 被拦
proxy2 = AccountProxy(account, "小明")
proxy2.withdraw(500)         # 本人取钱 → 放行
