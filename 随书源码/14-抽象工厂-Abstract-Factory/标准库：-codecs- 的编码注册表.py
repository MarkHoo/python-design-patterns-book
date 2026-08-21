# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》14-抽象工厂-Abstract-Factory
# 代码块 #8：标准库：`codecs` 的编码注册表
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import codecs

# codecs.lookup 按名字返回一个 CodecInfo：一族编码工具的"包装盒"
info = codecs.lookup("utf-8")
print("编码族名称:", info.name)

text = "设计模式"
raw, _ = info.encode(text)        # 用这一族的编码器
print("用 utf-8 编码:", raw)
back, _ = info.decode(raw)        # 用这一族的解码器
print("再解码回来:", back)
