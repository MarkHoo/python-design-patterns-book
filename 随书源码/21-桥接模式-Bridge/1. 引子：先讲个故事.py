# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》21-桥接模式-Bridge
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：继承爆炸——消息发送 × 紧急程度，两两组合出 6 个类！
class Message:
    def send(self) -> None: ...


class NormalSMS(Message):
    def send(self) -> None:
        print("发送普通短信")


class UrgentSMS(Message):
    def send(self) -> None:
        print("发送加急短信：!!!")


class NormalEmail(Message):
    def send(self) -> None:
        print("发送普通邮件")


class UrgentEmail(Message):
    def send(self) -> None:
        print("发送加急邮件：!!!")


class NormalAppPush(Message):
    def send(self) -> None:
        print("发送普通 App 推送")


class UrgentAppPush(Message):
    def send(self) -> None:
        print("发送加急 App 推送：!!!")


for cls in (NormalSMS, UrgentSMS, NormalEmail, UrgentEmail, NormalAppPush, UrgentAppPush):
    cls().send()
