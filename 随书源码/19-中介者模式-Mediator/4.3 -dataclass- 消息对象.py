# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》19-中介者模式-Mediator
# 代码块 #6：4.3 `dataclass` 消息对象
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    """不可变消息：发出去就不能被篡改"""
    sender: str
    content: str


# 中介者投递消息：frozen 保证消息在传递途中不会被改
def deliver(room, msg):
    print(f"[{room}] {msg.sender} 说：{msg.content}")


deliver("吃货群", Message("爱丽丝", "今晚吃火锅？"))
try:
    Message("爱丽丝", "今晚吃火锅？").content = "被篡改"
except Exception as e:
    print("消息不可变，篡改失败：", e)
