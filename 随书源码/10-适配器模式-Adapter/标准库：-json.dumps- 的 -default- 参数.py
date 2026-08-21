# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #8：标准库：`json.dumps` 的 `default` 参数
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import json
from datetime import datetime, date

def json_default(obj):
    """适配器：把不认识的对象翻译成可序列化的类型"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"类型 {type(obj).__name__} 不可序列化")

data = {"name": "会议", "time": datetime(2024, 6, 1, 9, 30)}
print(json.dumps(data, default=json_default, ensure_ascii=False))
