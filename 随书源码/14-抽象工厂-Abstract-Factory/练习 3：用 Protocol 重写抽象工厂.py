# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》14-抽象工厂-Abstract-Factory
# 代码块 #12：练习 3：用 Protocol 重写抽象工厂
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：协议只描述行为，不要求继承
from typing import Protocol


class Widget(Protocol):
    def render(self) -> str:
        """渲染自己"""


class WidgetKit(Protocol):
    def create_button(self) -> Widget:
        """造按钮"""

    def create_dialog(self) -> Widget:
        """造弹窗"""


class RoundButton:
    def render(self) -> str:
        return "圆角按钮"


class RoundDialog:
    def render(self) -> str:
        return "圆角弹窗"


class SquareButton:
    def render(self) -> str:
        return "方形按钮"


class SquareDialog:
    def render(self) -> str:
        return "方形弹窗"


class RoundKit:
    def create_button(self) -> Widget:
        return RoundButton()

    def create_dialog(self) -> Widget:
        return RoundDialog()


class SquareKit:
    def create_button(self) -> Widget:
        return SquareButton()

    def create_dialog(self) -> Widget:
        return SquareDialog()


def demo(kit: WidgetKit) -> None:
    print(kit.create_button().render(), "|", kit.create_dialog().render())


demo(RoundKit())
demo(SquareKit())
