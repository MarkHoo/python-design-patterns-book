# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #11：练习 1：用模板方法实现"支付流程"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：骨架在基类，差异在子类
import abc


class PayFlow(abc.ABC):
    """模板方法：支付流程骨架"""

    def pay(self, amount: float) -> str:
        self.choose_channel()
        result = self.deduct(amount)
        self.notify(result)
        return result

    @abc.abstractmethod
    def choose_channel(self) -> None:
        pass

    @abc.abstractmethod
    def deduct(self, amount: float) -> str:
        pass

    def notify(self, result: str) -> None:
        print(f"通知：支付{result}")


class AlipayFlow(PayFlow):
    def choose_channel(self):
        print("渠道：支付宝")

    def deduct(self, amount):
        print(f"支付宝扣款 {amount} 元")
        return "成功"


class WechatFlow(PayFlow):
    def choose_channel(self):
        print("渠道：微信支付")

    def deduct(self, amount):
        print(f"微信扣款 {amount} 元")
        return "成功"


AlipayFlow().pay(66.6)
WechatFlow().pay(88.8)
