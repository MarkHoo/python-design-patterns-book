# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #13：练习 3：用"组合 + 函数参数"重写同一流程
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：组合版"模板"——流程就是函数列表，依次执行
def run_flow(steps, *args):
    """steps 是一串函数，前一个的输出作为后一个的输入"""
    result = None
    for step in steps:
        result = step(result, *args)
    return result


def step_prepare(prev, name):
    print(f"准备：{name}")
    return name


def step_cook(prev, name):
    print(f"烹饪：{prev}")
    return "熟了的" + prev


def step_serve(prev, name):
    print(f"上桌：{prev}")
    return prev


dish = run_flow([step_prepare, step_cook, step_serve], "红烧肉")
print("成品：", dish)
