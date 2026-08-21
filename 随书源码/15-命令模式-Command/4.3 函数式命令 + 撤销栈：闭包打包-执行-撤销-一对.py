# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #7：4.3 函数式命令 + 撤销栈：闭包打包"执行/撤销"一对
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def make_commands(editor, text: str):
    """函数式命令：把"执行"和"撤销"打包成一对函数"""
    def do() -> None:
        editor.text += text

    def undo() -> None:
        editor.text = editor.text[:-len(text)]

    return do, undo


class Editor:
    def __init__(self):
        self.text = ""


editor = Editor()
undo_stack = []

do1, undo1 = make_commands(editor, "设计")
do2, undo2 = make_commands(editor, "模式")

do1()
undo_stack.append(undo1)
do2()
undo_stack.append(undo2)
print("执行两条命令后:", repr(editor.text))

undo_stack.pop()()
print("撤销一次后:", repr(editor.text))

undo_stack.pop()()
print("再撤销一次后:", repr(editor.text))
