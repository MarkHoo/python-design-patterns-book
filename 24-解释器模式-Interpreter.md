# 第 24 章 解释器模式（Interpreter）

> **一句话总结**：定义一门小语言，写个程序解释它。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 行为型 | ★★★★★ | ★☆☆☆☆ |

---

## 1. 引子：先讲个故事

给老外指路你会怎么做？他不会中文，你不会英文，于是你连比带划："直走，然后右转，再直走 50 米。"——你把"走路"这件事翻译成了一系列**他听得懂的动作**。同声传译也是这个道理：把一种语言，翻译成另一种语言背后的动作。

程序世界里也有这种需求：用户给你一段"表达式"（`1+2*3`）、一条"规则"（"周末打 8 折"），你要把它翻译成程序能执行的动作。最省事的写法是拿字符串硬凑——比如把表达式按 `+` 号切开：

```python
# 引子：没有解释器的世界——表达式用字符串硬凑
def calc_v1(expr: str) -> int:
    """最朴素的加法器：只认 '数字+数字' 一种格式"""
    left, right = expr.split("+")
    return int(left) + int(right)

print("3+5 =", calc_v1("3+5"))          # 还行

# 表达式稍微复杂一点，各种翻车
try:
    print("3+5+2 =", calc_v1("3+5+2"))  # 三个数？两个变量装不下
except Exception as e:
    print("3+5+2 翻车了：", type(e).__name__, "——", e)

try:
    print("10-3 =", calc_v1("10-3"))    # 减法？想都别想
except Exception as e:
    print("10-3 翻车了：", type(e).__name__, "——", e)
```

运行输出：

```
3+5 = 8
3+5+2 翻车了： ValueError —— too many values to unpack (expected 2)
10-3 翻车了： ValueError —— not enough values to unpack (expected 2, got 1)
```

问题在于：字符串是"扁平"的，而表达式是"有结构的"（`1+2*3` 里乘法优先级更高）。你需要的不只是切字符串，而是一门**小语言 + 一个解释器**：先分词，再按语法规则拼成树，最后求值。

---

## 2. 模式登场

### 定义

> **解释器模式**：给定一门语言，定义它的文法（语法规则）表示，并提供一个解释器，用这个解释器来解释语言中的句子。

### 三步走：词法 → 语法 → 求值

任何"语言处理"都逃不过这三大步：

1. **词法分析（tokenize）**：把字符串切成记号流——数字、运算符、括号各归各；
2. **语法分析（parse）**：按语法规则把记号流拼成**抽象语法树（AST）**——表达式的"结构"；
3. **求值（evaluate）**：递归遍历语法树，算出结果。

**抽象语法树（AST）**是把"扁平字符串"变成"有结构的树"的关键：`3 + 5 * 2` 的树是"加法节点下面挂一个数字和一个乘法节点"，乘法天然比加法低一层，优先级问题迎刃而解。

### 结构

```
     "3 + 5 * 2"              （源字符串）
          │ ① 词法分析
          ▼
  [NUM(3), PLUS, NUM(5), MUL, NUM(2)]    （记号流）
          │ ② 语法分析
          ▼
       ┌─── Add ───┐
       │           │
     NUM(3)    ┌── Mul ──┐
               │         │
            NUM(5)    NUM(2)            （抽象语法树 AST）
          │ ③ 求值（递归遍历）
          ▼
             13
```

### 角色

| 角色 | 说明 |
|------|------|
| **AbstractExpression** | 抽象表达式：所有节点的公共接口（如 `evaluate`） |
| **TerminalExpression** | 终结符表达式：数字（叶子节点） |
| **NonterminalExpression** | 非终结符表达式：加/减/乘（组合子节点） |
| **Client** | 组装语法树并调用解释 |

### 为什么它"最难且最不常用"

实现成本高（词法 + 语法 + 求值三套代码）、调试困难、类数量爆炸，而且现实里绝大多数"语言"都有现成解释器（正则、SQL、Python 表达式）。所以 GoF 23 个模式里，解释器是"面试最爱问、日常最不用"的那个——**它的价值在于让你理解"语言是怎么被处理的"，而不是让你真的去写语言**。

