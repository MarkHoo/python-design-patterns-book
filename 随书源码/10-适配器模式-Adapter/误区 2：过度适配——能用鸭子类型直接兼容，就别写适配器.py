# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #11：误区 2：过度适配——能用鸭子类型直接兼容，就别写适配器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class ModernPrinter:
    """新打印机：本来就有 transfer 方法"""

    def transfer(self, data):
        print(f"新打印机传输：{data}")

class OldPrinter:
    """老设备：只有 print_document，没有 transfer"""

    def print_document(self, doc):
        print(f"打印机输出：{doc}")

class PrinterAdapter:
    """只有老设备这种"接口不匹配"的才需要适配器"""

    def __init__(self, printer):
        self._printer = printer

    def transfer(self, data):
        self._printer.print_document(data)

def send_to_device(device, data):
    """调用方只认 transfer（鸭子类型）"""
    device.transfer(data)

send_to_device(ModernPrinter(), "文档.pdf")                   # 零适配，直接用
send_to_device(PrinterAdapter(OldPrinter()), "文档.pdf")      # 老设备才需要包一层
