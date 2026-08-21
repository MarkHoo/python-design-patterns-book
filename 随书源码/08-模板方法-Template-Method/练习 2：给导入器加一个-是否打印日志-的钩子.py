# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #12：练习 2：给导入器加一个"是否打印日志"的钩子
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：钩子默认 False，子类可覆盖
import abc
import os
import tempfile


class Importer(abc.ABC):
    def run(self, source):
        rows = self.read(source)
        count = self.save(rows)
        if self.verbose():                 # 钩子：默认不打印
            print(f"本次导入 {count} 行")
        return count

    @abc.abstractmethod
    def read(self, source):
        pass

    @abc.abstractmethod
    def save(self, rows):
        pass

    def verbose(self) -> bool:
        return False


class TxtImporter(Importer):
    def read(self, source):
        with open(source, encoding="utf-8") as f:
            return [ln.strip() for ln in f if ln.strip()]

    def save(self, rows):
        print(f"入库 {len(rows)} 行")
        return len(rows)


class VerboseTxtImporter(TxtImporter):
    def verbose(self) -> bool:             # 覆盖钩子
        return True


with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
    f.write("a\nb\nc\n")
    path = f.name

try:
    print("普通导入：")
    TxtImporter().run(path)
    print("verbose 导入：")
    VerboseTxtImporter().run(path)
finally:
    os.unlink(path)
