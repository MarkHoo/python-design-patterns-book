# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #13：练习 3：给权限链加上兜底
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：链尾加兜底放行节点
class Node:
    def __init__(self, name):
        self.name = name
        self._next = None

    def set_next(self, n):
        self._next = n
        return n

    def handle(self, req):
        if self._next:
            return self._next.handle(req)
        return None

class AuthNode(Node):
    def handle(self, req):
        if not req.get("token"):
            return "拒绝访问：未登录"
        return super().handle(req)

class RateNode(Node):
    def handle(self, req):
        if req.get("path") == "/api/vip":
            return "拒绝访问：需要会员"
        return super().handle(req)

class FallbackNode(Node):
    """兜底：走到这里说明全部检查通过"""

    def handle(self, req):
        return "放行：请求已通过全部检查"

chain = AuthNode("登录检查")
chain.set_next(RateNode("限流检查")).set_next(FallbackNode("兜底放行"))

print(chain.handle({"path": "/api/vip", "token": "abc"}))
print(chain.handle({"path": "/api/free", "token": "abc"}))
print(chain.handle({"path": "/api/free"}))
