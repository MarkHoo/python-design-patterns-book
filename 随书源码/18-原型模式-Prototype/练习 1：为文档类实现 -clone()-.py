# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #12：练习 1：为文档类实现 `clone()`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class Document:
    def __init__(self, title, sections):
        self.title = title
        self.sections = sections  # 段落列表，每个段落是一个 dict
    def clone(self):
        return copy.deepcopy(self)
    def __repr__(self):
        return f"<Document {self.title!r} 段落数={len(self.sections)}>"


doc = Document("周报", [{"标题": "本周进展", "内容": "完成了登录模块"}])
backup = doc.clone()
backup.sections.append({"标题": "下周计划", "内容": "写测试"})

print("原文档段落数：", len(doc.sections))
print("备份段落数：", len(backup.sections))
print("互不影响：", len(doc.sections) == 1)
