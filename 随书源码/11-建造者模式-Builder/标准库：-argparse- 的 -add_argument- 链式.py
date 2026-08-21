# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》11-建造者模式-Builder
# 代码块 #7：标准库：`argparse` 的 `add_argument` 链式
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import argparse

parser = argparse.ArgumentParser(description="命令行工具")
parser.add_argument("--host", default="127.0.0.1", help="监听地址")
parser.add_argument("--port", type=int, default=8080, help="端口号")
parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")

# parse_args() 才是"交货"——把攒好的参数解析成对象
args = parser.parse_args(["--port", "9000", "-v"])
print(f"host={args.host} port={args.port} verbose={args.verbose}")
