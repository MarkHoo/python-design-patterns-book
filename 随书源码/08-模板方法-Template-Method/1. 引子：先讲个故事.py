# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：两段 90% 相同的代码——复制粘贴的代价
import json
import os
import tempfile


def import_csv(path):
    print("1. 读取 CSV 文件")
    with open(path, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    print(f"2. 清洗：去掉空行，剩 {len(lines)} 行")
    print("3. 入库：写入数据库")
    return len(lines)


def import_json(path):
    print("1. 读取 JSON 文件")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    print(f"2. 清洗：校验字段，剩 {len(data)} 条")
    print("3. 入库：写入数据库")
    return len(data)


with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
    f.write("name,age\n小明,18\n\n小红,20\n")
    csv_path = f.name
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    json.dump([{"name": "小明"}, {"name": "小红"}], f)
    json_path = f.name

try:
    print("CSV 导入：", import_csv(csv_path), "行")
    print("JSON 导入：", import_json(json_path), "条")
finally:
    os.unlink(csv_path)
    os.unlink(json_path)
