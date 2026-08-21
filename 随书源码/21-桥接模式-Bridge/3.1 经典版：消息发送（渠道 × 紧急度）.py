# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》21-桥接模式-Bridge
# 代码块 #2：3.1 经典版：消息发送（渠道 × 紧急度）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Sender:
    """实现维度：发送渠道"""

    def send(self, content: str) -> None: ...


class SMSSender(Sender):
    def send(self, content: str) -> None:
        print(f"[短信] {content}")


class EmailSender(Sender):
    def send(self, content: str) -> None:
        print(f"[邮件] {content}")


class AppPushSender(Sender):
    def send(self, content: str) -> None:
        print(f"[App推送] {content}")


class Message:
    """抽象维度：消息（控制层），持有渠道引用"""

    def __init__(self, sender: Sender):
        self._sender = sender

    def send(self, content: str) -> None:
        self._sender.send(content)          # 把活交给渠道


class UrgentMessage(Message):
    """抽象维度的变体：加急消息"""

    def send(self, content: str) -> None:
        self._sender.send("【加急】" + content + "！！！")


# 组合：3 种渠道 × 2 种紧急度 = 6 种用法，只用了 5 个类
msgs = [
    Message(SMSSender()),
    Message(EmailSender()),
    UrgentMessage(SMSSender()),
    UrgentMessage(AppPushSender()),
]
for m in msgs:
    m.send("项目上线了")
