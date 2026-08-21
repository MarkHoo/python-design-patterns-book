# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #2：3.1 经典对象适配器（组合）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class OldThermometer:
    """老设备：只能读出华氏温度"""

    def read_fahrenheit(self):
        return 98.6

class NewDisplay:
    """新系统：只接受摄氏度"""

    def show(self, celsius):
        print(f"当前体温：{celsius:.1f} ℃")

class FahrenheitToCelsiusAdapter:
    """对象适配器：包住老设备，对外提供新接口"""

    def __init__(self, thermometer):
        self._thermometer = thermometer      # 组合：持有被适配对象

    def read_celsius(self):
        """翻译：华氏度 → 摄氏度"""
        f = self._thermometer.read_fahrenheit()
        return (f - 32) * 5 / 9

display = NewDisplay()
adapter = FahrenheitToCelsiusAdapter(OldThermometer())
display.show(adapter.read_celsius())        # 新系统眼里，这就是个"摄氏度温度计"
