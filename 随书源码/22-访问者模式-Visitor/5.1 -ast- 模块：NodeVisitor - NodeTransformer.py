# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #7：5.1 `ast` 模块：NodeVisitor / NodeTransformer
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# NodeTransformer：不只是"看"，还能"改"语法树
import ast

class AddOne(ast.NodeTransformer):
    """把所有数字字面量 +1"""

    def visit_Constant(self, node):
        if isinstance(node.value, int):
            node.value += 1
        return node

source = "price = 10 + 5"
tree = ast.parse(source)
new_tree = AddOne().visit(tree)
print("改写后的代码：", ast.unparse(new_tree))
