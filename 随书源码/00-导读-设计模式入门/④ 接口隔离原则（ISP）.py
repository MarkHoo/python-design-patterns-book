# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》00-导读-设计模式入门
# 代码块 #7：④ 接口隔离原则（ISP）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面教材：一个"全能打印机"接口，普通打印机被迫实现传真
class MultiFunctionPrinter:
    def print(self) -> None: ...
    def fax(self) -> None: ...
    def scan(self) -> None: ...


class BasicPrinter(MultiFunctionPrinter):
    def print(self) -> None:
        print("打印中...")

    def fax(self) -> None:
        raise NotImplementedError("我没有传真功能！")

    def scan(self) -> None:
        raise NotImplementedError("我没有扫描功能！")


# 正确姿势：接口拆开
class Printer:
    def print(self) -> None: ...


class Scanner:
    def scan(self) -> None: ...


class BasicPrinter(Printer):
    def print(self) -> None:
        print("打印中...")


basic = BasicPrinter()
basic.print()
