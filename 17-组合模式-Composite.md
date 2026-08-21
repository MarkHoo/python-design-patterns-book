# 第 17 章 组合模式（Composite）

> **一句话总结**：树形结构，叶子与容器一视同仁。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 结构型 | ★★★☆☆ | ★★★☆☆ |

---

## 1. 引子：先讲个故事

你的电脑里全是文件夹套文件夹 📁：`工作` 文件夹里有个 `文档` 文件夹，`文档` 里躺着几个文件。有意思的是：**双击文件夹能"打开"，双击文件也能"打开"**——对用户来说，文件夹和文件在"打开"这件事上毫无区别，根本不需要知道它俩是两种东西。

程序里就惨了。很多人写菜单、写文件系统时，把"文件"和"文件夹"当成两套完全独立的对象，调用方被迫用 `isinstance` 区分类型，每加一种新节点（快捷方式、压缩包）就要改一遍调用方的代码：

```python
# 引子：没有组合的世界——文件和文件夹分开处理，调用方要判类型
class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def open(self):
        print(f"打开文件：{self.name}（{self.size} KB）")


class Folder:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def open(self):
        print(f"打开文件夹：{self.name}（{len(self.children)} 个条目）")


def show(node) -> None:
    # 调用方被迫区分类型——加新类型（快捷方式、压缩包）就要改这里
    if isinstance(node, File):
        node.open()
    elif isinstance(node, Folder):
        print(f"进入文件夹 {node.name}")
        for child in node.children:
            show(child)


root = Folder("工作")
docs = Folder("文档")
docs.add(File("需求.md", 12))
docs.add(File("设计.md", 45))
root.add(docs)
root.add(File("README.txt", 3))
show(root)
```

运行输出：

```
进入文件夹 工作
进入文件夹 文档
打开文件：需求.md（12 KB）
打开文件：设计.md（45 KB）
打开文件：README.txt（3 KB）
```

这段代码有两个毛病：

1. **调用方知道太多**：`show` 必须区分叶子（文件）和容器（文件夹），加新节点类型就得改它；
2. **"打开"被拆成两套**：双击文件夹和双击文件明明是同一个动作，却散在两处实现。

**组合模式**的思路：给文件和文件夹一个**统一接口**，让客户端只跟"节点"打交道——你不需要知道它是叶子还是容器，反正它都能"打开"、都能被递归处理。

---

## 2. 模式登场

### 定义

> **组合模式**：将对象组合成树形结构以表示"部分-整体"的层次结构，让客户端对单个对象（叶子）和组合对象（容器）的使用具有一致性。

### 解决的问题

1. **客户端零判断**：不再需要区分"单个"还是"整体"，统一按节点处理；
2. **天然递归**：容器把自己的操作递归转给子节点，深层嵌套也不怕；
3. **易扩展**：新增一种节点类型，客户端代码一行不用改。

### 结构

```
                    ┌─────────────────────────┐
                    │  Component（组件接口）    │
                    ├─────────────────────────┤
                    │ + open()                │
                    │ + size()                │
                    └────────────┬────────────┘
                      ▲          ▲
         ┌────────────┘          └────────────┐
   ┌─────┴───────┐                     ┌──────┴─────┐
   │    Leaf     │                     │ Composite  │
   │  （叶子）     │                     │  （容器）    │
   │  文件/菜单项  │                     │ 文件夹/菜单  │
   └─────────────┘                     │ - children  │
                                       └────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **Component** | 统一接口：叶子与容器共有的操作（open、size） |
| **Leaf（叶子）** | 没有子节点，实现最基础的行为（文件、菜单项） |
| **Composite（容器）** | 包含子节点，把操作递归转发给孩子们（文件夹、菜单） |
| **客户端** | 只认 Component，不区分叶子还是容器 |

---

## 3. Python 实现

### 3.1 经典版：文件系统

先看最经典的文件系统例子。关键设计：所有节点都有 `children`（叶子返回空），所有节点都有 `open()` 和 `size()`——客户端处理任何节点都不用判断类型：

```python
class FileNode:
    """组件接口：叶子（文件）和容器（文件夹）的统一接口"""

    @property
    def children(self):
        """默认没有子节点——叶子返回空，容器返回子节点列表"""
        return ()

    def open(self) -> str:
        raise NotImplementedError

    def add(self, child) -> None:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError


