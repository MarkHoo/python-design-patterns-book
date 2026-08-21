# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #13：练习 1：状态表版电梯
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：状态表驱动电梯——(状态, 动作) → 下一状态
from enum import Enum


class ElevatorState(Enum):
    IDLE = "静止"
    MOVING = "运行中"
    DOOR_OPEN = "门开着"


TRANSITIONS = {
    (ElevatorState.IDLE, "press"): ElevatorState.MOVING,
    (ElevatorState.MOVING, "arrive"): ElevatorState.DOOR_OPEN,
    (ElevatorState.DOOR_OPEN, "close"): ElevatorState.IDLE,
    (ElevatorState.DOOR_OPEN, "press"): ElevatorState.MOVING,
}


class Elevator:
    def __init__(self):
        self.state = ElevatorState.IDLE

    def trigger(self, event: str) -> None:
        key = (self.state, event)
        if key not in TRANSITIONS:
            raise ValueError(f"非法事件：{self.state.value} + {event}")
        self.state = TRANSITIONS[key]
        print(f"事件[{event}] → 现在是「{self.state.value}」")


elevator = Elevator()
elevator.trigger("press")
elevator.trigger("arrive")
elevator.trigger("close")
elevator.trigger("press")
