# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #5：4.1 模块即外观
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# ===== 模拟一个组织良好的模块：config_loader.py =====
import os
import tempfile


# 模块内部：三个"脏活累活"的私有函数（下划线 = 对外不可见）
def _read_raw(path: str) -> str:
    print("  底层：读取配置文件")
    with open(path, encoding="utf-8") as f:
        return f.read()


def _parse(text: str) -> dict:
    print("  底层：解析 INI 格式")
    result = {}
    for line in text.splitlines():
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            result[key.strip()] = value.strip()
    return result


def _validate(config: dict) -> dict:
    print("  底层：校验必填字段")
    if "name" not in config:
        raise ValueError("缺少 name 字段")
    return config


# 模块对外：只暴露这一个"外观函数"
def load_config(path: str) -> dict:
    """读配置：读取 → 解析 → 校验，调用方一行搞定"""
    return _validate(_parse(_read_raw(path)))


# ===== 调用方：完全不知道模块内部有三个函数 =====
with tempfile.NamedTemporaryFile("w", suffix=".ini", delete=False, encoding="utf-8") as f:
    f.write("# 我的配置\nname=小明\nlevel=3\n")
    tmp_path = f.name

try:
    config = load_config(tmp_path)
    print("调用方拿到的配置：", config)
finally:
    os.unlink(tmp_path)