class File(FileNode):
    """叶子：文件"""

    def __init__(self, name: str, size: int):
        self.name = name
        self._size = size

    def open(self) -> str:
        return f"打开文件 {self.name}（{self._size} KB）"

    def add(self, child) -> None:
        raise ValueError("文件不能包含子节点")

    def size(self) -> int:
        return self._size


class Folder(FileNode):
    """容器：文件夹"""

    def __init__(self, name: str):
        self.name = name
        self._children = []

    @property
    def children(self):
        return self._children

    def open(self) -> str:
        return f"打开文件夹 {self.name}（{len(self._children)} 个条目）"

    def add(self, child) -> None:
        self._children.append(child)

    def size(self) -> int:
        return sum(child.size() for child in self._children)   # 递归求总大小


def print_tree(node: FileNode, indent: str = "") -> None:
    """客户端只认 FileNode：叶子与容器一视同仁，零类型判断"""
    print(indent + node.open())
    for child in node.children:
        print_tree(child, indent + "  ")


root = Folder("工作")
docs = Folder("文档")
docs.add(File("需求.md", 12))
docs.add(File("设计.md", 45))
root.add(docs)
root.add(File("README.txt", 3))

print_tree(root)
print("整个工作目录总大小:", root.size(), "KB")
```

运行输出：

```
打开文件夹 工作（2 个条目）
  打开文件夹 文档（2 个条目）
    打开文件 需求.md（12 KB）
    打开文件 设计.md（45 KB）
  打开文件 README.txt（3 KB）
整个工作目录总大小: 60 KB
```

`root.size()` 一条调用，递归算到底——客户端完全不关心树有多深、节点是文件还是文件夹。

> **透明性 vs 安全性**：这里的 `File.add` 存在但抛异常，叫"透明性"风格——接口完全统一，代价是叶子被迫实现用不到的方法（违反接口隔离原则）。另一种"安全性"风格把 `add` 只放在容器上，叶子根本没有，但客户端就得用类型判断。Python 的鸭子类型给了第三种方案：叶子直接不写 `add`，靠 `children` 默认空元组维持统一接口（见 3.2、4.1），两边的好处都占一点。

### 3.2 菜单系统：菜单套菜单，菜单项是叶子

GUI 菜单是组合的另一个经典场景：菜单（容器）可以包含菜单项（叶子），也可以包含子菜单（容器）——递归渲染，一套代码通吃：

```python
class MenuItem:
    """叶子：可点击的菜单项"""

    def __init__(self, name: str, action: str):
        self.name = name
        self.action = action

    @property
    def children(self):
        return ()          # 叶子没有子项

    def render(self) -> list:
        return [f"- {self.name}（{self.action}）"]

    def click(self) -> str:
        return f"执行菜单项「{self.name}」：{self.action}"


class Menu:
    """容器：菜单可以包含菜单项，也可以包含子菜单"""

    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, item) -> None:
        self.children.append(item)

    def render(self) -> list:
        lines = [f"▸ {self.name}"]
        for child in self.children:
            lines.extend("  " + line for line in child.render())   # 递归
        return lines

    def click(self) -> str:
        return f"展开菜单「{self.name}」（{len(self.children)} 项）"


file_menu = Menu("文件")
file_menu.add(MenuItem("新建", "ctrl+n"))
file_menu.add(MenuItem("打开", "ctrl+o"))
edit_menu = Menu("编辑")
edit_menu.add(MenuItem("撤销", "ctrl+z"))
main_menu = Menu("主菜单")
main_menu.add(file_menu)
main_menu.add(edit_menu)

for line in main_menu.render():
    print(line)
print()
print(file_menu.children[0].click())
print(file_menu.click())
```

运行输出：

```
▸ 主菜单
  ▸ 文件
    - 新建（ctrl+n）
    - 打开（ctrl+o）
  ▸ 编辑
    - 撤销（ctrl+z）

执行菜单项「新建」：ctrl+n
展开菜单「文件」（2 项）
```

`render()` 里没有任何 `isinstance`——`MenuItem` 和 `Menu` 都提供 `children` 和 `render`，递归自然展开。

### 3.3 商品分类树：对整体和对部分一视同仁

电商的分类树（服装 → 男装/女装 → 具体商品）里，"某个分类的销量"是个高频需求。组合模式让"分类销量"和"商品销量"用同一个调用：

```python
class Category:
    """分类节点：叶子（具体商品）和容器（分类）的统一接口"""

    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return ()

    def sales(self) -> int:
        raise NotImplementedError


