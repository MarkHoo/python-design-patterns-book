# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #16：练习 3：把 24 小时制适配成 12 小时制
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：函数式适配
def to_12h(time_24: str) -> str:
    h, m = map(int, time_24.split(":"))
    period = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12          # 0 点和 12 点都显示为 12
    return f"{h12}:{m:02d} {period}"

print(to_12h("09:30"))
print(to_12h("12:00"))
print(to_12h("23:30"))
print(to_12h("00:15"))
