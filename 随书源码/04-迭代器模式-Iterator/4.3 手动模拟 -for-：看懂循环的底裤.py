# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #7：4.3 手动模拟 `for`：看懂循环的底裤
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

words = ["迭代", "器", "模式"]

it = iter(words)                   # ① 拿到迭代器
while True:
    try:
        word = next(it)            # ② 取下一个
        print("取到：", word)
    except StopIteration:          # ③ 取完了
        print("迭代结束")
        break
