# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有外观的世界——下单流程散落在每个调用方里
def buy_online(sku, qty, amount, address):
    """调用方 A：自己要操心"查库存→扣库存→支付→发货"全套流程"""
    print(f"  库存：检查 {sku} x{qty} 是否有货")
    if qty > 10:
        print("库存不足，下单失败")
        return
    print(f"  库存：扣减 {sku} x{qty}")
    order_id = f"ORD-{sku}-{qty}"
    print(f"  支付：{order_id} 收款 {amount} 元")
    print(f"  物流：{order_id} 发往 {address}")
    print("下单成功！")


def buy_in_store(sku, qty, amount, address):
    """调用方 B：同样的流程，再抄一遍——复制粘贴的臭味"""
    print(f"  库存：检查 {sku} x{qty} 是否有货")
    if qty > 10:
        print("库存不足，下单失败")
        return
    print(f"  库存：扣减 {sku} x{qty}")
    order_id = f"ORD-{sku}-{qty}"
    print(f"  支付：{order_id} 收款 {amount} 元")
    print(f"  物流：{order_id} 发往 {address}")
    print("下单成功！")


buy_online("P001", 2, 199.0, "上海市浦东新区")
buy_in_store("P002", 1, 59.0, "北京市朝阳区")
