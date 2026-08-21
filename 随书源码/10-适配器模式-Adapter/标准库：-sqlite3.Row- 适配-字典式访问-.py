# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #9：标准库：`sqlite3.Row` 适配"字典式访问"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row        # 启用 Row 工厂：行变成"元组+字典"双接口
conn.execute("CREATE TABLE user (id INTEGER, name TEXT)")
conn.execute("INSERT INTO user VALUES (1, '小明')")
row = conn.execute("SELECT id, name FROM user").fetchone()

print("按下标访问：", row[1])          # 像元组
print("按列名访问：", row["name"])     # 像字典
