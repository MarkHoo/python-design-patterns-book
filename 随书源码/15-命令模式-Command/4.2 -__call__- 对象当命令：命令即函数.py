# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #6：4.2 `__call__` 对象当命令：命令即函数
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Logger:
    """接收者：操作日志"""

    def __init__(self):
        self.entries = []

    def add(self, message: str) -> None:
        self.entries.append(message)
        print(f"记录日志：{message}")


class LogCommand:
    """__call__ 版命令：实例本身就能当函数调用"""

    def __init__(self, logger: Logger, message: str):
        self.logger = logger
        self.message = message

    def __call__(self) -> None:
        self.logger.add(self.message)


logger = Logger()
commands = [LogCommand(logger, f"第 {i} 步操作") for i in range(1, 4)]
for cmd in commands:          # 命令排队执行
    cmd()                     # 直接当函数调用

print("日志条数:", len(logger.entries))
