# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #13：练习 2：把简单工厂重构为工厂方法
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：抽象工厂 + 每个类型一个工厂子类
import abc


class Logger(abc.ABC):
    @abc.abstractmethod
    def log(self, m):
        pass


class ConsoleLogger(Logger):
    def log(self, m):
        print(f"[控制台] {m}")


class FileLogger(Logger):
    def log(self, m):
        print(f"[文件] {m}")


class LoggerFactory(abc.ABC):
    @abc.abstractmethod
    def create(self) -> Logger:
        pass


class ConsoleFactory(LoggerFactory):
    def create(self) -> Logger:
        return ConsoleLogger()


class FileFactory(LoggerFactory):
    def create(self) -> Logger:
        return FileLogger()


for factory in (ConsoleFactory(), FileFactory()):
    factory.create().log("重构完成")
