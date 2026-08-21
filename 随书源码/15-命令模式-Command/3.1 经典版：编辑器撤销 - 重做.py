# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #2：3.1 经典版：编辑器撤销 / 重做
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class TextEditor:
    """接收者：真正干活的文本编辑器"""

    def __init__(self):
        self.text = ""

    def insert(self, text: str) -> None:
        self.text += text

    def delete(self, count: int) -> None:
        self.text = self.text[:-count]

    def __repr__(self):
        return f"<编辑器 文本={self.text!r}>"


class Command:
    """命令接口：执行 + 撤销"""

    def execute(self) -> None:
        raise NotImplementedError

    def undo(self) -> None:
        raise NotImplementedError


class InsertCommand(Command):
    """插入命令：撤销 = 把自己插进去的删掉"""

    def __init__(self, editor: TextEditor, text: str):
        self.editor = editor
        self.text = text

    def execute(self) -> None:
        self.editor.insert(self.text)

    def undo(self) -> None:
        self.editor.delete(len(self.text))


class DeleteCommand(Command):
    """删除命令：执行前先记下删掉的内容，撤销 = 补回去"""

    def __init__(self, editor: TextEditor, count: int):
        self.editor = editor
        self.count = count
        self.deleted = ""       # 执行时才记录

    def execute(self) -> None:
        self.deleted = self.editor.text[-self.count:]
        self.editor.delete(self.count)

    def undo(self) -> None:
        self.editor.insert(self.deleted)


class CommandHistory:
    """调用者：管理命令的撤销栈和重做栈"""

    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()        # 新操作会清空重做栈

    def undo(self) -> None:
        if not self._undo_stack:
            print("没有可以撤销的操作")
            return
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self) -> None:
        if not self._redo_stack:
            print("没有可以重做的操作")
            return
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)


editor = TextEditor()
history = CommandHistory()

history.execute(InsertCommand(editor, "你好"))
history.execute(InsertCommand(editor, "世界"))
print("输入两段文字后:", editor)

history.execute(DeleteCommand(editor, 3))
print("删除 3 个字符后:", editor)

history.undo()
print("撤销删除后:", editor)

history.undo()
print("再撤销一次后:", editor)

history.redo()
print("重做一次后:", editor)