---

## 3. Python 实现

### 3.1 经典版：表达式树 + 每个节点自己会求值

先定义一棵"表达式树"：数字是叶子（终结符），加减乘是树枝（非终结符）。每个节点都会 `evaluate`，求值就是递归：

```python
# 解释器经典版：表达式树 + 每个节点自己会求值
class Expr:
    """抽象表达式：所有节点的基类"""

    def evaluate(self) -> int:
        raise NotImplementedError

class Number(Expr):
    """终结符：数字"""

    def __init__(self, value: int):
        self.value = value

    def evaluate(self) -> int:
        return self.value

class Add(Expr):
    """非终结符：加法"""

    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self) -> int:
        return self.left.evaluate() + self.right.evaluate()

class Multiply(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def evaluate(self) -> int:
        return self.left.evaluate() * self.right.evaluate()

# 3 + 5 * 2：乘法节点挂在加法下面，优先级天然正确
expr = Add(Number(3), Multiply(Number(5), Number(2)))
print("3 + 5 * 2 =", expr.evaluate())

# (3 + 5) * 2：换括号就是换树形
expr2 = Multiply(Add(Number(3), Number(5)), Number(2))
print("(3 + 5) * 2 =", expr2.evaluate())
```

运行输出：

```
3 + 5 * 2 = 13
(3 + 5) * 2 = 16
```


### 3.2 迷你计算器：词法 → 语法 → 求值

一个支持 `+ - * /` 和括号的完整计算器，三大步一个不少。语法分析用**递归下降**（每个语法规则对应一个函数）：

```python
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
```

运行输出：

```
1+2*3 = 7
(1+2)*3 = 9
10-2*3+4 = 8
(2+3)*(4-1) = 15
```

看看 `parse_add_sub` 和 `parse_mul_div` 的分工：加法层调用乘法层，乘法层调用原子层——**优先级就是靠"谁包着谁"实现的**。这就是递归下降解析器的精髓。

### 3.3 打折规则 DSL：让业务人员自己写规则

把"周末打 8 折"这种口语规则，解释成程序能判断的条件：

```python
# 规则 DSL："周末 打 8 折" 这种话，让解释器来读懂
def tokenize_rule(text: str) -> list:
    """词法：把规则字符串切成记号"""
    tokens = []
    for word in text.split():
        if word in ("周末", "工作日", "会员", "非会员", "打", "折"):
            tokens.append(("KW", word))
        elif word.isdigit():
            tokens.append(("NUM", int(word)))
        else:
            raise ValueError(f"未知词：{word}")
    tokens.append(("END", ""))
    return tokens

def parse_rule(tokens: list):
    """语法：'条件 打 N 折' → ('折扣', 条件, N)"""
    cond = tokens[0][1]
    if tokens[1] != ("KW", "打") or tokens[2][0] != "NUM":
        raise ValueError("规则格式应为：条件 打 N 折")
    return ("折扣", cond, tokens[2][1])

def apply_rule(rule, is_weekend: bool, is_vip: bool) -> float:
    """求值：根据实际场景算出这条规则打几折（不匹配就是不打折）"""
    _, cond, discount = rule
    match = {
        "周末": is_weekend,
        "工作日": not is_weekend,
        "会员": is_vip,
        "非会员": not is_vip,
    }[cond]
    return discount / 10 if match else 1.0

def final_discount(rules, is_weekend: bool, is_vip: bool) -> float:
    """多条规则都生效时，取最优惠的折扣"""
    return min(apply_rule(r, is_weekend, is_vip) for r in rules)

rules = [
    parse_rule(tokenize_rule("周末 打 8 折")),
    parse_rule(tokenize_rule("会员 打 9 折")),
]
print("周六 + 会员：", final_discount(rules, True, True))
print("周六 + 非会员：", final_discount(rules, True, False))
print("周二 + 会员：", final_discount(rules, False, True))
print("周二 + 非会员：", final_discount(rules, False, False))
```

