# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》14-抽象工厂-Abstract-Factory
# 代码块 #11：练习 2：用注册表替换 if/elif
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：注册表 + 新增一行即可
class Kit:
    def __init__(self, style: str):
        self.style = style

    def render(self) -> str:
        return f"{self.style}套装"


def make_light() -> Kit:
    return Kit("浅色")


def make_dark() -> Kit:
    return Kit("深色")


def make_blue() -> Kit:          # 新主题：新函数
    return Kit("蓝色")


FACTORIES = {
    "light": make_light,
    "dark": make_dark,
    "blue": make_blue,           # 注册一行
}


def get_factory(name: str):
    if name not in FACTORIES:
        raise KeyError(f"未知主题：{name}")
    return FACTORIES[name]


for name in ("light", "dark", "blue"):
    print(f"{name}: {get_factory(name)().render()}")
