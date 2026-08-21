# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #5：4.1 观察者就是函数：回调列表
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class WechatOfficialAccount:
    """公众号：观察者就是普通函数"""

    def __init__(self, name: str):
        self.name = name
        self._followers = []          # 列表里存的是函数

    def follow(self, callback) -> None:
        """关注：传入一个函数作为观察者"""
        self._followers.append(callback)

    def unfollow(self, callback) -> None:
        self._followers.remove(callback)

    def publish(self, article: str) -> None:
        print(f"📢 {self.name} 发布：《{article}》")
        for callback in self._followers:
            callback(self.name, article)


def fan_zhang(account, article):
    print(f"  张三收到推送：{account} 更新了《{article}》")


def fan_li(account, article):
    print(f"  李四点赞：《{article}》")


account = WechatOfficialAccount("Python 设计模式")
account.follow(fan_zhang)
account.follow(fan_li)
account.publish("观察者模式入门")
account.unfollow(fan_zhang)
account.publish("工厂方法入门")