运行输出：

```
周六 + 会员： 0.8
周六 + 非会员： 0.8
周二 + 会员： 0.9
周二 + 非会员： 1.0
```

有了这门"规则小语言"，运营改规则就不用改代码了——改一行配置字符串就行。这就是解释器模式的典型价值：**把"变"的部分做成语言，把"不变"的部分留在程序里**。

---

## 4. Python 特有玩法

### 4.1 用 `ast` 模块解析，自己只写求值器

自己写词法 + 语法分析很累？Python 自带 `ast` 模块帮你把表达式解析成语法树——你只需要写求值器：

```python
# 用标准库 ast 做语法分析，自己只写求值器
import ast

class MyEvaluator(ast.NodeVisitor):
    """遍历 ast 生成的表达式树并求值（支持变量）"""

    def __init__(self, env: dict):
        self.env = env

    def visit_Constant(self, node):
        return node.value

    def visit_Name(self, node):
        if node.id not in self.env:
            raise NameError(f"未定义变量：{node.id}")
        return self.env[node.id]

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        raise ValueError(f"不支持的运算：{type(node.op).__name__}")

tree = ast.parse("price * qty - 10", mode="eval")
ev = MyEvaluator({"price": 30, "qty": 2})
print("price * qty - 10 =", ev.visit(tree.body))
```

运行输出：

```
price * qty - 10 = 50
```

`ast.parse` 干掉了 3.2 里所有的 tokenize 和 Parser 代码——这就是"现代做法"：**解析交给标准库，解释留给自己**。

### 4.2 `ast.literal_eval`：安全地解析字面量

只想要"读配置"级别的解析（列表、字典、元组），不想执行任何代码？`ast.literal_eval` 只认字面量：

```python
# ast.literal_eval：只认字面量，不执行任何代码——安全！
import ast

# 解析配置文件里的"字面量"字符串
print(ast.literal_eval("[1, 2, 3]"))
print(ast.literal_eval("{'name': '小明', 'age': 18}"))
print(ast.literal_eval("(1, 2)"))

# 表达式？不行——literal_eval 只认字面量
try:
    ast.literal_eval("1 + 2")
except ValueError:
    print("拒绝执行表达式：ValueError")
```

运行输出：

```
[1, 2, 3]
{'name': '小明', 'age': 18}
(1, 2)
拒绝执行表达式：ValueError
```


### 4.3 `eval` 的危险性（警示）

`eval` 确实能求值表达式——但它不是"求值器"，而是"**任意代码执行器**"：`eval("__import__('math').sqrt(16)")` 能调用函数，`eval("__import__('os').system('rm -rf /')")` 就能执行系统命令。**把 eval 用在用户输入上，等于把服务器的钥匙挂在门口**。要安全求值，用 `ast.literal_eval`（只认字面量）或自写求值器（白名单运算符，见 4.1 和误区 1）。

---

## 5. 真实世界中的它

### 5.1 `re` 模块：正则表达式就是一门小语言

正则表达式（`\d+`、`(?P<year>\d{4})`）是一套完整的"字符匹配语言"，`re` 模块就是它的解释器：

```python
# 正则表达式：一门"字符匹配语言"，re 模块就是它的解释器
import re

pattern = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
m = pattern.search("会议日期：2026-05-01，请准时参加")
if m:
    print("年：", m.group("year"))
    print("月：", m.group("month"))
    print("日：", m.group("day"))

text = "客服 138-0000-1111，售后 139-0000-2222"
print("电话号码：", re.findall(r"\d{3}-\d{4}-\d{4}", text))
```

运行输出：

```
年： 2026
月： 05
日： 01
电话号码： ['138-0000-1111', '139-0000-2222']
```


### 5.2 `ast` 模块：Python 自己也在用解释器

Python 解释器读你的 `.py` 文件时，第一步就是把源码 parse 成 AST——`ast` 模块把这个过程暴露给了我们：

