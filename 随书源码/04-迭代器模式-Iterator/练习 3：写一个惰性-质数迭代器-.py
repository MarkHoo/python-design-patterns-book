# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #16：练习 3：写一个惰性"质数迭代器"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import itertools


def primes():
    n = 2
    while True:
        for d in range(2, int(n ** 0.5) + 1):
            if n % d == 0:
                break
        else:                      # for 循环没被 break → 是质数
            yield n
        n += 1


first_six = list(itertools.islice(primes(), 6))
print("前 6 个质数：", first_six)
