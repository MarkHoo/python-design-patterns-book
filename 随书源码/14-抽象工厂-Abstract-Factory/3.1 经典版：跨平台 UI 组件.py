# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》14-抽象工厂-Abstract-Factory
# 代码块 #2：3.1 经典版：跨平台 UI 组件
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from abc import ABC, abstractmethod


# ── 抽象产品：三类组件的统一接口 ──
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError


class TextBox(ABC):
    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError


class Dialog(ABC):
    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError


# ── 具体产品：Windows 一套 ──
class WindowsButton(Button):
    def render(self) -> str:
        return "渲染 [Windows 按钮]（圆角、蓝色高亮）"


class WindowsTextBox(TextBox):
    def render(self) -> str:
        return "渲染 [Windows 输入框]（带聚焦边框）"


class WindowsDialog(Dialog):
    def render(self) -> str:
        return "渲染 [Windows 弹窗]（带关闭按钮）"


# ── 具体产品：Linux 一套 ──
class LinuxButton(Button):
    def render(self) -> str:
        return "渲染 [Linux 按钮]（直角、极简风）"


class LinuxTextBox(TextBox):
    def render(self) -> str:
        return "渲染 [Linux 输入框]（无边框）"


class LinuxDialog(Dialog):
    def render(self) -> str:
        return "渲染 [Linux 弹窗]（带确定/取消）"


# ── 抽象工厂：定义"一族产品"的创建接口 ──
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        raise NotImplementedError

    @abstractmethod
    def create_textbox(self) -> TextBox:
        raise NotImplementedError

    @abstractmethod
    def create_dialog(self) -> Dialog:
        raise NotImplementedError


# ── 具体工厂：每个平台一套 ──
class WindowsFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_textbox(self) -> TextBox:
        return WindowsTextBox()

    def create_dialog(self) -> Dialog:
        return WindowsDialog()


class LinuxFactory(UIFactory):
    def create_button(self) -> Button:
        return LinuxButton()

    def create_textbox(self) -> TextBox:
        return LinuxTextBox()

    def create_dialog(self) -> Dialog:
        return LinuxDialog()


def build_login_page(factory: UIFactory) -> None:
    """客户端只认抽象工厂：不管底层是 Windows 还是 Linux"""
    print(factory.create_button().render())
    print(factory.create_textbox().render())
    print(factory.create_dialog().render())


print("=== 在 Windows 上构建登录页 ===")
build_login_page(WindowsFactory())
print("=== 在 Linux 上构建登录页 ===")
build_login_page(LinuxFactory())
