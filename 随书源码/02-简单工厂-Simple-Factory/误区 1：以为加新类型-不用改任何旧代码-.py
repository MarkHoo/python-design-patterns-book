# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #11：误区 1：以为加新类型"不用改任何旧代码"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class WechatPay:
    def pay(self, amount):
        return f"微信 {amount} 元"


class Alipay:
    def pay(self, amount):
        return f"支付宝 {amount} 元"


def create_channel(name):
    if name == "wechat":
        return WechatPay()
    elif name == "alipay":
        return Alipay()
    else:
        raise ValueError(f"未知渠道：{name}")


print(create_channel("wechat").pay(100))
print(create_channel("alipay").pay(50))
print("（半年后要加银联？还是得回来改 create_channel 本体）")
