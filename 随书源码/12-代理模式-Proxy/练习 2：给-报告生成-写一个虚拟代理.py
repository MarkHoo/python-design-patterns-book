# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #12：练习 2：给"报告生成"写一个虚拟代理
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：虚拟代理（懒加载）
class Report:
    def __init__(self, title):
        print(f"正在生成报告《{title}》，需要 5 秒……")
        self.title = title

    def show(self):
        return f"《{self.title}》报告内容"

class ReportProxy:
    def __init__(self, title):
        self.title = title
        self._real = None

    def show(self):
        if self._real is None:
            self._real = Report(self.title)
        return self._real.show()

proxy = ReportProxy("年度总结")
print("代理已创建，报告还没生成")
print(proxy.show())
print(proxy.show())   # 第二次不再生成
