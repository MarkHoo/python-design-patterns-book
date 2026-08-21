# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》21-桥接模式-Bridge
# 代码块 #6：4.2 函数即实现维度
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Alarm:
    """抽象维度：闹钟"""

    def __init__(self, notifier):
        self._notifier = notifier      # 函数注入

    def fire(self, reason: str) -> None:
        self._notifier(f"【告警】{reason}")


def email_notify(text: str) -> None:
    print(f"[邮件] {text}")


def sms_notify(text: str) -> None:
    print(f"[短信] {text}")


Alarm(email_notify).fire("CPU 温度过高")
Alarm(sms_notify).fire("磁盘空间不足")
