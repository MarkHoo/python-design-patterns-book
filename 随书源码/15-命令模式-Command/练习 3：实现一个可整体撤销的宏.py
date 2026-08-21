# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #14：练习 3：实现一个可整体撤销的宏
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：宏命令——录一串命令，整体执行、整体撤销
class TextEditor:
    def __init__(self):
        self.text = ""

    def insert(self, text: str) -> None:
        self.text += text
        print(f"插入「{text}」，当前：{self.text}")

    def delete(self, count: int) -> None:
        self.text = self.text[:-count]
        print(f"删除 {count} 个字符，当前：{self.text}")


class InsertCommand:
    def __init__(self, editor: TextEditor, text: str):
        self.editor = editor
        self.text = text

    def execute(self) -> None:
        self.editor.insert(self.text)

    def undo(self) -> None:
        self.editor.delete(len(self.text))


class Macro:
    def __init__(self, commands):
        self.commands = commands

    def execute(self) -> None:
        for c in self.commands:
            c.execute()

    def undo(self) -> None:
        for c in reversed(self.commands):
            c.undo()


editor = TextEditor()
macro = Macro([
    InsertCommand(editor, "第一段"),
    InsertCommand(editor, "第二段"),
])
print("--- 执行宏 ---")
macro.execute()
print("--- 撤销宏 ---")
macro.undo()
print("最终文本:", repr(editor.text))
