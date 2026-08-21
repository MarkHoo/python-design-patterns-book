# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #5：4.1 函数 / `partial` 直接当命令
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import functools


def save_file(path: str, content: str) -> None:
    """接收者上的动作：保存文件"""
    print(f"保存文件：{path}，内容 {len(content)} 个字符")


# partial 把"函数 + 参数"打包成一个可调用对象——这就是命令！
save_report = functools.partial(save_file, "report.txt", "本月营收 100 万")
save_backup = functools.partial(save_file, "backup.db", "数据库快照")


class Button:
    """调用者：按钮只负责在点击时调用命令"""

    def __init__(self, label: str, command):
        self.label = label
        self.command = command

    def click(self) -> None:
        print(f"[点击 {self.label}]")
        self.command()


Button("保存报表", save_report).click()
Button("备份数据库", save_backup).click()
