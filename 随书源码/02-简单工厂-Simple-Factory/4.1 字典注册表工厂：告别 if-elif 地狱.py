# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #5：4.1 字典注册表工厂：告别 if-elif 地狱
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class WechatPay:
    def pay(self, amount):
        return f"微信支付 {amount} 元"

class Alipay:
    def pay(self, amount):
        return f"支付宝 {amount} 元"

class UnionPay:
    def pay(self, amount):
        return f"银联支付 {amount} 元"


# 注册表：名字 → 类 的映射集中在这里
CHANNELS = {
    "wechat": WechatPay,
    "alipay": Alipay,
    "unionpay": UnionPay,
}


def create_channel(name: str):
    cls = CHANNELS.get(name)
    if cls is None:
        raise ValueError(f"未知支付渠道：{name}")
    return cls()


# 加新渠道 = 加一个类 + 注册表加一行，工厂函数体永远不用动
print(create_channel("wechat").pay(100))
print(create_channel("unionpay").pay(200))
