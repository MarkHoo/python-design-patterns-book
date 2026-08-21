# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #3：3.2 全部经过型：评论过滤链（每个节点都处理）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Filter:
    def __init__(self):
        self._next = None

    def set_next(self, f):
        self._next = f
        return f

    def process(self, text):
        if self._next:
            return self._next.process(text)
        return text

class SensitiveFilter(Filter):
    """敏感词过滤：处理完继续传给下一个"""

    def process(self, text):
        text = text.replace("垃圾", "**").replace("混蛋", "**")
        return super().process(text)

class AdFilter(Filter):
    """广告过滤：含"加微信"就标记"""

    def process(self, text):
        if "加微信" in text:
            text = text + "（疑似广告）"
        return super().process(text)

class LengthFilter(Filter):
    """长度过滤：超过 30 字截断"""

    def process(self, text):
        if len(text) > 30:
            text = text[:30] + "……"
        return super().process(text)

chain = SensitiveFilter()
chain.set_next(AdFilter()).set_next(LengthFilter())

msg1 = "这个混蛋又在发广告，加微信领券"
msg2 = "这是一条很长的正常评论，讲了整整五十个字的故事，从早讲到晚，非常啰嗦，请务必看完哦"

print("原始：", msg1)
print("过滤后：", chain.process(msg1))
print()
print("原始：", msg2)
print("过滤后：", chain.process(msg2))
