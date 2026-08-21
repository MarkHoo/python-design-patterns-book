# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #5：4.1 鸭子类型：被适配对象不需要继承任何接口
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class USBDevice:
    """新系统要求的接口：有 transfer 方法"""

    def transfer(self, data):
        print(f"USB 传输：{data}")

class OldPrinter:
    """老设备：只有 print_document 方法，没有 transfer"""

    def print_document(self, doc):
        print(f"打印机输出：{doc}")

class PrinterAdapter:
    """适配器：把 print_document 翻译成 transfer"""

    def __init__(self, printer):
        self._printer = printer

    def transfer(self, data):
        self._printer.print_document(data)

def connect_to_pc(device):
    """电脑只认 transfer 方法（鸭子类型，不检查类型）"""
    device.transfer("年度报告.pdf")

connect_to_pc(USBDevice())                  # 本来就兼容，直接用
connect_to_pc(PrinterAdapter(OldPrinter())) # 老设备包一层适配器
