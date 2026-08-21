# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #13：练习 3：写一个"指路 DSL"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：把"口语指路"解释成程序动作
def parse_directions(text: str) -> list:
    """词法+语法：'向前 N 步' / '左转' / '右转' → 指令列表"""
    commands = []
    words = text.split()
    i = 0
    while i < len(words):
        word = words[i]
        if word in ("左转", "右转"):
            commands.append((word, 0))
            i += 1
        elif word == "向前":
            commands.append(("向前", int(words[i + 1])))
            i += 2
        elif word == "步":
            i += 1
        else:
            raise ValueError(f"听不懂：{word}")
    return commands

def run(commands: list, start: tuple) -> tuple:
    """求值：按指令移动，返回终点坐标 (x, y)"""
    x, y = start
    direction = 0   # 0=北 1=东 2=南 3=西
    for cmd, arg in commands:
        if cmd == "左转":
            direction = (direction - 1) % 4
        elif cmd == "右转":
            direction = (direction + 1) % 4
        elif cmd == "向前":
            dx = [0, 1, 0, -1][direction]
            dy = [1, 0, -1, 0][direction]
            x += dx * arg
            y += dy * arg
    return (x, y)

text = "向前 3 步 右转 向前 2 步 左转 向前 1 步"
commands = parse_directions(text)
print("解析出的指令：", commands)
print("从 (0,0) 出发，终点：", run(commands, (0, 0)))
