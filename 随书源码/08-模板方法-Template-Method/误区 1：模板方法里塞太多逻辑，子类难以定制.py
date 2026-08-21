# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #8：误区 1：模板方法里塞太多逻辑，子类难以定制
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面：基类把"怎么显示"写死，子类想改格式只能复制整个方法
import abc


class BadReport(abc.ABC):
    def generate(self, data):
        header = "===== 报表 ====="
        lines = [f"- {k}: {v}" for k, v in data.items()]
        # 想改分隔符？想加边框？这里写死了，子类无能为力
        return "\n".join([header] + lines)


# 正确：把"每行怎么格式化"做成抽象方法，交给子类
class GoodReport(abc.ABC):
    def generate(self, data):
        lines = [self.format_row(k, v) for k, v in data.items()]
        return "\n".join([self.header()] + lines)

    def header(self):
        return "===== 报表 ====="

    @abc.abstractmethod
    def format_row(self, key, value):
        pass


class MarkdownReport(GoodReport):
    def format_row(self, key, value):
        return f"| {key} | {value} |"


data = {"周一": 100}
print("反面版输出：")
print(BadReport().generate(data))
print("正确版输出：")
print(MarkdownReport().generate(data))
