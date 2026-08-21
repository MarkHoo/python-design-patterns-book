# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有命令的世界——按钮和业务逻辑焊死在一起
class TextEditor:
    def __init__(self):
        self.text = ""

    def insert(self, text: str) -> None:
        self.text += text

    def delete(self, count: int) -> None:
        self.text = self.text[:-count]


class Toolbar:
    """工具栏按钮：直接调用业务对象的方法"""

    def __init__(self, editor: TextEditor):
        self.editor = editor

    def on_insert_click(self, text: str) -> None:
        # 想撤销？想记录宏？没门——动作执行完就消失了
        self.editor.insert(text)

    def on_delete_click(self, count: int) -> None:
        self.editor.delete(count)


editor = TextEditor()
toolbar = Toolbar(editor)
toolbar.on_insert_click("你好")
toolbar.on_insert_click("世界")
print("当前文本:", editor.text)
toolbar.on_delete_click(2)
print("删了 2 个字符后:", editor.text)
print("用户手滑想撤销？动作已经'蒸发'，无从撤起")
