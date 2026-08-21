# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》14-抽象工厂-Abstract-Factory
# 代码块 #7：4.3 用 Protocol 代替抽象基类
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from typing import Protocol


class Widget(Protocol):
    """协议版抽象产品：只要会 render，就算组件"""

    def render(self) -> str:
        """渲染自己"""


class KitFactory(Protocol):
    """协议版抽象工厂：只要提供 create_button / create_dialog，就算工厂"""

    def create_button(self) -> Widget:
        """造一个按钮"""

    def create_dialog(self) -> Widget:
        """造一个弹窗"""


# 具体实现：不继承任何抽象类，长得像就行
class ModernButton:
    def render(self) -> str:
        return "现代风按钮（玻璃拟态）"


class ModernDialog:
    def render(self) -> str:
        return "现代风弹窗（圆角卡片）"


class RetroButton:
    def render(self) -> str:
        return "复古风按钮（像素边框）"


class RetroDialog:
    def render(self) -> str:
        return "复古风弹窗（CRT 扫描线）"


class ModernKit:
    def create_button(self) -> Widget:
        return ModernButton()

    def create_dialog(self) -> Widget:
        return ModernDialog()


class RetroKit:
    def create_button(self) -> Widget:
        return RetroButton()

    def create_dialog(self) -> Widget:
        return RetroDialog()


def build_page(kit: KitFactory) -> None:
    """客户端只认协议：谁长得像工厂，谁就能上"""
    print(kit.create_button().render())
    print(kit.create_dialog().render())


print("=== 现代风整套 ===")
build_page(ModernKit())
print("=== 复古风整套 ===")
build_page(RetroKit())
