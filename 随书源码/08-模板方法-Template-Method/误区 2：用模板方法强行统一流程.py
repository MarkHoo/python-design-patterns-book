# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #9：误区 2：用模板方法强行统一流程
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面：子类把每个步骤都重写一遍——说明这套骨架根本不适合它
import abc


class Workflow(abc.ABC):
    def run(self):
        self.step1()
        self.step2()

    @abc.abstractmethod
    def step1(self):
        pass

    @abc.abstractmethod
    def step2(self):
        pass


class WeirdJob(Workflow):
    """这个任务的流程和基类骨架完全不一样"""
    def run(self):      # 连模板方法都整体重写了——骨架成了摆设
        print("直接做一件完全不相关的事")

    def step1(self):
        print("不会被调用")

    def step2(self):
        print("也不会被调用")


WeirdJob().run()