class Product(Category):
    """叶子：具体商品，自带销量"""

    def __init__(self, name: str, sales: int):
        super().__init__(name)
        self._sales = sales

    def sales(self) -> int:
        return self._sales


class CategoryNode(Category):
    """容器：分类，销量 = 所有子分类/商品销量之和"""

    def __init__(self, name: str):
        super().__init__(name)
        self._children = []

    @property
    def children(self):
        return self._children

    def add(self, child: Category) -> None:
        self._children.append(child)

    def sales(self) -> int:
        return sum(child.sales() for child in self._children)


root = CategoryNode("服装")
men = CategoryNode("男装")
men.add(Product("T恤", 120))
men.add(Product("牛仔裤", 80))
women = CategoryNode("女装")
women.add(Product("连衣裙", 300))
root.add(men)
root.add(women)

print("男装销量:", men.sales())
print("女装销量:", women.sales())
print("全站服装销量:", root.sales())     # 一条调用，递归算到底
```

运行输出：

```
男装销量: 200
女装销量: 300
全站服装销量: 500
```

---

## 4. Python 特有玩法

### 4.1 鸭子类型统一接口：不需要抽象基类

Python 里连抽象基类都可以省：只要"有 `children`、有 `size()`"，就是合格节点。`File` 和 `Folder` 没有任何血缘关系，照样组成树：

```python
class File:
    """叶子"""

    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return ()          # 叶子没有孩子

    def size(self) -> int:
        return 10          # 假设每个文件 10 KB


class Folder:
    """容器"""

    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def size(self) -> int:
        return sum(child.size() for child in self.children)


def total_size(node) -> int:
    """不需要类型判断，也不需要抽象基类——长得像节点就行"""
    return node.size()


root = Folder("项目")
root.add(File("a.py"))
root.add(File("b.py"))
print("总大小:", total_size(root), "KB")
print("单个文件大小:", total_size(File("c.py")), "KB")
```

运行输出：

```
总大小: 20 KB
单个文件大小: 10 KB
```

### 4.2 实现 `__iter__` / `__len__`：组合直接支持遍历

给容器实现 `__iter__` 和 `__len__`，组合对象就能像列表一样 `for` 和 `len`——Python 的迭代器协议（第 4 章）在这里直接派上用场：

```python
class File:
    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return ()

    def __iter__(self):
        return iter(())        # 叶子迭代 = 空

    def __len__(self):
        return 0


class Folder:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def __iter__(self):
        return iter(self.children)     # 迭代 = 遍历直接子节点

    def __len__(self):
        return len(self.children)


root = Folder("工作")
docs = Folder("文档")
docs.add(File("需求.md"))
docs.add(File("设计.md"))
root.add(docs)
root.add(File("README.txt"))

print("工作目录下条目数:", len(root))
print("文档目录下条目数:", len(docs))
for node in root:
    print("直接子节点:", node.name)
```

运行输出：

```
工作目录下条目数: 2
文档目录下条目数: 2
直接子节点: 文档
直接子节点: README.txt
```

### 4.3 递归函数处理树：生成器版深度遍历

用生成器 + `yield from` 写树的深度优先遍历，一行递归、处处可消费：

```python
class File:
    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return ()


class Folder:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)


def walk(node, depth: int = 0):
    """递归遍历：生成器版，产出 (节点, 深度)"""
    yield node, depth
    for child in node.children:
        yield from walk(child, depth + 1)


root = Folder("root")
src = Folder("src")
src.add(File("main.py"))
src.add(File("utils.py"))
root.add(src)
root.add(File("README.md"))

for node, depth in walk(root):
    print("  " * depth + node.name)
```

运行输出：

```
root
  src
    main.py
    utils.py
  README.md
```

---

## 5. 真实世界中的它

### 标准库：`xml.etree.ElementTree` —— Element 就是组合！

Python 标准库解析 XML 用的 `ElementTree`，其核心类 `Element` 就是组合模式的教科书实现：一个元素既可以只有文本（叶子），也可以包含子元素（容器），`find`、`iter`、`findall` 全是递归树操作：

```python
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
```

运行输出：

```
<catalog>
  <book id="1">
    <title>Python 设计模式修炼手册</title>
    <author>修炼者</author>
  </book>
  <book id="2">
    <title>Python 网络爬虫实战</title>
  </book>
