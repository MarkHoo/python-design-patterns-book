# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：打开相册就把所有高清大图全加载了——慢死了
class HeavyImage:
    """一张高清大图：加载很贵"""

    def __init__(self, filename):
        self.filename = filename
        print(f"正在从磁盘加载 {filename}（50MB，花了 3 秒）...")

    def display(self):
        print(f"显示 {self.filename}")

# 相册应用：一打开就把 3 张图全部加载
album = [HeavyImage(f"photo{i}.jpg") for i in range(1, 4)]
print("——用户其实只想看第 1 张——")
album[0].display()
