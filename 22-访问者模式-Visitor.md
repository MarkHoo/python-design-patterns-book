# 第 22 章 访问者模式（Visitor）

> **一句话总结**：数据结构不动，操作随便加——把"操作"做成访客。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 行为型 | ★★★★☆ | ★★☆☆☆ |

---

## 1. 引子：先讲个故事

你去医院体检，会发现一个巧妙的分工：**身体结构是你自己的，检查项目是医院的一套"标准动作"**。血常规抽血，心电图贴电极，B 超抹耦合剂——每个项目对着你的不同部位做不同的事。医院绝不会为了加一个"新体检项目"就让你重新长一遍器官；项目随便加，身体结构纹丝不动。

程序世界也一样：数据结构（表达式树、文件目录、账本）很稳定，但"对数据做的事"（求值、统计、出报表）三天两头变。最粗暴的写法是堆 `isinstance` 判断的"万能函数"——每加一种操作，就复制粘贴一条一模一样的判断链：

```python
# 引子：没有访问者的世界——isinstance 链到处复制粘贴
class Number:
    def __init__(self, value: int):
        self.value = value

class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

def evaluate(node) -> int:
    """求值：每加一种节点，这里就要加一个 elif"""
    if isinstance(node, Number):
        return node.value
    elif isinstance(node, Add):
        return evaluate(node.left) + evaluate(node.right)

def count_nodes(node) -> int:
    """统计节点数：又是一条一模一样的 isinstance 链！"""
    if isinstance(node, Number):
        return 1
    elif isinstance(node, Add):
        return 1 + count_nodes(node.left) + count_nodes(node.right)

expr = Add(Number(1), Add(Number(2), Number(3)))
print("求值结果：", evaluate(expr))
print("节点总数：", count_nodes(expr))
```

运行输出：

```
求值结果： 6
节点总数： 5
```

每新增一种节点类型（比如乘法），`evaluate`、`count_nodes` 全都要改一遍——改漏一个就是线上事故。**这就是开闭原则的十字路口**：结构（节点类型）和操作（求值/统计）都在变，到底锁死哪一头？访问者模式给出的答案是：**锁死结构，放开操作**。

---

## 2. 模式登场

### 定义

> **访问者模式**：在不修改数据结构的前提下，把"作用在结构上的操作"封装成独立的访问者对象。结构想稳就稳，操作想加就加。

### 解决的问题

1. **"往类里加方法"和"往操作里加类"的矛盾**：给每个节点加 `evaluate()`、`count()`、`to_string()`……节点类越来越臃肿，每次加操作还要改所有节点类（违背开闭原则）；
2. **相关操作分散**：一个操作（比如求值）的代码被拆散在各个节点类里，难以整体理解；
3. **跨节点累积状态**：统计"树里最大的数字"这类操作需要跨节点携带状态，塞在节点里很别扭。

### 双分派（double dispatch）

普通多态是**一次分派**：`obj.method()` 根据 `obj` 的类型选方法。访问者靠 `accept` + `visit` 实现**两次分派**：`expr.accept(visitor)` 先按元素类型找到 `Number.accept`（第一次分派），`accept` 里再调用 `visitor.visit_number(self)` 按访问者类型找到对应方法（第二次分派）。两个维度同时解耦，这就是访问者的核心机关。

### 结构

