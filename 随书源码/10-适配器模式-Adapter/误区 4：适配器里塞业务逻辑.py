# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #13：误区 4：适配器里塞业务逻辑
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class OldSensor:
    """老传感器：输出原始读数"""

    def read_raw(self):
        return 100

# 正确姿势：适配器只做"翻译"
class VoltageAdapter:
    def __init__(self, sensor):
        self._sensor = sensor

    def read_voltage(self):
        return self._sensor.read_raw() / 10   # 只翻译单位，不管业务

adapter = VoltageAdapter(OldSensor())
print("电压：", adapter.read_voltage(), "V")
