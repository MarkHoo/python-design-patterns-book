# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》19-中介者模式-Mediator
# 代码块 #10：练习 2：用事件注册表实现"输入 → 列表 + 状态栏"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 练习 2 答案：事件注册表版中介者实现表单联动
class Mediator:
    def __init__(self):
        self._handlers = {}
    def on(self, event, handler):
        self._handlers.setdefault(event, []).append(handler)
    def emit(self, event, *args):
        for h in self._handlers.get(event, []):
            h(*args)


mediator = Mediator()
items = []


def add_to_list(text):
    items.append(text)
    print(f"列表新增：{text}")


def update_status(text):
    print(f"状态栏：当前共 {len(items)} 条")


mediator.on("input", add_to_list)
mediator.on("input", update_status)

for text in ["买牛奶", "交房租", "约牙医"]:
    mediator.emit("input", text)
