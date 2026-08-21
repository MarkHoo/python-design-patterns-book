# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》20-备忘录模式-Memento
# 代码块 #2：3.1 经典版：显式的 Memento 类
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy
from dataclasses import dataclass
from typing import Optional


@dataclass
class Memento:
    """备忘录：一个不可变的快照（frozen=True 防止外部乱改）"""
    content: str
    cursor: int


class Editor:
    """发起人：文本编辑器，能存快照、能恢复"""

    def __init__(self):
        self.content = ""
        self.cursor = 0

    def type(self, text: str) -> None:
        self.content += text
        self.cursor = len(self.content)

    def move_cursor(self, pos: int) -> None:
        self.cursor = max(0, min(pos, len(self.content)))

    def save(self) -> Memento:
        """生成快照"""
        return Memento(content=copy.deepcopy(self.content), cursor=self.cursor)

    def restore(self, m: Memento) -> None:
        """从快照恢复"""
        self.content = copy.deepcopy(m.content)
        self.cursor = m.cursor

    def __repr__(self):
        return f"<Editor 内容={self.content!r} 光标={self.cursor}>"


class History:
    """管理者：只负责存快照和取快照"""

    def __init__(self):
        self._stack = []

    def push(self, m: Memento) -> None:
        self._stack.append(m)

    def pop(self) -> Optional[Memento]:
        return self._stack.pop() if self._stack else None


# 使用：写一段 → 存个档 → 继续写 → 后悔了 → 读档
editor = Editor()
history = History()

editor.type("第 1 行：设计模式真好玩。")
history.push(editor.save())          # 存档点 1
print("存档 1：", editor)

editor.type("第 2 行：备忘录模式最实用。")
history.push(editor.save())          # 存档点 2
print("存档 2：", editor)

editor.type("第 3 行：但是写书好累啊……")
print("现在（未存档）：", editor)

snapshot = history.pop()             # 后悔了，回到存档 2
editor.restore(snapshot)
print("读档后：", editor)
