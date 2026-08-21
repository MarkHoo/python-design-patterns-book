# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #8：5.2 `shutil`：文件操作的"一站式服务"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import os
import shutil

# 在当前目录创建两个"假图片"文件（本示例的工作目录是隔离的临时目录）
src = "photo.jpg"
dst = "backup.jpg"
with open(src, "wb") as f:
    f.write(b"\xff\xd8" + b"0" * 1024)   # 伪造一张 1026 字节的"图片"

# 方式一：手动复制（模拟 os 层面的繁琐）
with open(src, "rb") as f_in, open(dst, "wb") as f_out:
    f_out.write(f_in.read())
print("手动复制完成，大小：", os.path.getsize(dst), "字节")

# 方式二：shutil.copyfile——一行搞定
shutil.copyfile(src, dst)
print("shutil 复制完成，大小：", os.path.getsize(dst), "字节")

# 清理临时文件
os.remove(src)
os.remove(dst)
