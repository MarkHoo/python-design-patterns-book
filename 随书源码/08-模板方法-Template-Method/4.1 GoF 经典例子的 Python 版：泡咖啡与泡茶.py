# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #5：4.1 GoF 经典例子的 Python 版：泡咖啡与泡茶
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import abc


class CaffeineBeverage(abc.ABC):
    """含咖啡因饮料：烧水→冲泡→倒杯→加料，骨架固定"""

    def prepare(self) -> None:
        print("1. 把水烧开")
        self.brew()                    # 抽象：怎么冲泡
        self.pour_in_cup()             # 具体：倒进杯子
        if self.wants_condiments():    # 钩子：要不要加料
            self.add_condiments()      # 抽象：加什么料

    @abc.abstractmethod
    def brew(self) -> None:
        pass

    def pour_in_cup(self) -> None:
        print("3. 倒进杯子里")

    def wants_condiments(self) -> bool:
        """钩子：默认要加料"""
        return True

    @abc.abstractmethod
    def add_condiments(self) -> None:
        pass


class Coffee(CaffeineBeverage):
    def brew(self) -> None:
        print("2. 用沸水冲泡咖啡粉")

    def add_condiments(self) -> None:
        print("4. 加糖和牛奶")


class Tea(CaffeineBeverage):
    def brew(self) -> None:
        print("2. 用沸水浸泡茶叶")

    def add_condiments(self) -> None:
        print("4. 加柠檬片")

    def wants_condiments(self) -> bool:
        return False   # 覆盖钩子：纯茶不加料


print("== 泡咖啡 ==")
Coffee().prepare()
print("== 泡茶 ==")
Tea().prepare()
