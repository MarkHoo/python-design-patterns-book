# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》14-抽象工厂-Abstract-Factory
# 代码块 #5：4.1 模块级函数即工厂：一个模块 = 一个产品族
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import types

# 模拟两个"模块"：每个模块 = 一个产品族，自带一组 create_* 工厂函数
light_theme = types.ModuleType("theme_light")
dark_theme = types.ModuleType("theme_dark")


def install_theme(module, style: str, bg: str, fg: str) -> None:
    """往模块里安装一对工厂函数"""

    def create_button() -> str:
        return f"{style}按钮（{bg}底{fg}字）"

    def create_dialog() -> str:
        return f"{style}弹窗（{bg}底{fg}框）"

    module.create_button = create_button
    module.create_dialog = create_dialog


install_theme(light_theme, "浅色", "白", "黑")
install_theme(dark_theme, "深色", "黑", "白")


def build_page(theme_module) -> str:
    """客户端只认两个函数：create_button 和 create_dialog"""
    return theme_module.create_button() + " | " + theme_module.create_dialog()


print("浅色模块:", build_page(light_theme))
print("深色模块:", build_page(dark_theme))
