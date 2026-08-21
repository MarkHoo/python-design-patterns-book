# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：简单工厂的"增长烦恼"——每加一种类型，就要改一次 create_logger
import os
import tempfile


class ConsoleLogger:
    def log(self, msg):
        print(f"[控制台] {msg}")


class FileLogger:
    def __init__(self, path):
        self._path = path

    def log(self, msg):
        with open(self._path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")


def create_logger(kind, **kwargs):
    """简单工厂：所有分支挤在一个函数里"""
    if kind == "console":
        return ConsoleLogger()
    elif kind == "file":
        return FileLogger(kwargs["path"])
    # 以后加 email 日志？加 database 日志？都得来这里改！——违反开闭原则
    raise ValueError(f"未知的日志类型：{kind}")


with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
    tmp_path = f.name

try:
    create_logger("console").log("启动系统")
    create_logger("file", path=tmp_path).log("写入文件日志")
    print("文件内容：", open(tmp_path, encoding="utf-8").read().strip())
finally:
    os.unlink(tmp_path)
