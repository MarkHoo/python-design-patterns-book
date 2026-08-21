# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有工厂的世界——每个业务模块都自己写一遍"怎么创建支付渠道"
class WechatPay:
    def pay(self, amount):
        return f"微信支付 {amount} 元"


class Alipay:
    def pay(self, amount):
        return f"支付宝支付 {amount} 元"


# 模块 A：下单模块里的创建逻辑
def create_channel_a(name: str):
    if name == "wechat":
        return WechatPay()
    elif name == "alipay":
        return Alipay()
    else:
        raise ValueError(f"不支持的支付渠道：{name}")


# 模块 B：退款模块又抄了一遍
def create_channel_b(name: str):
    if name == "wechat":
        return WechatPay()
    elif name == "alipay":
        return Alipay()
    else:
        raise ValueError(f"不支持的支付渠道：{name}")


print(create_channel_a("wechat").pay(100))
print(create_channel_b("alipay").pay(50))
