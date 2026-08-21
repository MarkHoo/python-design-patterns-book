# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #7：标准库：`logging` 的 logger 层级与传播
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import logging
import sys

# 根 logger：所有 logger 的"兜底"
root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(name)s -> %(message)s"))
root.addHandler(handler)

# 子 logger：不配 handler，日志会"冒泡"到父 logger 的 handler
child = logging.getLogger("app.service")
child.info("子 logger 的日志，父 logger 帮忙输出")

# 孙子 logger：继续向上冒泡
grand = logging.getLogger("app.service.db")
grand.warning("孙子 logger 的警告也冒泡了")
