# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》21-桥接模式-Bridge
# 代码块 #5：4.1 用协议（Protocol）代替抽象基类
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from typing import Protocol


class Sender(Protocol):
    """实现维度：协议（结构性子类型，无需继承）"""

    def send(self, content: str) -> None: ...


class WeChatSender:
    """微信渠道：没继承任何类，只是长得像 Sender"""
    def send(self, content: str) -> None:
        print(f"[微信] {content}")


class Notice:
    """抽象维度：通知"""

    def __init__(self, sender: Sender):
        self._sender = sender

    def push(self, content: str) -> None:
        self._sender.send(content)


Notice(WeChatSender()).push("今晚 8 点上线评审")
