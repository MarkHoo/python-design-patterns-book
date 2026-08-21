# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #13：练习 2：用 `dataclasses.replace` 生成配置变体
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from dataclasses import dataclass, replace


@dataclass
class AppConfig:
    host: str
    port: int
    debug: bool = False
    workers: int = 4


base = AppConfig(host="0.0.0.0", port=8000)
prod = replace(base, debug=False, workers=8)
dev = replace(base, debug=True)

print("基础配置：", base)
print("生产配置：", prod)
print("开发配置：", dev)
print("基础配置未被改动：", base.port == 8000 and base.workers == 4)
