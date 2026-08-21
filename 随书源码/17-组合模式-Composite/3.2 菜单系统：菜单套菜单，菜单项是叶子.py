# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #3：3.2 菜单系统：菜单套菜单，菜单项是叶子
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class MenuItem:
    """叶子：可点击的菜单项"""

    def __init__(self, name: str, action: str):
        self.name = name
        self.action = action

    @property
    def children(self):
        return ()          # 叶子没有子项

    def render(self) -> list:
        return [f"- {self.name}（{self.action}）"]

    def click(self) -> str:
        return f"执行菜单项「{self.name}」：{self.action}"


class Menu:
    """容器：菜单可以包含菜单项，也可以包含子菜单"""

    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, item) -> None:
        self.children.append(item)

    def render(self) -> list:
        lines = [f"▸ {self.name}"]
        for child in self.children:
            lines.extend("  " + line for line in child.render())   # 递归
        return lines

    def click(self) -> str:
        return f"展开菜单「{self.name}」（{len(self.children)} 项）"


file_menu = Menu("文件")
file_menu.add(MenuItem("新建", "ctrl+n"))
file_menu.add(MenuItem("打开", "ctrl+o"))
edit_menu = Menu("编辑")
edit_menu.add(MenuItem("撤销", "ctrl+z"))
main_menu = Menu("主菜单")
main_menu.add(file_menu)
main_menu.add(edit_menu)

for line in main_menu.render():
    print(line)
print()
print(file_menu.children[0].click())
print(file_menu.click())
