# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》14-抽象工厂-Abstract-Factory
# 代码块 #10：练习 1：补全一个主题工厂
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：DarkThemeFactory 与 LightThemeFactory 结构对称
class Button:
    def __init__(self, style: str):
        self.style = style

    def render(self) -> str:
        return f"{self.style}按钮"


class Dialog:
    def __init__(self, style: str):
        self.style = style

    def render(self) -> str:
        return f"{self.style}弹窗"


class ThemeFactory:
    def create_button(self) -> Button:
        raise NotImplementedError

    def create_dialog(self) -> Dialog:
        raise NotImplementedError


class LightThemeFactory(ThemeFactory):
    def create_button(self) -> Button:
        return Button("浅色")

    def create_dialog(self) -> Dialog:
        return Dialog("浅色")


class DarkThemeFactory(ThemeFactory):
    def create_button(self) -> Button:
        return Button("深色")

    def create_dialog(self) -> Dialog:
        return Dialog("深色")


for factory in (LightThemeFactory(), DarkThemeFactory()):
    print(factory.create_button().render(), "|", factory.create_dialog().render())
