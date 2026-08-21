# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》20-备忘录模式-Memento
# 代码块 #5：4.1 用 `copy.deepcopy` 直接拍"全息快照"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy
from dataclasses import dataclass, field, replace


@dataclass
class Settings:
    """应用配置（不可变风格：只读字段）"""
    theme: str = "light"
    font_size: int = 14
    plugins: list = field(default_factory=list)


s = Settings(theme="dark", font_size=16, plugins=["代码高亮"])
backup = copy.deepcopy(s)               # 改配置前先备份

# 一番折腾……
s.theme = "hacker"
s.plugins.append("vim 模式")
print("折腾后：", s)

# 回滚到备份
s = copy.deepcopy(backup)
print("回滚后：", s)

# 或者用 dataclasses.replace 做"部分回滚"：只还原主题，别的保持现状
s = replace(s, theme="light")
print("部分调整：", s)
