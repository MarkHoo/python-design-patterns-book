# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》21-桥接模式-Bridge
# 代码块 #11：练习 3：函数即实现维度
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Message:
    """抽象维度：消息（渠道改为函数注入）"""

    def __init__(self, send_func):
        self._send = send_func

    def send(self, content: str) -> None:
        self._send(content)


def sms(content: str) -> None:
    print(f"[短信] {content}")


def dingtalk(content: str) -> None:
    print(f"[钉钉] {content}")


Message(sms).send("开会了")
Message(dingtalk).send("代码评审 2 点开始")
