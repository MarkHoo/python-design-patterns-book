# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》14-抽象工厂-Abstract-Factory
# 代码块 #4：3.3 主题切换版：换工厂 = 换全家
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Button:
    def render(self) -> str:
        return "通用按钮"


class LightButton(Button):
    def render(self) -> str:
        return "浅色按钮（白底黑字）"


class DarkButton(Button):
    def render(self) -> str:
        return "深色按钮（黑底白字）"


class Dialog:
    def render(self) -> str:
        return "通用弹窗"


class LightDialog(Dialog):
    def render(self) -> str:
        return "浅色弹窗（白底黑框）"


class DarkDialog(Dialog):
    def render(self) -> str:
        return "深色弹窗（黑底白框）"


class ThemeFactory:
    """抽象工厂：这里故意不用 ABC，靠子类重写 + 鸭子类型"""

    def create_button(self) -> Button:
        raise NotImplementedError

    def create_dialog(self) -> Dialog:
        raise NotImplementedError


class LightThemeFactory(ThemeFactory):
    def create_button(self) -> Button:
        return LightButton()

    def create_dialog(self) -> Dialog:
        return LightDialog()


class DarkThemeFactory(ThemeFactory):
    def create_button(self) -> Button:
        return DarkButton()

    def create_dialog(self) -> Dialog:
        return DarkDialog()


def get_theme_factory(name: str) -> ThemeFactory:
    """根据用户偏好返回对应工厂——运行时决定用哪一套"""
    if name == "light":
        return LightThemeFactory()
    if name == "dark":
        return DarkThemeFactory()
    raise ValueError(f"未知主题：{name}")


def apply_theme(name: str) -> None:
    factory = get_theme_factory(name)
    print(f"--- 用户切换到「{name}」主题 ---")
    print(" ", factory.create_button().render())
    print(" ", factory.create_dialog().render())


apply_theme("light")
apply_theme("dark")