</catalog>
书的数量: 2
发现书 id = 1
发现书 id = 2
第一本书的标题: Python 设计模式修炼手册
```

### GUI：tkinter 的控件树

tkinter 的窗口是一个天然的"控件树"：`Tk` 根窗口（容器）下挂着 `Frame`（容器），`Frame` 里再放 `Button`、`Label`（叶子）。布局管理器（`pack`、`grid`）递归地处理整个控件树——"重绘整个窗口"就是一次从根开始的组合遍历。

### 标准库：`pathlib` 的目录遍历

`pathlib.Path` 配合 `Path.rglob()`、`os.walk()` 做目录遍历时，背后也是组合思想：目录是容器、文件是叶子，`rglob("*.py")` 会递归钻进每一层子目录，找到所有匹配的叶子——你用的时候完全不用关心目录嵌套了几层。

---

## 6. 优缺点与适用场景

### 优点

- **客户端极简**：叶子与容器统一处理，零类型判断；
- **天然递归**：多深的嵌套都优雅应对；
- **易扩展**：新增节点类型，客户端和已有节点都不用改；
- **对整体和对部分一视同仁**：`root.size()` 和 `file.size()` 是同一个调用。

### 缺点

- **接口过度统一**：透明性风格下，叶子被迫实现用不到的方法（接口隔离的代价）；
- **递归有成本**：树很深时递归开销大，甚至栈溢出；
- **类型信息变弱**：难以在代码里直接区分"单个"和"整体"（Python 本就如此，问题不大）。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 文件系统、菜单、UI 控件树 | 结构基本是扁平的（只有一层） |
| 组织架构、商品分类等树形数据 | 节点类型行为差异巨大，硬套统一接口很别扭 |
| 需要"对整体和对部分一视同仁"的操作 | 只有两层且从不嵌套，组合纯属多余 |

---

## 7. 与其他模式的关系

- **与迭代器**：组合树常配迭代器遍历（第 4 章）——4.2 的 `__iter__` 就是活例子，`yield from` 递归展开整棵树。
- **与装饰器**：两者都是递归结构，但装饰器是"**单链**"（一层套一层，像洋葱），组合是"**树**"（一层套多个，像目录）。装饰器给节点加能力，组合把节点组织成整体。
- **与解释器**：解释器的语法树就是组合结构——表达式套表达式（第 24 章）。
- **与命令**：第 15 章的宏命令 `MacroCommand` 就是组合的应用——命令套命令，构成命令树。

---

## 8. 常见误区

### 误区 1：叶子实现了容器方法，但抛异常

"透明性"风格的代价：叶子被迫实现 `add`，然后抛异常。接口是统一了，但叶子背上了永远用不到的包袱（违反接口隔离原则），而且错误要等到**运行时**才暴露：

```python
class Node:
    def add(self, child) -> None:
        raise NotImplementedError


class File(Node):
    def __init__(self, name: str):
        self.name = name

    def add(self, child) -> None:
        raise NotImplementedError("文件不能有子节点！")


class Folder(Node):
    def __init__(self):
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)


# 接口统一了，但"文件"被迫实现一个永远用不上的方法
node = File("a.txt")
try:
    node.add(File("b.txt"))
except NotImplementedError as e:
    print("运行时才炸:", e)
```

运行输出：

```
运行时才炸: 文件不能有子节点！
```

> 缓解办法：Python 里通常不值得追求"绝对透明"——叶子直接不写 `add`，用 `children` 默认空元组维持统一接口（见 3.1、4.1），把用不到的方法从叶子上摘掉。

### 误区 2：递归遍历在叶子处翻车

遍历函数假设"所有节点都有 `children`"，但叶子如果没有 `children` 属性，递归就会在叶子处炸掉；树太深（超过默认递归上限约 1000 层）还会栈溢出（`RecursionError`）：

```python
# 反面教材：遍历假设所有节点都有 children，叶子没有就炸
class File:
    def __init__(self, name: str):
        self.name = name


class Folder:
    def __init__(self, name: str):
        self.name = name
        self.children = []


def walk(node, depth: int = 0) -> None:
    print("  " * depth + node.name)
    for child in node.children:          # File 没有 children → 炸
        walk(child, depth + 1)


root = Folder("root")
root.children.append(File("a.txt"))
try:
    walk(root)
except AttributeError as e:
    print("遍历在叶子处炸了:", e)
```

运行输出：

```
root
a.txt
遍历在叶子处炸了: 'File' object has no attribute 'children'
```

> 规矩：要么让叶子也有 `children`（返回空），要么遍历前用 `getattr(node, "children", ())` 兜底。树的深度也要心里有数——真出现上万层的树，就该考虑改成迭代式遍历了。

### 误区 3：在树里引入循环引用

把父节点加进自己的子节点，树就变成了环——递归遍历会永远转圈（等价于死循环）：

```python
class Node:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)


