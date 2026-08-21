# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #2：3.1 经典版：日志器工厂
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import abc
import os
import tempfile


class Logger(abc.ABC):
    """产品：日志器"""

    @abc.abstractmethod
    def log(self, message: str) -> None:
        pass


class ConsoleLogger(Logger):
    def log(self, message: str) -> None:
        print(f"[控制台] {message}")


class FileLogger(Logger):
    def __init__(self, path: str):
        self._path = path

    def log(self, message: str) -> None:
        with open(self._path, "a", encoding="utf-8") as f:
            f.write(message + "\n")


class LoggerFactory(abc.ABC):
    """抽象工厂：只规定"你要能造出 Logger"，不规定怎么造"""

    @abc.abstractmethod
    def create_logger(self) -> Logger:
        """工厂方法：创建逻辑下沉到子类"""
        pass


class ConsoleLoggerFactory(LoggerFactory):
    def create_logger(self) -> Logger:
        return ConsoleLogger()


class FileLoggerFactory(LoggerFactory):
    def __init__(self, path: str):
        self._path = path

    def create_logger(self) -> Logger:
        return FileLogger(self._path)


# 客户端面向抽象编程：只认 LoggerFactory，不认具体工厂
def use_factory(factory: LoggerFactory) -> None:
    logger = factory.create_logger()   # 工厂方法在此被调用
    logger.log("这是一条日志")


use_factory(ConsoleLoggerFactory())
with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
    tmp_path = f.name
try:
    use_factory(FileLoggerFactory(tmp_path))
    print("文件日志内容：", open(tmp_path, encoding="utf-8").read().strip())
finally:
    os.unlink(tmp_path)