```
                  ┌──────────────────────────────┐
                  │           Visitor            │
                  │         （访问者接口）          │
                  ├──────────────────────────────┤
                  │ + visit_number(node)         │
                  │ + visit_add(node)            │
                  └──────────────────────────────┘
                        ▲                ▲
           ┌────────────┘                └────────────┐
   ┌───────────────────┐                  ┌───────────────────┐
   │    Evaluator      │                  │     Printer       │
   │   （求值访问者）    │                  │   （打印访问者）    │
   └───────────────────┘                  └───────────────────┘

       Element（元素接口）
   ┌──────────────────────────────┐
   │ + accept(visitor)            │
   └──────────────────────────────┘
        ▲          ▲
   ┌────────┐ ┌────────┐
   │ Number │ │  Add   │
   │accept()│ │accept()│
   └────────┘ └────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **Element（元素）** | 结构中的节点，提供 `accept(visitor)` 方法 |
| **ConcreteElement** | 具体节点（`Number`/`Add`…），`accept` 里调用 `visitor` 对应的 `visit` |
| **Visitor（访问者）** | 声明针对每种元素的 `visit` 方法；**ConcreteVisitor** 是具体操作（求值/打印/统计） |
| **客户端** | 拿着访问者，把它传给结构里的每个元素 |

---

## 3. Python 实现

### 3.1 经典版：表达式树 + 求值访问者

先建一棵"表达式树"，每个节点只做一件事：`accept` 访问者。求值逻辑全部收进 `Evaluator`——想再加"打印""统计深度"等操作？新建访问者类就行，元素类一行都不用动：

```python
# 经典访问者：表达式树（元素）+ 求值（访问者）
class Number:
    """数字节点：只有值，没有子节点"""

    def __init__(self, value: int):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_number(self)

class Add:
    """加法节点：左右各一个子表达式"""

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_add(self)

class Evaluator:
    """访问者：求值器"""

    def visit_number(self, node: Number) -> int:
        return node.value

    def visit_add(self, node: Add) -> int:
        return node.left.accept(self) + node.right.accept(self)

expr = Add(Number(1), Add(Number(2), Number(3)))
print("求值结果：", expr.accept(Evaluator()))
```

运行输出：

```
求值结果： 6
```

注意 `visit_add` 里的 `node.left.accept(self)`：加法节点自己不递归，而是**把求值权交还给访问者**——这就是双分派。以后想加"减法节点"？加一个元素类，再给访问者补一个 `visit_subtract` 即可。

### 3.2 文件目录统计版（带状态的访问者）

访问者可以**携带状态**跨节点累积——比如统计目录总大小、收集所有文件路径：

```python
# 访问者版目录统计：文件/文件夹共享 accept，访问者各自统计
class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def accept(self, visitor):
        return visitor.visit_file(self)

class Directory:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> "Directory":
        self.children.append(child)
        return self

    def accept(self, visitor):
        return visitor.visit_directory(self)

class SizeCounter:
    def visit_file(self, node: File) -> int:
        return node.size

    def visit_directory(self, node: Directory) -> int:
        return sum(child.accept(self) for child in node.children)

class FileLister:
    """带状态的访问者：收集文件路径"""

    def __init__(self):
        self.paths = []
        self._prefix = ""

    def visit_file(self, node: File) -> None:
        self.paths.append(self._prefix + node.name)

    def visit_directory(self, node: Directory) -> None:
        old = self._prefix
        self._prefix = old + node.name + "/"
        for child in node.children:
            child.accept(self)
        self._prefix = old

root = (Directory("项目")
        .add(File("README.md", 2))
        .add(Directory("src")
             .add(File("main.py", 50))
             .add(File("utils.py", 30))))

print("总大小：", root.accept(SizeCounter()), "KB")
lister = FileLister()
root.accept(lister)
print("文件列表：", lister.paths)
```

运行输出：

```
总大小： 82 KB
文件列表： ['项目/README.md', '项目/src/main.py', '项目/src/utils.py']
```

`FileLister` 把 `paths` 和 `_prefix` 当"随身行李"走一路记一路——遍历攒下的状态收在访问者兜里，而不是塞进结构类。

### 3.3 报表生成版：同一份账本，不同口径出不同报表

会计和税务对同一笔账的理解完全不同：会计眼里"收入减支出"是利润，税务眼里"收入全额计税、支出只有一半能抵扣"。账本结构不变，两套口径各写一个访问者：

```python
# 报表访问者：账本节点不变，会计/税务两套口径各自实现
class Income:
    def __init__(self, amount: float):
        self.amount = amount

    def accept(self, visitor):
        return visitor.visit_income(self)

class Expense:
    def __init__(self, amount: float):
        self.amount = amount

    def accept(self, visitor):
        return visitor.visit_expense(self)

