# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #4：3.2 `@` 语法糖：日志 + 权限，一层层包
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import functools


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[日志] 调用 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def check_permission(func):
    """权限校验装饰器：黑名单用户直接拒绝"""
    BLACKLIST = {"黑名单用户"}

    @functools.wraps(func)
    def wrapper(user: str, *args, **kwargs):
        if user in BLACKLIST:
            return "下单失败：无权限"
        return func(user, *args, **kwargs)
    return wrapper


@log
@check_permission
def order(user: str, product: str) -> str:
    return f"订单创建成功：{product}（下单人：{user}）"


print(order("小明", "键盘"))
print(order("黑名单用户", "鼠标"))
