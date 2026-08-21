# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》21-桥接模式-Bridge
# 代码块 #9：练习 1：用桥接重构"日志系统"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Sink:
    """实现维度：输出目标"""

    def write(self, line: str) -> None: ...


class ConsoleSink(Sink):
    def write(self, line: str) -> None:
        print(f"[控制台] {line}")


class FileSink(Sink):
    def write(self, line: str) -> None:
        print(f"[文件] {line}")     # 演示用：真实场景应写入文件


class Logger:
    """抽象维度：日志器（含级别过滤）"""

    def __init__(self, sink: Sink, level: str = "INFO"):
        self._sink = sink
        self._level = level

    def _allowed(self, level: str) -> bool:
        order = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
        return order[level] >= order[self._level]

    def log(self, level: str, msg: str) -> None:
        if self._allowed(level):
            self._sink.write(f"[{level}] {msg}")


console_logger = Logger(ConsoleSink(), level="INFO")
error_file_logger = Logger(FileSink(), level="ERROR")

console_logger.log("INFO", "用户登录成功")
console_logger.log("ERROR", "数据库连接失败")
error_file_logger.log("INFO", "这行不该出现")
error_file_logger.log("ERROR", "磁盘写入失败")
