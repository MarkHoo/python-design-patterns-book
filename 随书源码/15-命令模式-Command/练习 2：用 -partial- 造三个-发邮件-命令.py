# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #13：练习 2：用 `partial` 造三个"发邮件"命令
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：partial 打包"函数 + 参数"，三个按钮共享一个发送函数
import functools


def send_email(to: str, subject: str) -> None:
    print(f"发送邮件 → {to}，主题：{subject}")


send_to_boss = functools.partial(send_email, "boss@company.com", "季度总结")
send_to_team = functools.partial(send_email, "team@company.com", "周报")
send_to_customer = functools.partial(send_email, "customer@example.com", "发票")


class Button:
    def __init__(self, label: str, command):
        self.label = label
        self.command = command

    def click(self) -> None:
        print(f"[点击 {self.label}]")
        self.command()


Button("发给老板", send_to_boss).click()
Button("发给团队", send_to_team).click()
Button("发给客户", send_to_customer).click()
