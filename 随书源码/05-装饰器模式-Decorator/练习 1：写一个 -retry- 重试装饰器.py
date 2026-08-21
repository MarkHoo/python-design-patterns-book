# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #15：练习 1：写一个 `retry` 重试装饰器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def retry(times: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ValueError as e:
                    print(f"第 {attempt} 次失败：{e}")
            raise ValueError(f"重试 {times} 次仍失败")
        return wrapper
    return decorator


@retry(3)
def flaky():
    """前两次失败，第三次成功"""
    flaky.calls = getattr(flaky, "calls", 0) + 1
    if flaky.calls < 3:
        raise ValueError("网络抖动")
    return "请求成功"


print(flaky())
