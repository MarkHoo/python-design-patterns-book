# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #3：3.2 类适配器（继承）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class OldThermometer:
    """老设备：只能读出华氏温度"""

    def read_fahrenheit(self):
        return 98.6

class CelsiusThermometer(OldThermometer):
    """类适配器：继承老设备，补上新接口"""

    def read_celsius(self):
        return (self.read_fahrenheit() - 32) * 5 / 9

t = CelsiusThermometer()
print(f"摄氏度读数：{t.read_celsius():.1f} ℃")
print(f"老接口还在：{t.read_fahrenheit()} ℉")
