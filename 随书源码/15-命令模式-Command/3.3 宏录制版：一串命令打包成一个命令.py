# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #4：3.3 宏录制版：一串命令打包成一个命令
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Light:
    """接收者：灯"""

    def __init__(self):
        self.is_on = False

    def switch(self) -> None:
        self.is_on = not self.is_on
        print(f"灯现在是{'开' if self.is_on else '关'}的")


class LightCommand:
    """具体命令：按一下开关"""

    def __init__(self, light: Light):
        self.light = light

    def execute(self) -> None:
        self.light.switch()

    def undo(self) -> None:
        self.light.switch()        # 灯的撤销 = 再按一下


class MacroCommand:
    """宏命令：把一串命令打包成一个命令"""

    def __init__(self, commands):
        self.commands = commands

    def execute(self) -> None:
        print("== 宏开始执行 ==")
        for cmd in self.commands:
            cmd.execute()

    def undo(self) -> None:
        print("== 宏整体撤销（逆序） ==")
        for cmd in reversed(self.commands):
            cmd.undo()


light = Light()
macro = MacroCommand([
    LightCommand(light),
    LightCommand(light),
    LightCommand(light),
])
macro.execute()
print("执行 3 次开关后，灯是开的:", light.is_on)
macro.undo()
print("整体撤销后，灯是关的:", light.is_on)
