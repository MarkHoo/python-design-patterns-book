# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》14-抽象工厂-Abstract-Factory
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有抽象工厂的世界——主题"混搭"翻车现场
class LightButton:
    def render(self) -> str:
        return "浅色按钮（白底黑字）"


class DarkButton:
    def render(self) -> str:
        return "深色按钮（黑底白字）"


class LightDialog:
    def render(self) -> str:
        return "浅色弹窗（白底黑框）"


class DarkDialog:
    def render(self) -> str:
        return "深色弹窗（黑底白框）"


def create_button(theme: str) -> object:
    """每个组件一个创建函数，各自用 if 判断主题"""
    if theme == "light":
        return LightButton()
    return DarkButton()


def create_dialog(theme: str) -> object:
    if theme == "light":
        return LightDialog()
    return DarkDialog()


# 模块 A：切了深色主题，创建深色按钮
button = create_button("dark")
# 模块 B：忘了切，还在用默认浅色弹窗
dialog = create_dialog("light")

print(button.render())
print(dialog.render())
print("？按钮深色、弹窗浅色——用户看了想报警")
