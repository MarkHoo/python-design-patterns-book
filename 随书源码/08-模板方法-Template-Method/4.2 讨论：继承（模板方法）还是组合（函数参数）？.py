# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #6：4.2 讨论：继承（模板方法）还是组合（函数参数）？
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import abc
import os
import tempfile


# ---- 方案 A：模板方法（继承）----
class ImporterA(abc.ABC):
    def run(self, source):
        rows = self.read(source)
        return self.save(rows)

    @abc.abstractmethod
    def read(self, source):
        pass

    @abc.abstractmethod
    def save(self, rows):
        pass


class CsvImporterA(ImporterA):
    def read(self, source):
        with open(source, encoding="utf-8") as f:
            return [ln.strip() for ln in f if ln.strip()]

    def save(self, rows):
        print(f"[继承版] 入库 {len(rows)} 行")
        return len(rows)


# ---- 方案 B：组合 + 函数参数 ----
def run_import(source, reader, saver):
    rows = reader(source)
    return saver(rows)


def read_csv(source):
    with open(source, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def save_db(rows):
    print(f"[组合版] 入库 {len(rows)} 行")
    return len(rows)


with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
    f.write("1\n2\n3\n")
    path = f.name

try:
    print("继承版：", CsvImporterA().run(path), "行")
    print("组合版：", run_import(path, read_csv, save_db), "行")
finally:
    os.unlink(path)
