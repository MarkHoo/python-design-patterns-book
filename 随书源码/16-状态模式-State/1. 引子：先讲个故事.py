# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有状态模式的世界——if/elif 状态机地狱
class MediaPlayer:
    def __init__(self):
        self.state = "stopped"      # stopped / playing / paused

    def play(self):
        if self.state == "stopped":
            self.state = "playing"
            print("开始播放")
        elif self.state == "playing":
            print("已经在播放了，忽略")
        elif self.state == "paused":
            self.state = "playing"
            print("从暂停恢复播放")

    def pause(self):
        if self.state == "playing":
            self.state = "paused"
            print("暂停")
        else:
            print("当前状态不能暂停")

    def stop(self):
        if self.state == "playing" or self.state == "paused":
            self.state = "stopped"
            print("停止")
        else:
            print("已经停止了")


player = MediaPlayer()
player.play()
player.pause()
player.play()
player.stop()
player.stop()
