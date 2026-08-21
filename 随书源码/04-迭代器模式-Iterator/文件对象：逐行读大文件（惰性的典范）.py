# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #8：文件对象：逐行读大文件（惰性的典范）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import io

# 用 io.StringIO 模拟一个"文件"
fake_file = io.StringIO("第一行\n第二行\n第三行\n")

for line in fake_file:             # 文件对象可迭代，每次吐一行
    print("读到：", line.strip())
