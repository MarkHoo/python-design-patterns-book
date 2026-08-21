# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》20-备忘录模式-Memento
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有存档的世界——文档被改坏了只能干瞪眼
class Document:
    """一个简陋的文档对象，没有任何存档能力"""

    def __init__(self):
        self.content = ""

    def type(self, text: str) -> None:
        self.content += text

    def delete_last(self, n: int) -> None:
        self.content = self.content[:-n]


doc = Document()
doc.type("第一章：设计模式入门。")
doc.type("第二章：单例模式。")
print("写了两章：", doc.content)

# 手滑！删多了，而且没法撤销
doc.delete_last(9)
print("删过头了：", doc.content)   # 整章没了，后悔莫及，没有 Ctrl+Z