```python
# ast：Python 官方用 ast 模块来"读懂"你的源码
import ast

source = """
def add(a, b):
    return a + b
"""
tree = ast.parse(source)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        print("找到函数：", node.name, "参数：", [a.arg for a in node.args.args])
```

运行输出：

```
找到函数： add 参数： ['a', 'b']
```


### 5.3 Django 的 Q 对象（文字）

Django ORM 的 `Q` 对象用 `&`、`|` 组合查询条件（`Q(age__gt=18) & Q(city="北京")`），本质是一套"查询条件小语言"：`Q` 对象组成一棵条件树，最终被翻译成 SQL。SQL 本身又是一门语言，由数据库引擎解释执行——语言套语言，解释器套解释器。

---

## 6. 优缺点与适用场景

### 优点

- **灵活表达"语言"类需求**：规则、表达式、查询条件想怎么变就怎么变；
- **与组合模式天然契合**：树形结构 + 递归遍历，实现起来很自然。

### 缺点

- **实现成本高**：词法 + 语法 + 求值三套代码，还要处理各种边界情况；
- **类数量爆炸**：每种语法规则一个类，语言一复杂就失控；
- **性能开销**：解释执行比直接写逻辑慢；
- **Python 里大多有现成替代**：正则、`ast`、解析库，轮不到你自己写。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 表达式/规则/查询条件的 DSL | 简单配置（dict/JSON 就够） |
| 语法树需要多种处理（求值+优化+翻译） | 性能敏感的核心路径 |
| 教学与理解"语言原理" | 团队没人维护过解析器 |


---

## 7. 与其他模式的关系

- **解释器 + 组合**：语法树就是组合结构——叶子是终结符，树枝是非终结符；
- **解释器 + 访问者**：解释器构建语法树，访问者遍历语法树执行（见第 22 章）——编译器标配；
- **解释器 + 策略**：求值规则可以抽成策略，随时换一套算法；

---

## 8. 常见误区

### 误区 1：用 `eval` 处理用户输入（安全漏洞）

这是解释器主题下最危险的一个坑。`eval` 会把用户输入**当成 Python 代码执行**：

```python
# 误区：eval 用户输入 = 把服务器的钥匙交给陌生人
user_input = "__import__('os').getcwd()"   # 假设这是用户提交的"表达式"

result = eval(user_input)                  # 危险！用户输入被当成代码执行
print("用户输入被执行了，返回类型：", type(result).__name__)
```

运行输出：

```
用户输入被执行了，返回类型： str
```

`getcwd()` 只是读个目录，人畜无害；但换成 `__import__('os').system('rm -rf /')` 呢？**正确做法**：用 `ast.literal_eval`（只认字面量）或自写求值器（只允许白名单里的运算符，见 4.1）。

### 误区 2：用字符串切片"解析"表达式
### 误区 2：用字符串切片"解析"表达式

表达式是有结构的，字符串是扁平的。用 `split` 硬切，要么值太多拆不开（`"1+2+3"` 三个数装进两个变量直接 ValueError），要么卡在 `int('2*3')` 这种"半个数字"上——引子里的 `calc_v1` 已经演示过这两连翻车。**要处理"有结构"的文本，就老老实实走"词法 → 语法 → 求值"三步**，或者直接用 `ast`。

### 误区 3：把解释器用在不该用的地方

不是所有配置都值得造一门语言。普通配置就是数据，用 dict / JSON 就完了：

```python
# 误区：普通配置也上"DSL"——杀鸡用牛刀
# 反例：为"数据库地址"写一套词法+语法分析；正例：配置就是数据，用 dict 就完了
config = {
    "db_host": "127.0.0.1",
    "db_port": 3306,
    "timeout": 30,
}
print("数据库地址：", f"{config['db_host']}:{config['db_port']}")
```

运行输出：

```
数据库地址： 127.0.0.1:3306
```

判断标准：**如果配置里只有"数据"，用 dict；如果配置里有"逻辑"（条件、规则、表达式），才考虑 DSL**。把"数据"硬解释成"语言"，是解释器模式最常见的滥用。

---

## 9. 练习题

