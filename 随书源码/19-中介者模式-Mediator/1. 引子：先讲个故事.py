# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》19-中介者模式-Mediator
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有中介者的界面——两个组件互相直接引用
class InputBox:
    def __init__(self):
        self.text = ""
        self.listbox = None

    def on_type(self, text):
        self.text = text
        self.listbox.add_item(text)


class ListBox:
    def __init__(self):
        self.items = []
        self.input = None

    def add_item(self, text):
        self.items.append(text)
        self.input.text = ""


inp = InputBox()
lst = ListBox()
inp.listbox = lst
lst.input = inp

inp.on_type("买牛奶")
print("列表条目：", lst.items)
print("输入框内容：", repr(inp.text))
