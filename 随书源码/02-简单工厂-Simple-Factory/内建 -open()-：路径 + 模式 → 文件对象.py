# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #10：内建 `open()`：路径 + 模式 → 文件对象
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import os
import tempfile

with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
    f.write("临时文件内容")
    path = f.name

with open(path, "r", encoding="utf-8") as f_text:
    print("文本模式返回：", type(f_text).__name__)
with open(path, "rb") as f_bin:
    print("二进制模式返回：", type(f_bin).__name__)
os.unlink(path)