### 练习 1：用 `ast.NodeVisitor` 统计函数调用

写一个访问者，统计一段代码里所有被调用的函数名（`Call` 节点）：

```python
# 答案：统计代码里所有函数调用
import ast


class CallCounter(ast.NodeVisitor):
    def __init__(self):
        self.calls = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.append(node.func.id)
        self.generic_visit(node)


source = "print(len('abc')) + str(42)"
counter = CallCounter()
counter.visit(ast.parse(source))
print("函数调用：", counter.calls)
```

运行输出：

```
函数调用： ['print', 'len', 'str']
```

### 练习 2：给 `ast` 求值器支持一元负号

4.1 的 `MyEvaluator` 还不认识 `-x`。补上 `visit_UnaryOp`：

```python
# 答案：给 ast 求值器加上"一元负号"支持
import ast

class MyEvaluator(ast.NodeVisitor):
    def __init__(self, env: dict):
        self.env = env

    def visit_Constant(self, node):
        return node.value

    def visit_Name(self, node):
        return self.env[node.id]

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            return -operand
        if isinstance(node.op, ast.UAdd):
            return +operand
        raise ValueError("不支持的运算符")

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        raise ValueError("不支持的运算符")

ev = MyEvaluator({"x": 5})
print("-x + 3 =", ev.visit(ast.parse("-x + 3", mode="eval").body))
print("--x =", ev.visit(ast.parse("--x", mode="eval").body))
```

运行输出：

```
-x + 3 = -2
--x = 5
```

### 练习 3：写一个"指路 DSL"

把口语指令"向前 3 步 右转 向前 2 步 左转 向前 1 步"解释成坐标移动：

```python
# 答案：把"口语指路"解释成程序动作
def parse_directions(text: str) -> list:
    """词法+语法：'向前 N 步' / '左转' / '右转' → 指令列表"""
    commands = []
    words = text.split()
    i = 0
    while i < len(words):
        word = words[i]
        if word in ("左转", "右转"):
            commands.append((word, 0))
            i += 1
        elif word == "向前":
            commands.append(("向前", int(words[i + 1])))
            i += 2
        elif word == "步":
            i += 1
        else:
            raise ValueError(f"听不懂：{word}")
    return commands

def run(commands: list, start: tuple) -> tuple:
    """求值：按指令移动，返回终点坐标 (x, y)"""
    x, y = start
    direction = 0   # 0=北 1=东 2=南 3=西
    for cmd, arg in commands:
        if cmd == "左转":
            direction = (direction - 1) % 4
        elif cmd == "右转":
            direction = (direction + 1) % 4
        elif cmd == "向前":
            dx = [0, 1, 0, -1][direction]
            dy = [1, 0, -1, 0][direction]
            x += dx * arg
            y += dy * arg
    return (x, y)

text = "向前 3 步 右转 向前 2 步 左转 向前 1 步"
commands = parse_directions(text)
print("解析出的指令：", commands)
print("从 (0,0) 出发，终点：", run(commands, (0, 0)))
```

运行输出：

```
解析出的指令： [('向前', 3), ('右转', 0), ('向前', 2), ('左转', 0), ('向前', 1)]
从 (0,0) 出发，终点： (2, 4)
```

---

## 10. 小结与口诀

> **口诀：词法切词，语法建树，遍历求值；真要写解释器，先看 ast 库。**

解释器模式是"定义小语言 + 写程序解释它"的套路，三大步（词法 → 语法 → 求值）是所有语言处理的骨架。它是 GoF 23 个模式里最难、最不常用的一个——但理解了它，你就理解了正则、SQL、模板引擎乃至 Python 本身是怎么工作的。记住：**能用现成解释器就别自己写，必须自己写时，解析交给 `ast`，求值留给自己**。

至此，24 个模式全部讲完。下一章，也是全书最后一章——**结语：模式不是银弹**。学完了模式，更要知道什么时候不该用。

---

*本章金句：解释器模式提醒我们：每个领域都藏着一门小语言，就看你敢不敢把它写出来。*
