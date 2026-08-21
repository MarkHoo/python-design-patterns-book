# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #5：4.1 状态表：dict 映射 (状态, 动作) → 下一状态
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from enum import Enum


class Light(Enum):
    RED = "红"
    GREEN = "绿"
    YELLOW = "黄"


# 状态表：(当前状态, 动作) → 下一状态
TRANSITIONS = {
    (Light.RED, "timeout"): Light.GREEN,
    (Light.GREEN, "timeout"): Light.YELLOW,
    (Light.YELLOW, "timeout"): Light.RED,
}


def next_state(current: Light, action: str) -> Light:
    key = (current, action)
    if key not in TRANSITIONS:
        raise ValueError(f"非法转移：{current.name} + {action}")
    return TRANSITIONS[key]


state = Light.RED
for i in range(4):
    print(f"第 {i + 1} 轮：{state.value}灯亮，车辆{'通行' if state is Light.GREEN else '停止'}")
    state = next_state(state, "timeout")