root = Node("root")
child = Node("child")
root.add(child)
child.add(root)          # 树变成了环！遍历会永远转圈


def walk(node, depth: int = 0) -> None:
    print("  " * depth + node.name)
    if depth >= 3:                       # 人为设个深度上限，模拟"发现不对劲"
        print("...还在循环（正常遍历早该结束了）")
        return
    for c in node.children:
        walk(c, depth + 1)


walk(root)
```

运行输出：

```
root
  child
    root
      child
...还在循环（正常遍历早该结束了）
```

> 真实项目里没人会给遍历加深度上限。防范手段：`add` 时拒绝把自己/祖先加进来，或者遍历时用 `id()` 集合记录访问过的节点，发现重复立即报错。

---

## 9. 练习题

### 练习 1：组织架构树，统计总人数

用组合模式实现"部门（容器）套员工（叶子）"，并统计任意一级的人数：

```python
# 答案：部门（容器）+ 员工（叶子），统一统计人数
class Employee:
    """叶子：员工"""

    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return ()

    def headcount(self) -> int:
        return 1


class Department:
    """容器：部门，人数 = 子部门 + 员工人数之和"""

    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def headcount(self) -> int:
        return sum(child.headcount() for child in self.children)


tech = Department("技术部")
backend = Department("后端组")
backend.add(Employee("小明"))
backend.add(Employee("小红"))
tech.add(backend)
tech.add(Employee("产品经理老王"))

print("后端组人数:", backend.headcount())
print("技术部总人数:", tech.headcount())
```

运行输出：

```
后端组人数: 2
技术部总人数: 3
```

### 练习 2：在树里递归查找节点

写一个 `find(node, name)`，深度优先查找，找到返回节点，找不到返回 `None`：

```python
# 答案：递归查找——先查自己，再查每个孩子
class File:
    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return ()


class Folder:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)


def find(node, name: str):
    if node.name == name:
        return node
    for child in node.children:
        result = find(child, name)
        if result is not None:
            return result
    return None


root = Folder("项目")
src = Folder("src")
src.add(File("main.py"))
root.add(src)
root.add(File("README.md"))

target = find(root, "main.py")
print("找到了:", target.name)
print("找不到的返回:", find(root, "不存在.py"))
```

运行输出：

```
找到了: main.py
找不到的返回: None
```

### 练习 3：让分类树支持 `for` 和 `len`

给商品分类树实现 `__iter__` / `__len__`，让"数码"分类能被直接遍历：

```python
# 答案：容器实现 __iter__/__len__，叶子返回空迭代
class Category:
    def __init__(self, name: str):
        self.name = name

    @property
    def price(self):
        return None          # 容器没有价格

    def __iter__(self):
        return iter(())      # 叶子：迭代为空

    def __len__(self):
        return 0


class Product(Category):
    def __init__(self, name: str, price: float):
        super().__init__(name)
        self._price = price

    @property
    def price(self):
        return self._price


class CategoryNode(Category):
    def __init__(self, name: str):
        super().__init__(name)
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)


digital = CategoryNode("数码")
digital.add(Product("手机", 4999))
digital.add(Product("耳机", 999))
digital.add(CategoryNode("配件"))

print("数码分类下有", len(digital), "个直接子分类/商品")
for item in digital:
    price = item.price
    suffix = f"（{price} 元）" if price is not None else "（子分类）"
    print(f" - {item.name}{suffix}")
```

运行输出：

```
数码分类下有 3 个直接子分类/商品
 - 手机（4999 元）
 - 耳机（999 元）
 - 配件（子分类）
```

---

## 10. 小结与口诀

> **口诀：树形结构一个样，叶子容器共接口；递归遍历走到底，别让节点变成环。**

组合模式是"树形结构"的万能解法：统一接口让客户端零判断，递归让深层嵌套举重若轻。三个记忆点：

1. **统一接口**：叶子有 `children`（空），容器有 `children`（列表），客户端不区分；
2. **递归到底**：容器的操作 = 孩子们的操作之和，`yield from` 让遍历一行搞定；
3. **防环防深**：别让节点指向祖先，别让叶子缺 `children`。

下一章，我们回到创建型模式——**原型模式**：复制粘贴，克隆对象。

---

*本章金句：组合模式让"部分"与"整体"共用一张脸——树有多深，调用方的心就有多定。*
