# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #2：3.1 经典版：一个函数 + if-elif（支付渠道工厂）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class WechatPay:
    def pay(self, amount: float) -> str:
        return f"【微信支付】{amount} 元"


class Alipay:
    def pay(self, amount: float) -> str:
        return f"【支付宝】{amount} 元"


class UnionPay:
    def pay(self, amount: float) -> str:
        return f"【银联支付】{amount} 元"


def create_channel(name: str):
    """简单工厂：报一个名字，返回对应的支付渠道"""
    if name == "wechat":
        return WechatPay()
    elif name == "alipay":
        return Alipay()
    elif name == "unionpay":
        return UnionPay()
    else:
        raise ValueError(f"未知支付渠道：{name}")


for name in ["wechat", "alipay", "unionpay"]:
    channel = create_channel(name)
    print(channel.pay(99.9))
