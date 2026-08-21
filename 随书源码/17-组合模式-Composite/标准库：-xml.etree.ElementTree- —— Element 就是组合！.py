# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #8：标准库：`xml.etree.ElementTree` —— Element 就是组合！
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import xml.etree.ElementTree as ET

# Element 就是组合：元素可以包含子元素（容器），也可以只有文本（叶子）
root = ET.Element("catalog")
book1 = ET.SubElement(root, "book", {"id": "1"})
ET.SubElement(book1, "title").text = "Python 设计模式修炼手册"
ET.SubElement(book1, "author").text = "修炼者"
book2 = ET.SubElement(root, "book", {"id": "2"})
ET.SubElement(book2, "title").text = "Python 网络爬虫实战"

# 构造完成，直接打印成 XML
ET.indent(root)
print(ET.tostring(root, encoding="unicode"))

# findall / iter / find 都是递归树操作
print("书的数量:", len(root.findall("book")))
for book in root.iter("book"):
    print("发现书 id =", book.get("id"))
print("第一本书的标题:", root.find("book/title").text)
