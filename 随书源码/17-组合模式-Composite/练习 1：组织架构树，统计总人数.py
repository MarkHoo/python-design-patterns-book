# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #12：练习 1：组织架构树，统计总人数
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：部门（容器）+ 员工（叶子），统一统计人数
class Employee:
    """叶子：员工"""

    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return ()

    def headcount(self) -> int:
        return 1


class Department:
    """容器：部门，人数 = 子部门 + 员工人数之和"""

    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def headcount(self) -> int:
        return sum(child.headcount() for child in self.children)


tech = Department("技术部")
backend = Department("后端组")
backend.add(Employee("小明"))
backend.add(Employee("小红"))
tech.add(backend)
tech.add(Employee("产品经理老王"))

print("后端组人数:", backend.headcount())
print("技术部总人数:", tech.headcount())
