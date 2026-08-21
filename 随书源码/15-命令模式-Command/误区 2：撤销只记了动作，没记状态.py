# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #10：误区 2：撤销只记了动作，没记状态
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面教材：撤销命令没保存"被删了什么"
class DeleteWithoutMemory:
    def __init__(self, editor, count: int):
        self.editor = editor
        self.count = count

    def execute(self) -> None:
        self.editor.text = self.editor.text[:-self.count]

    def undo(self) -> None:
        raise RuntimeError("我不知道刚才删了什么！")


class Editor:
    def __init__(self):
        self.text = "设计模式"


editor = Editor()
cmd = DeleteWithoutMemory(editor, 2)
cmd.execute()
print("删除后:", editor.text)
try:
    cmd.undo()
except RuntimeError as e:
    print("撤销失败:", e)
