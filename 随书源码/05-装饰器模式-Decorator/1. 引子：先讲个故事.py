# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有装饰器的世界——需求一个一个来，函数越改越臃肿
def order(user: str, product: str) -> str:
    # 需求 1：加日志
    print(f"[日志] {user} 下单 {product}")
    # 需求 2：加权限校验（插在业务中间）
    if user == "黑名单用户":
        return "下单失败：无权限"
    # —— 核心业务 ——
    return f"订单创建成功：{product}"


print(order("小明", "键盘"))
print(order("黑名单用户", "鼠标"))
