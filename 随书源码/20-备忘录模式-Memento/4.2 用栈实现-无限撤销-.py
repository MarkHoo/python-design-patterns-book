# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》20-备忘录模式-Memento
# 代码块 #6：4.2 用栈实现"无限撤销"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy
from dataclasses import dataclass, field


@dataclass
class CodeEditor:
    """带撤销功能的迷你编辑器（备忘录=整份文本快照）"""
    text: str = ""
    _history: list = field(default_factory=list)

    def edit(self, new_text: str) -> None:
        self._history.append(copy.deepcopy(self.text))   # 改之前先存档
        self.text = new_text

    def undo(self) -> bool:
        if not self._history:
            return False
        self.text = self._history.pop()                  # 弹出上一个快照
        return True


ed = CodeEditor()
ed.edit("print('hello')")
ed.edit("print('hello world')")
ed.edit("print('hello world!!!')")
print("当前：", ed.text)

ed.undo()
print("撤销 1 次：", ed.text)
ed.undo()
print("撤销 2 次：", ed.text)
ed.undo()
print("撤销 3 次：", ed.text)
print("还能撤销吗：", ed.undo())
