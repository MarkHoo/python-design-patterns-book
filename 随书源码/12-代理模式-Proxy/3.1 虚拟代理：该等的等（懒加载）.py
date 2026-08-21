# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #2：3.1 虚拟代理：该等的等（懒加载）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class HeavyImage:
    """真实对象：加载很贵"""

    def __init__(self, filename):
        self.filename = filename
        print(f"正在从磁盘加载 {filename}（50MB，花了 3 秒）...")

    def display(self):
        print(f"显示 {self.filename}")

class ImageProxy:
    """虚拟代理：先不加载，真正要显示时才创建真实对象"""

    def __init__(self, filename):
        self.filename = filename
        self._real = None          # 真实对象先不创建

    def display(self):
        if self._real is None:     # 第一次调用才加载（懒加载）
            self._real = HeavyImage(self.filename)
        self._real.display()

album = [ImageProxy(f"photo{i}.jpg") for i in range(1, 4)]
print("相册已打开，但一张图都没加载")
album[1].display()   # 只看第 2 张，只加载第 2 张
