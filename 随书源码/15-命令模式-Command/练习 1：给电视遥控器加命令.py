# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #12：练习 1：给电视遥控器加命令
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：完整的命令模式小例子——电视机音量遥控
class TV:
    """接收者：电视机"""

    def __init__(self):
        self.volume = 10

    def volume_up(self) -> None:
        self.volume += 1

    def volume_down(self) -> None:
        self.volume -= 1


class VolumeUpCommand:
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self) -> None:
        self.tv.volume_up()

    def undo(self) -> None:
        self.tv.volume_down()


class RemoteControl:
    """调用者：遥控器，记录按键历史"""

    def __init__(self):
        self._history = []

    def press(self, command) -> None:
        command.execute()
        self._history.append(command)
        print(f"按了一下，音量现在是 {command.tv.volume}")

    def press_undo(self) -> None:
        if not self._history:
            print("没有可撤销的按键")
            return
        command = self._history.pop()
        command.undo()
        print(f"撤销一次，音量现在是 {command.tv.volume}")


tv = TV()
remote = RemoteControl()
remote.press(VolumeUpCommand(tv))
remote.press(VolumeUpCommand(tv))
remote.press(VolumeUpCommand(tv))
remote.press_undo()
remote.press_undo()