class Accountant:
    """会计口径：收入减支出"""

    def visit_income(self, node: Income) -> float:
        return node.amount

    def visit_expense(self, node: Expense) -> float:
        return -node.amount

class TaxOfficer:
    """税务口径：收入全额计税，支出只有一半能抵扣"""

    def visit_income(self, node: Income) -> float:
        return node.amount

    def visit_expense(self, node: Expense) -> float:
        return -node.amount * 0.5

ledger = [Income(10000.0), Expense(3000.0)]
print("会计口径利润：", round(sum(e.accept(Accountant()) for e in ledger), 2))
print("税务口径税基：", round(sum(e.accept(TaxOfficer()) for e in ledger), 2))
```

运行输出：

```
会计口径利润： 7000.0
税务口径税基： 8500.0
```

以后要出"现金流报表"？再写一个访问者就行——**加口径不加账本，加操作不加结构**。

---

## 4. Python 特有玩法

### 4.1 `functools.singledispatch`：Python 版访问者

经典访问者要写 `accept` + `visit` 一整套。Python 里有个更轻的替代：`singledispatch` 按参数类型分派到不同函数——**天然就是"按类型分发操作"的访问者**，结构类零改动：

```python
# singledispatch：按参数类型分派到不同函数——天然就是"访问者"
from functools import singledispatch

class Number:
    def __init__(self, value: int):
        self.value = value

class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

@singledispatch
def evaluate(node):
    raise TypeError(f"不知道如何求值：{type(node).__name__}")

@evaluate.register
def _(node: Number) -> int:
    return node.value

@evaluate.register
def _(node: Add) -> int:
    return evaluate(node.left) + evaluate(node.right)

expr = Add(Number(1), Add(Number(2), Number(3)))
print("求值结果：", evaluate(expr))
```

运行输出：

```
求值结果： 6
```

`@evaluate.register` 后面函数签名里的类型注解（`node: Number`）告诉 singledispatch"这个分支管哪种类型"——分派表就是你的"访问者注册表"，想加"打印"？再注册一套函数就行。

### 4.2 `ast.NodeVisitor`：标准库内置的"访问者框架"

标准库的 `ast` 模块自带访问者基类 `NodeVisitor`：你只要重写 `visit_XXX` 方法，它负责遍历整棵语法树：

```python
# ast.NodeVisitor：标准库内置的"访问者框架"
import ast

class FunctionCounter(ast.NodeVisitor):
    """访问者：统计代码里的函数定义数量"""

    def __init__(self):
        self.count = 0

    def visit_FunctionDef(self, node):
        self.count += 1
        self.generic_visit(node)   # 继续往下遍历（函数里还能嵌套函数）

source = """
def greet(name):
    return "你好，" + name

def main():
    def inner(): pass

class Helper:
    def method(self): pass
"""

tree = ast.parse(source)
counter = FunctionCounter()
counter.visit(tree)
print("函数定义数量（含嵌套和类方法）：", counter.count)
```

运行输出：

```
函数定义数量（含嵌套和类方法）： 4
```

你只管写 `visit_FunctionDef`，遍历逻辑（`generic_visit` 递归进入子节点）由基类代劳——**AST 结构由 `ast` 模块定死，你的操作随便加**。

---

## 5. 真实世界中的它

### 5.1 `ast` 模块：NodeVisitor / NodeTransformer

`ast.NodeTransformer` 是 `NodeVisitor` 的"会改代码"版本——不只读，还能改写语法树。下面这个访问者把源码里所有数字字面量 +1：

```python
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
```

运行输出：

```
改写后的代码： price = 11 + 6
```

代码格式化工具（Black）、静态检查器（pyflakes）、代码转换工具（2to3）全是这个套路：用访问者遍历/改写 AST，语言本身的语法结构纹丝不动。

### 5.2 `functools.singledispatch`：标准库里的"操作分派"

`singledispatch` 在标准库和第三方库里到处可见（`dataclasses`、各种序列化器），本质就是"给不同类型的对象派发不同操作"：

```python
# singledispatch 的真实用例：给不同类型的对象做统一处理
from functools import singledispatch

