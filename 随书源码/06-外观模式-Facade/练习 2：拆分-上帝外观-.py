# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #12：练习 2：拆分"上帝外观"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：按业务域拆分——每个外观只干一件事
class OrderFacade:
    """订单域外观：只做下单相关"""
    def place_order(self):
        print("下单")
    def refund(self):
        print("退款")


class BillingFacade:
    """财务域外观：只做发票相关"""
    def invoice(self):
        print("开发票")


class AccountFacade:
    """账号域外观：只做账号相关"""
    def reset_password(self):
        print("重置密码")


OrderFacade().place_order()
BillingFacade().invoice()
AccountFacade().reset_password()
