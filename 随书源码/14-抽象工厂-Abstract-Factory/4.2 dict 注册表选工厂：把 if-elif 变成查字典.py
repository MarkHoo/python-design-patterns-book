# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》14-抽象工厂-Abstract-Factory
# 代码块 #6：4.2 dict 注册表选工厂：把 if/elif 变成查字典
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

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


def make_light_kit():
    return Button("浅色"), Dialog("浅色")


def make_dark_kit():
    return Button("深色"), Dialog("深色")


def make_blue_kit():          # 新主题：只要新增一个函数 + 注册一行
    return Button("蓝色"), Dialog("蓝色")


KITS = {
    "light": make_light_kit,
    "dark": make_dark_kit,
    "blue": make_blue_kit,
}


def apply_theme(name: str) -> None:
    factory = KITS.get(name)
    if factory is None:
        raise KeyError(f"未知主题：{name}")
    button, dialog = factory()
    print(f"「{name}」主题：{button.render()} | {dialog.render()}")


apply_theme("light")
apply_theme("dark")
apply_theme("blue")

try:
    apply_theme("red")
except KeyError as e:
    print("未知主题被拦截:", e)
