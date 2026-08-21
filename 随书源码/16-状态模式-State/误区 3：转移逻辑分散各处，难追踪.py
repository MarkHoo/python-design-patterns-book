# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #12：误区 3：转移逻辑分散各处，难追踪
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 状态表集中管理：缺转移当场报错，不会静默出错
TRANSITIONS = {
    ("待支付", "支付"): "已支付",
    ("已支付", "发货"): "已发货",
    # 忘了写：已支付 → 已完成 这条转移
}


def transit(current: str, action: str) -> str:
    key = (current, action)
    if key not in TRANSITIONS:
        raise ValueError(f"没有定义转移：{current} + {action}")
    return TRANSITIONS[key]


try:
    transit("已支付", "完成")
except ValueError as e:
    print("缺转移被当场抓住:", e)
