# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #13：练习 2：用"函数观察者"实现任务完成提醒
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：观察者就是函数，主题存回调列表
class TaskCenter:
    """任务中心：任务完成时广播"""

    def __init__(self):
        self._watchers = []

    def watch(self, fn):
        self._watchers.append(fn)

    def complete(self, task_name, cost):
        print(f"任务完成：{task_name}（耗时 {cost} 秒）")
        for fn in self._watchers:
            fn(task_name, cost)


def notify_leader(task, cost):
    print(f"  [领导] {task} 完成，耗时 {cost}s")


def save_log(task, cost):
    print(f"  [日志] 记录 {task} 耗时 {cost}s")


center = TaskCenter()
center.watch(notify_leader)
center.watch(save_log)
center.complete("数据清洗", 12)
