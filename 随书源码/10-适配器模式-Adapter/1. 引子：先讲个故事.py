# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：老设备只输出华氏度，新系统只认摄氏度——直接怼上就出洋相
class OldThermometer:
    """服役十年的老温度计：只会报华氏度"""

    def read_fahrenheit(self):
        return 98.6

class NewDisplay:
    """新买的智能大屏：只接受摄氏度"""

    def show(self, celsius):
        print(f"当前体温：{celsius:.1f} ℃")

old = OldThermometer()
display = NewDisplay()
# 直接把华氏度塞给摄氏度显示器——98.6 ℉ 被当成 98.6 ℃，离谱
display.show(old.read_fahrenheit())
