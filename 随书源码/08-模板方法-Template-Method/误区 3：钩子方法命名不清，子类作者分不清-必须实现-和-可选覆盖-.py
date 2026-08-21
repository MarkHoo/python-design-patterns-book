# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #10：误区 3：钩子方法命名不清，子类作者分不清"必须实现"和"可选覆盖"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import abc


class Downloader(abc.ABC):
    """命名规范演示：on_ 前缀 = 钩子（可选），_fetch = 抽象（必须）"""

    def download(self, url: str) -> str:
        self.on_before()                 # 钩子：可选覆盖
        data = self._fetch(url)          # 抽象：必须实现
        self.on_after(data)              # 钩子：可选覆盖
        return data

    def on_before(self) -> None:
        pass                             # 钩子默认什么都不做

    @abc.abstractmethod
    def _fetch(self, url: str) -> str:
        pass

    def on_after(self, data: str) -> None:
        print(f"（默认钩子）下载完成，共 {len(data)} 个字符")


class HttpDownloader(Downloader):
    def _fetch(self, url: str) -> str:
        return f"来自 {url} 的内容"

    def on_before(self) -> None:
        print("钩子：检查网络连接")


print(HttpDownloader().download("https://example.com/page"))
