# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #2：3.1 经典版：数据导入流程
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import abc
import json
import os
import tempfile


class DataImporter(abc.ABC):
    """抽象类：固定了导入流程的骨架"""

    def import_data(self, source: str) -> int:
        """模板方法：流程骨架固定，子类不能改"""
        raw = self.read(source)           # 步骤 1：读取
        cleaned = self.clean(raw)         # 步骤 2：清洗
        count = self.load(cleaned)        # 步骤 3：入库
        if self.should_verify():          # 钩子：默认不校验
            self.verify(count)
        return count

    @abc.abstractmethod
    def read(self, source: str):
        """抽象方法：必须实现——怎么读"""
        pass

    @abc.abstractmethod
    def clean(self, raw) -> list:
        """抽象方法：必须实现——怎么清洗"""
        pass

    @abc.abstractmethod
    def load(self, cleaned: list) -> int:
        """抽象方法：必须实现——怎么入库"""
        pass

    def should_verify(self) -> bool:
        """钩子方法：有默认实现，子类可选覆盖"""
        return False

    def verify(self, count: int) -> None:
        print(f"  校验：{count} 条数据已入库")


class CsvImporter(DataImporter):
    def read(self, source: str):
        print("  读取：CSV 文件")
        with open(source, encoding="utf-8") as f:
            return [ln.strip() for ln in f if ln.strip()]

    def clean(self, raw) -> list:
        print(f"  清洗：去掉注释行，剩 {len(raw)} 行")
        return [ln for ln in raw if not ln.startswith("#")]

    def load(self, cleaned: list) -> int:
        print(f"  入库：写入 {len(cleaned)} 行")
        return len(cleaned)


class JsonImporter(DataImporter):
    def read(self, source: str):
        print("  读取：JSON 文件")
        with open(source, encoding="utf-8") as f:
            return json.load(f)

    def clean(self, raw) -> list:
        print(f"  清洗：过滤无 name 字段的记录，剩 {len(raw)} 条")
        return [item for item in raw if item.get("name")]

    def load(self, cleaned: list) -> int:
        print(f"  入库：写入 {len(cleaned)} 条记录")
        return len(cleaned)

    def should_verify(self) -> bool:
        """覆盖钩子：JSON 导入后做校验"""
        return True


with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
    f.write("name,age\n# 注释行\n小明,18\n小红,20\n")
    csv_path = f.name
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    json.dump([{"name": "小明"}, {"age": 99}], f)
    json_path = f.name

try:
    print("== CSV 导入 ==")
    CsvImporter().import_data(csv_path)
    print("== JSON 导入 ==")
    JsonImporter().import_data(json_path)
finally:
    os.unlink(csv_path)
    os.unlink(json_path)
