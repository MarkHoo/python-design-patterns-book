# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #6：4.2 `itertools`：标准库的迭代器工具箱
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import itertools


def fib_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


merged = itertools.chain([1, 2], ["a", "b"], "hi")
print("chain 拼接：", list(merged))

for combo in itertools.product(["红", "蓝"], ["大", "小"]):
    print("product：", combo)

print("斐波那契前 8 个：", list(itertools.islice(fib_gen(), 8)))
