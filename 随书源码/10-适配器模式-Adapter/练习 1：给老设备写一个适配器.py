# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #14：练习 1：给老设备写一个适配器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：对象适配器——组合 + 翻译
class Walkman:
    """老设备：只会放磁带"""

    def play_cassette(self):
        return "磁带转动中……"

class WalkmanAdapter:
    """适配器：把 play_cassette 翻译成 play_audio"""

    def __init__(self, walkman):
        self._walkman = walkman

    def play_audio(self, file):
        return f"{file} → {self._walkman.play_cassette()}"

def new_player(device):
    """新播放器：只认 play_audio"""
    print("新播放器：", device.play_audio("我的歌单"))

new_player(WalkmanAdapter(Walkman()))
