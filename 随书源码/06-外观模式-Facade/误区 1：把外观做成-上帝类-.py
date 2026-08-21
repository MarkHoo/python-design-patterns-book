# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #9：误区 1：把外观做成"上帝类"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面教材：上帝外观——什么都往里塞
class GodFacade:
    """下单、退款、发票、密码、短信……全包了"""

    def place_order(self):
        print("下单")

    def refund(self):
        print("退款")

    def invoice(self):
        print("开发票")

    def reset_password(self):
        print("重置密码")   # ← 这跟下单系统有什么关系？

    def send_sms(self):
        print("发短信")     # ← 又一个八竿子打不着的

    def calculate_shipping(self):
        print("算运费")

    # ……还在继续膨胀


facade = GodFacade()
facade.place_order()
facade.reset_password()   # 外观变成了杂物间
