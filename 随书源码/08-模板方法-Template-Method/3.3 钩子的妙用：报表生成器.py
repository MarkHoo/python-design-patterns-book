# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #4：3.3 钩子的妙用：报表生成器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import abc


class ReportGenerator(abc.ABC):
    """抽象报表生成器：骨架固定，细节下放"""

    def generate(self, title: str, data: dict) -> str:
        """模板方法：生成完整报告"""
        parts = [self.make_header(title)]
        parts.append(self.make_body(data))
        if self.should_include_chart(data):   # 钩子
            parts.append(self.make_chart(data))
        parts.append(self.make_footer())
        return "\n".join(parts)

    def make_header(self, title: str) -> str:
        return f"===== {title} ====="

    @abc.abstractmethod
    def make_body(self, data: dict) -> str:
        pass

    def make_chart(self, data: dict) -> str:
        return "图表：趋势折线图"

    @abc.abstractmethod
    def make_footer(self) -> str:
        pass

    def should_include_chart(self, data: dict) -> bool:
        """钩子：默认数据量够大才配图表"""
        return len(data) >= 3


class TextReport(ReportGenerator):
    def make_body(self, data: dict) -> str:
        return "\n".join(f"  {k}: {v}" for k, v in data.items())

    def make_footer(self) -> str:
        return "（文字版报告，无图表）"

    def should_include_chart(self, data: dict) -> bool:
        return False   # 覆盖钩子：文字版永不配图


class HtmlReport(ReportGenerator):
    def make_body(self, data: dict) -> str:
        return "<ul>" + "".join(f"<li>{k}={v}</li>" for k, v in data.items()) + "</ul>"

    def make_footer(self) -> str:
        return "</html>"

    def make_chart(self, data: dict) -> str:
        return "<img src='chart.png' />"


sales = {"周一": 100, "周二": 120, "周三": 90, "周四": 150}
print("== 文字版 ==")
print(TextReport().generate("本周销售", sales))
print("== HTML 版（数据量大，自动配图） ==")
print(HtmlReport().generate("本周销售", sales))
