# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #10：误区 2：把外观和适配器、中介者混为一谈
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 适配器：把"旧接口"翻译成"新接口"——转换
class OldSocket:
    def plug(self) -> str:
        return "老式插头"


class UsbCAdapter:
    """适配器：让老插头能插进新插座"""

    def __init__(self, old: OldSocket):
        self._old = old

    def usb_c(self) -> str:
        return f"{self._old.plug()} → 转成 USB-C"


# 外观：把"一堆子系统"简化成"一个入口"——简化
class TV:
    def on(self):
        print("电视：开机")


class SoundBar:
    def on(self):
        print("音响：开机")


class MediaFacade:
    def __init__(self):
        self._tv = TV()
        self._sound = SoundBar()

    def watch(self):
        self._tv.on()
        self._sound.on()


print(UsbCAdapter(OldSocket()).usb_c())
MediaFacade().watch()
