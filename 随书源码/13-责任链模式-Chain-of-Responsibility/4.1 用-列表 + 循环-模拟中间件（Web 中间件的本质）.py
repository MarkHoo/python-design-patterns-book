# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #5：4.1 用"列表 + 循环"模拟中间件（Web 中间件的本质）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 中间件的本质：一个"处理函数"的列表，请求依次穿过
def log_middleware(request):
    print(f"[日志] 收到请求：{request.get('path')}")
    return None                  # 放行：返回 None 表示继续下一个

def auth_middleware(request):
    if not request.get("user"):
        return "401 未登录"      # 拦截：直接返回响应
    return None                  # 放行

def route_middleware(request):
    if request.get("path") == "/":
        return "首页"
    return None

def final_handler(request):
    return f"404：{request.get('path')} 不存在"

middlewares = [log_middleware, auth_middleware, route_middleware]   # 责任链 = 有序列表

def handle_request(request):
    for mw in middlewares:       # 列表 + 循环：请求依次穿过
        response = mw(request)
        if response is not None:
            return response      # 有中间件拦截了
    return final_handler(request)  # 全部放行 → 兜底处理

print(handle_request({"path": "/", "user": "小明"}))
print(handle_request({"path": "/admin", "user": None}))
print(handle_request({"path": "/unknown", "user": "小明"}))
