# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #10：误区 3：把解释器用在不该用的地方
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 误区：普通配置也上"DSL"——杀鸡用牛刀
# 反例：为"数据库地址"写一套词法+语法分析；正例：配置就是数据，用 dict 就完了
config = {
    "db_host": "127.0.0.1",
    "db_port": 3306,
    "timeout": 30,
}
print("数据库地址：", f"{config['db_host']}:{config['db_port']}")
