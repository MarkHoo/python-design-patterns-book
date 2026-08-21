# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》11-建造者模式-Builder
# 代码块 #10：练习 1：给"优惠券"写一个建造者
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：链式建造者
class Coupon:
    def __init__(self, title, discount, expire_days, scope):
        self.title = title
        self.discount = discount
        self.expire_days = expire_days
        self.scope = scope

    def __repr__(self):
        return f"<优惠券 {self.title} 立减{self.discount}元 有效期{self.expire_days}天 适用{self.scope}>"

class CouponBuilder:
    def __init__(self):
        self.title = "通用优惠券"
        self.discount = 0
        self.expire_days = 7
        self.scope = "全店"

    def named(self, title):
        self.title = title
        return self

    def cut(self, amount):
        self.discount = amount
        return self

    def valid_for(self, days):
        self.expire_days = days
        return self

    def only_for(self, scope):
        self.scope = scope
        return self

    def build(self):
        return Coupon(self.title, self.discount, self.expire_days, self.scope)

coupon = (CouponBuilder()
          .named("新人专享")
          .cut(20)
          .valid_for(30)
          .only_for("数码类")
          .build())
print(coupon)
