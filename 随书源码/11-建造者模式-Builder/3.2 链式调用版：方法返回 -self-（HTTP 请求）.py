# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》11-建造者模式-Builder
# 代码块 #3：3.2 链式调用版：方法返回 `self`（HTTP 请求）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class HttpRequest:
    """产品：HTTP 请求"""

    def __init__(self):
        self.method = "GET"
        self.url = ""
        self.headers = {}
        self.body = None
        self.timeout = 30

    def __repr__(self):
        return f"<请求 {self.method} {self.url} headers={self.headers} body={self.body} 超时={self.timeout}s>"

class RequestBuilder:
    """建造者：每个方法返回 self，支持链式调用"""

    def __init__(self, url):
        self._req = HttpRequest()
        self._req.url = url

    def method(self, m):
        self._req.method = m
        return self

    def header(self, key, value):
        self._req.headers[key] = value
        return self

    def body(self, data):
        self._req.body = data
        return self

    def timeout(self, seconds):
        self._req.timeout = seconds
        return self

    def build(self):
        return self._req

req = (RequestBuilder("https://api.example.com/orders")
       .method("POST")
       .header("Content-Type", "application/json")
       .header("Authorization", "Bearer token123")
       .body('{"amount": 99.9}')
       .timeout(10)
       .build())
print(req)
