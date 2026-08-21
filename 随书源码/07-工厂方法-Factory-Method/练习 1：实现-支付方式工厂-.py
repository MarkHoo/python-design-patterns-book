# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #12：练习 1：实现"支付方式工厂"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：产品族 + 一一对应的工厂子类
import abc


class Payment(abc.ABC):
    """产品：支付方式"""

    @abc.abstractmethod
    def pay(self, amount: float) -> str:
        pass


class Alipay(Payment):
    def pay(self, amount: float) -> str:
        return f"支付宝支付 {amount} 元"


class WechatPay(Payment):
    def pay(self, amount: float) -> str:
        return f"微信支付 {amount} 元"


class BankCard(Payment):
    def pay(self, amount: float) -> str:
        return f"银行卡支付 {amount} 元"


class PaymentFactory(abc.ABC):
    """抽象工厂：决定用哪种支付方式"""

    @abc.abstractmethod
    def create_payment(self) -> Payment:
        pass


class AlipayFactory(PaymentFactory):
    def create_payment(self) -> Payment:
        return Alipay()


class WechatFactory(PaymentFactory):
    def create_payment(self) -> Payment:
        return WechatPay()


class BankCardFactory(PaymentFactory):
    def create_payment(self) -> Payment:
        return BankCard()


def checkout(factory: PaymentFactory, amount: float) -> str:
    """收银台：只认抽象工厂"""
    return factory.create_payment().pay(amount)


print(checkout(AlipayFactory(), 66.6))
print(checkout(WechatFactory(), 88.8))
print(checkout(BankCardFactory(), 100.0))