@singledispatch
def describe(obj):
    return f"未知类型：{type(obj).__name__}"

@describe.register
def _(obj: int) -> str:
    return f"整数 {obj}，绝对值 {abs(obj)}"

@describe.register
def _(obj: str) -> str:
    return f"字符串 {obj!r}，长度 {len(obj)}"

@describe.register
def _(obj: list) -> str:
    return f"列表，共 {len(obj)} 个元素"

print(describe(42))
print(describe("访问者"))
print(describe([1, 2, 3]))
print(describe(1.5))
```

运行输出：

```
整数 42，绝对值 42
字符串 '访问者'，长度 3
列表，共 3 个元素
未知类型：float
```

### 5.3 pytest 插件体系（文字）

pytest 的插件机制与访问者神似：核心在测试运行的各个阶段（收集、setup、执行、报告）调用插件注册的 hook 函数（如 `pytest_collection_modifyitems`）。测试框架结构固定，插件（访问者）想加就加、想删就删。

---

## 6. 优缺点与适用场景

### 优点

- **开闭原则**：加操作（新访问者）不用改任何结构类；
- **相关操作集中**：一个访问者 = 一族相关操作，读代码一目了然；
- **状态累积**：访问者可以携带状态跨节点统计（目录大小、函数数量）。

### 缺点

- **对称的痛点**：加一种新结构类型，所有访问者都要跟着改——"结构稳定"是前提；
- **破坏封装**：访问者往往需要访问节点的内部数据；
- **结构偏重**：`accept` + `visit` 两套方法，小场景下是杀鸡用牛刀；
- **Python 有更轻的替代**：`singledispatch`、直接遍历、甚至一个函数都能搞定简单场景。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 结构稳定、操作频繁变（AST 分析、报表口径） | 结构本身经常变（对称爆炸） |
| 需要跨节点累积状态的统计类操作 | 只有一两种操作（直接写函数） |
| 编译器/解释器/静态分析工具 | 性能敏感的热路径（间接调用有开销） |

> **Python 圈的共识**：访问者模式在 Python 里"使用率低"是有原因的——`ast.NodeVisitor` 和 `singledispatch` 已覆盖 80% 的真实需求。手写一整套 `accept`/`visit` 之前，先想想能不能用这两个现成家伙。

---

## 7. 与其他模式的关系

- **访问者 + 迭代器**：迭代器管"怎么走"，访问者管"走到之后干什么"——遍历 + 操作分离；
- **访问者 + 解释器**：解释器构建语法树，访问者遍历语法树执行——编译器标配（见第 24 章）；
- **访问者 vs 策略**：策略是"换一种算法"，访问者是"换一整套操作"。

---

## 8. 常见误区

### 误区 1：改了结构，忘了同步访问者

新增节点类型时，如果只加了类、忘了给访问者加对应方法，错误会在**运行期**才暴露——Python 没有编译器帮你兜底：

```python
# 误区：新增节点类型，老访问者没有对应方法 → 运行期才炸
class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Evaluator:
    def visit_number(self, node) -> int:
        return node.value

    def visit_add(self, node) -> int:
        return node.left.accept(self) + node.right.accept(self)

expr = Multiply(Multiply(2, 3), 4)
try:
    print(expr.accept(Evaluator()))
except AttributeError as e:
    print("运行期才炸：", e)
```

运行输出：

```
运行期才炸： 'Multiply' object has no attribute 'accept'
```

**防御办法**：给访问者基类提供"通配"的默认 `visit`（抛 NotImplementedError 或记日志），或者给元素基类提供默认 `accept`——至少让错误早点、清楚点。

### 误区 2：Python 里过度使用访问者

访问者是为"操作很多、结构稳定"准备的。节点只有两三种、操作只有一两个？一个函数加 `isinstance` 就够了，何必 `accept`/`visit` 两套方法来回倒腾。判断标准很简单：**如果"加一个操作"只需要改一个函数，那访问者就是在给自己加戏**。反过来，结构天天变的话，访问者会让你每个访问者都跟着改，比不用还惨——两种情况下，访问者都不该出场。

### 误区 3：访问者携带太多状态，且复用对象

访问者带状态（如 `FileLister.paths`）是允许的，但**同一个访问者对象被遍历两次，状态会叠加**：

```python
# 误区：访问者对象复用导致状态叠加
class File:
    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_file(self)

