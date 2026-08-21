# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》14-抽象工厂-Abstract-Factory
# 代码块 #9：误区 1：加新产品要改所有工厂（开闭原则的代价）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from abc import ABC, abstractmethod


class ThemeFactory(ABC):
    @abstractmethod
    def create_button(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_slider(self) -> str:      # 新需求：加一个"滑块"产品
        raise NotImplementedError


class LightFactory(ThemeFactory):
    def create_button(self) -> str:
        return "浅色按钮"

    # 忘了实现 create_slider——老工厂立刻翻车


try:
    LightFactory()   # 抽象方法没实现，实例化直接报错
except TypeError as e:
    print("老工厂没跟上新需求:", e)
