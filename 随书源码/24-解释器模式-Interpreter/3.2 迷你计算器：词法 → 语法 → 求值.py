# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #3：3.2 迷你计算器：词法 → 语法 → 求值
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 完整迷你计算器：支持 + - * / 和括号
# 第一步：词法分析——字符串切成记号
def tokenize(expr: str) -> list:
    tokens = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            tokens.append(("NUM", int(expr[i:j])))
            i = j
        elif ch in "+-*/()":
            tokens.append((ch, ch))
            i += 1
        else:
            raise ValueError(f"无法识别的字符：{ch!r}")
    tokens.append(("END", ""))
    return tokens

# 第二步：递归下降语法分析——记号流拼成"树"（用嵌套元组表示）
class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def next(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self):
        node = self.parse_add_sub()
        if self.peek()[0] != "END":
            raise ValueError("表达式末尾有多余内容")
        return node

    def parse_add_sub(self):
        node = self.parse_mul_div()
        while self.peek()[0] in ("+", "-"):
            op = self.next()[0]
            right = self.parse_mul_div()
            node = (op, node, right)
        return node

    def parse_mul_div(self):
        node = self.parse_atom()
        while self.peek()[0] in ("*", "/"):
            op = self.next()[0]
            right = self.parse_atom()
            node = (op, node, right)
        return node

    def parse_atom(self):
        tok = self.next()
        if tok[0] == "NUM":
            return ("NUM", tok[1])
        if tok[0] == "(":
            node = self.parse_add_sub()
            if self.next()[0] != ")":
                raise ValueError("缺少右括号")
            return node
        raise ValueError(f"意外的记号：{tok}")

# 第三步：求值——递归遍历"树"
def evaluate(node) -> int:
    kind = node[0]
    if kind == "NUM":
        return node[1]
    op, left, right = node
    a, b = evaluate(left), evaluate(right)
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a // b
    raise ValueError(f"未知运算符：{op}")

def calc(expr: str) -> int:
    return evaluate(Parser(tokenize(expr)).parse())

print("1+2*3 =", calc("1+2*3"))
print("(1+2)*3 =", calc("(1+2)*3"))
print("10-2*3+4 =", calc("10-2*3+4"))
print("(2+3)*(4-1) =", calc("(2+3)*(4-1)"))