class Collector:
    """收集文件名——注意它是有状态的"""

    def __init__(self):
        self.names = []

    def visit_file(self, node: File) -> None:
        self.names.append(node.name)

files = [File("a.txt"), File("b.txt")]
c = Collector()
for f in files:
    f.accept(c)
print("第一次收集：", c.names)

# 同一个访问者再遍历一次，结果叠加了
for f in files:
    f.accept(c)
print("第二次收集：", c.names, "← 重复了！")
```

运行输出：

```
第一次收集： ['a.txt', 'b.txt']
第二次收集： ['a.txt', 'b.txt', 'a.txt', 'b.txt'] ← 重复了！
```

**解决办法**：每次遍历前重置状态，或者干脆每次新建一个访问者（访问者通常很轻，新建无妨）。

---

## 9. 练习题

### 练习 1：用 `ast.NodeVisitor` 统计赋值语句

写一个访问者，统计一段代码里赋值语句（`Assign`）的数量：

```python
# 答案：继承 NodeVisitor，重写 visit_Assign
import ast

class AssignCounter(ast.NodeVisitor):
    def __init__(self):
        self.count = 0

    def visit_Assign(self, node):
        self.count += 1
        self.generic_visit(node)

source = """
x = 1
y = x + 2
z = y * 3
"""

counter = AssignCounter()
counter.visit(ast.parse(source))
print("赋值语句数量：", counter.count)
```

运行输出：

```
赋值语句数量： 3
```

### 练习 2：给表达式树加一个"找最大值"访问者

沿用 3.1 的表达式树（`Number`/`Add`），新增访问者求出树中最大的数字。注意：**元素类一行都不能改**：

```python
# 答案：新增访问者，元素类一行不动
class Number:
    def __init__(self, value: int):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_number(self)

class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_add(self)

class MaxFinder:
    def visit_number(self, node: Number) -> int:
        return node.value

    def visit_add(self, node: Add) -> int:
        return max(node.left.accept(self), node.right.accept(self))

expr = Add(Number(7), Add(Number(3), Number(9)))
print("最大数字：", expr.accept(MaxFinder()))
```

运行输出：

```
最大数字： 9
```

### 练习 3：用 `singledispatch` 重写 `isinstance` 链

把"根据形状算面积"的 `if/elif` 链重写成 `singledispatch` 版本：

```python
# 答案：singledispatch 按类型分派，代替手写 isinstance 链
from functools import singledispatch

@singledispatch
def area(shape):
    raise TypeError(f"不支持的形状：{type(shape).__name__}")

class Circle:
    def __init__(self, r: float):
        self.r = r

class Rect:
    def __init__(self, w: float, h: float):
        self.w = w
        self.h = h

@area.register
def _(shape: Circle) -> float:
    return 3.14 * shape.r ** 2

@area.register
def _(shape: Rect) -> float:
    return shape.w * shape.h

print("圆面积：", round(area(Circle(2)), 2))
print("矩形面积：", area(Rect(3, 4)))
```

运行输出：

```
圆面积： 12.56
矩形面积： 12
```

---

## 10. 小结与口诀

> **口诀：结构不动操作加，accept 请来访问者；Python 里想偷懒，singledispatch 顶上。**

访问者模式是"开闭原则的极端实践"：把结构锁死，把操作开放。但代价也不小——结构一旦变化，所有访问者集体返工。所以真实项目里，`ast.NodeVisitor` 和 `singledispatch` 往往比手写访问者更实用。

下一章，我们从"结构不动"转向"数据太多"——**享元模式**：重复的东西别反复造，共享一份。

---

*本章金句：访问者把"操作"做成访客——数据结构闭门谢客，访客却可以络绎不绝。*
