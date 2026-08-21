# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #11：误区 3：滥用命令导致类爆炸
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import functools


def toggle(light) -> None:
    light.is_on = not light.is_on
    print(f"灯现在是{'开' if light.is_on else '关'}的")


class Light:
    def __init__(self):
        self.is_on = False


light = Light()
turn_on = functools.partial(toggle, light)   # 打包好的"命令"
for _ in range(3):
    turn_on()
