# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #6：4.2 用 `abc` 定义工厂钩子：爬虫解析器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import abc
import json
from html.parser import HTMLParser


class PageParser(abc.ABC):
    """产品：网页解析器——从文本里提取链接"""

    @abc.abstractmethod
    def parse(self, text: str) -> list[str]:
        pass


class JsonApiParser(PageParser):
    """解析 JSON 接口返回里的 url 字段"""

    def parse(self, text: str) -> list[str]:
        data = json.loads(text)
        return [item["url"] for item in data["items"]]


class LinkCollector(HTMLParser):
    """收集 HTML 里的所有链接"""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for key, value in attrs:
                if key == "href":
                    self.links.append(value)


class HtmlLinkParser(PageParser):
    def parse(self, text: str) -> list[str]:
        collector = LinkCollector()
        collector.feed(text)
        return collector.links


class CrawlerFactory(abc.ABC):
    """抽象工厂：爬虫用什么解析器，由子类决定"""

    @abc.abstractmethod
    def create_parser(self) -> PageParser:
        pass


class JsonCrawlerFactory(CrawlerFactory):
    def create_parser(self) -> PageParser:
        return JsonApiParser()


class HtmlCrawlerFactory(CrawlerFactory):
    def create_parser(self) -> PageParser:
        return HtmlLinkParser()


def crawl(url: str, text: str, factory: CrawlerFactory) -> list[str]:
    """爬虫主流程：只依赖抽象，不关心具体解析器"""
    parser = factory.create_parser()   # 工厂方法：解析器从这里来
    links = parser.parse(text)
    print(f"从 {url} 提取到 {len(links)} 个链接")
    return links


json_text = '{"items": [{"url": "/a"}, {"url": "/b"}]}'
html_text = '<a href="/home">首页</a><a href="/about">关于</a>'
print(crawl("api.example.com", json_text, JsonCrawlerFactory()))
print(crawl("www.example.com", html_text, HtmlCrawlerFactory()))
