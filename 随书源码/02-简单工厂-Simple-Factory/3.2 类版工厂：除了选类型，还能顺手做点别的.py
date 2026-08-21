# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #3：3.2 类版工厂：除了选类型，还能顺手做点别的
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import json


class JsonParser:
    def parse(self, text: str):
        return json.loads(text)


class PlainParser:
    def parse(self, text: str):
        return text.strip()


class ParserFactory:
    """类版工厂：选类型 + 顺手做缓存"""

    def __init__(self):
        self._cache = {}

    def get_parser(self, fmt: str):
        if fmt not in self._cache:
            if fmt == "json":
                self._cache[fmt] = JsonParser()
            elif fmt == "plain":
                self._cache[fmt] = PlainParser()
            else:
                raise ValueError(f"未知格式：{fmt}")
            print(f"首次创建 {fmt} 解析器")
        return self._cache[fmt]


factory = ParserFactory()
p1 = factory.get_parser("json")
p2 = factory.get_parser("json")
print("JSON 解析结果：", p1.parse('{"name": "小明", "age": 18}'))
print("同一个 json 解析器被复用：", p1 is p2)
