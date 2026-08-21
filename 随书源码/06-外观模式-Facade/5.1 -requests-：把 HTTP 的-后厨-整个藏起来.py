# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #7：5.1 `requests`：把 HTTP 的"后厨"整个藏起来
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import http.client
import http.server
import json
import threading
import urllib.parse


class ApiHandler(http.server.BaseHTTPRequestHandler):
    """本地测试用微型接口服务"""

    def do_GET(self):
        # ensure_ascii=False：让中文以原文输出（否则会变成 \u5c0f\u660e 转义）
        body = json.dumps({"code": 0, "data": {"name": "小明", "level": 3}}, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass  # 屏蔽请求日志，保持输出干净


server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), ApiHandler)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()

# 方式一：直接用 http.client——拼请求、读响应、解析 JSON 全要自己来
conn = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
conn.request("GET", "/api/user/1")
resp = conn.getresponse()
raw = resp.read().decode("utf-8")
print("http.client 手写：", raw)
conn.close()

# 方式二：一个迷你 requests——把上面那堆步骤都藏进外观
class MiniRequests:
    """外观：仿 requests 的极简版，只封装 http.client"""

    def get(self, url: str) -> dict:
        parts = urllib.parse.urlsplit(url)
        conn = http.client.HTTPConnection(parts.hostname, parts.port, timeout=3)
        conn.request("GET", parts.path)
        resp = conn.getresponse()
        data = json.loads(resp.read().decode("utf-8"))
        conn.close()
        return data


data = MiniRequests().get(f"http://127.0.0.1:{port}/api/user/1")
print("MiniRequests 一行：", data)

server.shutdown()
thread.join()
