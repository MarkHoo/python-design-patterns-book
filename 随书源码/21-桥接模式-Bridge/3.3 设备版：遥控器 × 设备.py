# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》21-桥接模式-Bridge
# 代码块 #4：3.3 设备版：遥控器 × 设备
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Device:
    """实现维度：可遥控的设备"""

    def power_on(self) -> None: ...
    def power_off(self) -> None: ...
    def set_volume(self, level: int) -> None: ...


class TV(Device):
    def __init__(self):
        self._on = False
        self._volume = 10

    def power_on(self) -> None:
        self._on = True
        print("电视：开机")

    def power_off(self) -> None:
        self._on = False
        print("电视：关机")

    def set_volume(self, level: int) -> None:
        self._volume = max(0, min(100, level))
        print(f"电视：音量调到 {self._volume}")


class Radio(Device):
    def __init__(self):
        self._on = False
        self._volume = 20

    def power_on(self) -> None:
        self._on = True
        print("收音机：开机")

    def power_off(self) -> None:
        self._on = False
        print("收音机：关机")

    def set_volume(self, level: int) -> None:
        self._volume = max(0, min(100, level))
        print(f"收音机：音量调到 {self._volume}")


class RemoteControl:
    """抽象维度：遥控器"""

    def __init__(self, device: Device):
        self._device = device

    def toggle_power(self) -> None:
        print("按下电源键：", end="")
        self._device.power_on()      # 简化：演示只开机

    def volume_up(self) -> None:
        self._device.set_volume(self._current_volume() + 5)

    def _current_volume(self) -> int:
        # 演示用：假设当前音量是 10
        return 10


class AdvancedRemote(RemoteControl):
    """抽象维度变体：高级遥控器（带静音）"""

    def mute(self) -> None:
        print("按下静音键：", end="")
        self._device.set_volume(0)


tv_remote = RemoteControl(TV())
tv_remote.toggle_power()
tv_remote.volume_up()

radio_remote = AdvancedRemote(Radio())
radio_remote.toggle_power()
radio_remote.mute()
