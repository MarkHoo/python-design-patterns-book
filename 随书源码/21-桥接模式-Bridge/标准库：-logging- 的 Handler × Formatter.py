# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》21-桥接模式-Bridge
# 代码块 #7：标准库：`logging` 的 Handler × Formatter
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import logging
import sys

# 维度一：Handler（输出渠道）
console = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("app.log", encoding="utf-8")

# 维度二：Formatter（消息格式）——同一个渠道可以换不同格式
fmt_simple = logging.Formatter("%(message)s")
fmt_detail = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

console.setFormatter(fmt_simple)        # 控制台：简单格式
file_handler.setFormatter(fmt_detail)   # 文件：详细格式

logger = logging.getLogger("bridge_demo")
logger.setLevel(logging.INFO)
logger.addHandler(console)
logger.addHandler(file_handler)

logger.info("这是一条测试日志")
