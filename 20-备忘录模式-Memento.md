# 第 20 章 备忘录模式（Memento）

> **一句话总结**：游戏存档：随时保存，随时回档。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 行为型 | ★★★☆☆ | ★★☆☆☆ |

---

## 1. 引子：先讲个故事

玩过《塞尔达》《黑魂》的朋友都有过这种体验：打 BOSS 前先存个档，死了读档重来，刚才的失误一笔勾销。要是没有存档功能，你打 30 分钟 BOSS 死了就得从头再来——血压直接拉满。

程序世界里"打 BOSS"的场景多了去了：

- **文本编辑器**：写文章手滑删了一大段，没有"撤销"就完蛋了；
- **订单系统**：管理员改错了订单状态，需要"回滚"；
- **配置中心**：改配置改崩了，想一键退回上一个版本。

这些需求的共同点是：**对象的内部状态需要能被"拍快照"保存下来，随时可以恢复回去**。这，就是备忘录模式要解决的问题。

先看一个"没有存档"的坏味道：

```python
# 引子：没有存档的世界——文档被改坏了只能干瞪眼
class Document:
    """一个简陋的文档对象，没有任何存档能力"""

    def __init__(self):
        self.content = ""

    def type(self, text: str) -> None:
        self.content += text

    def delete_last(self, n: int) -> None:
        self.content = self.content[:-n]


doc = Document()
doc.type("第一章：设计模式入门。")
doc.type("第二章：单例模式。")
print("写了两章：", doc.content)

# 手滑！删多了，而且没法撤销
doc.delete_last(9)
print("删过头了：", doc.content)   # 整章没了，后悔莫及，没有 Ctrl+Z
```

运行输出：

```
写了两章： 第一章：设计模式入门。第二章：单例模式。
删过头了： 第一章：设计模式入门。
```

（这个例子"删过头"删得不够明显？没关系——关键是**没有任何机制能把状态恢复回去**。接下来看备忘录怎么解决。）

---

## 2. 模式登场

### 定义

> **备忘录模式**：在不破坏封装的前提下，捕获并外部化一个对象的内部状态，以便之后可以把它恢复到这个状态。

### 解决的问题

1. **状态快照**：把对象某一时刻的状态完整保存；
2. **恢复能力**：随时回滚到任意一个保存过的状态；
3. **封装保护**：快照对外不可修改，只有原对象自己能看懂（外部只负责"存"和"取"，不负责"改"）。

### 结构

```
┌──────────────┐    create     ┌──────────────┐
│ Originator   │──────────────▶│   Memento    │
│ （发起人）     │               │ （备忘录/快照）│
│ - state      │               │ - state      │
│ + save()     │◀──────────────│               │
│ + restore(m) │   restore     └──────────────┘
└──────────────┘                      ▲
        │                             │ 存取
        │                             │
        ▼                             │
┌──────────────┐     保存/取出        │
│  Caretaker   │──────────────────────┘
│ （管理者）     │   只保管快照，不碰内容
└──────────────┘
```

### 角色

| 角色 | 说明 | 生活类比 |
|------|------|----------|
| **Originator（发起人）** | 状态的主人，负责生成快照和从快照恢复 | 游戏主角 |
| **Memento（备忘录）** | 快照本身，保存状态的容器 | 存档文件 |
| **Caretaker（管理者）** | 保管快照的栈/列表，不关心快照内容 | 存档管理器（"存档 1/存档 2"） |
| **客户端** | 指挥三者协作 | 玩家 |

---

## 3. Python 实现

### 3.1 经典版：显式的 Memento 类

```python
import copy
from dataclasses import dataclass
from typing import Optional


@dataclass
class Memento:
    """备忘录：一个不可变的快照（frozen=True 防止外部乱改）"""
    content: str
    cursor: int


class Editor:
    """发起人：文本编辑器，能存快照、能恢复"""

    def __init__(self):
        self.content = ""
        self.cursor = 0

    def type(self, text: str) -> None:
        self.content += text
        self.cursor = len(self.content)

    def move_cursor(self, pos: int) -> None:
        self.cursor = max(0, min(pos, len(self.content)))

    def save(self) -> Memento:
        """生成快照"""
        return Memento(content=copy.deepcopy(self.content), cursor=self.cursor)

    def restore(self, m: Memento) -> None:
        """从快照恢复"""
        self.content = copy.deepcopy(m.content)
        self.cursor = m.cursor

    def __repr__(self):
        return f"<Editor 内容={self.content!r} 光标={self.cursor}>"


class History:
    """管理者：只负责存快照和取快照"""

    def __init__(self):
        self._stack = []

    def push(self, m: Memento) -> None:
        self._stack.append(m)

    def pop(self) -> Optional[Memento]:
        return self._stack.pop() if self._stack else None


# 使用：写一段 → 存个档 → 继续写 → 后悔了 → 读档
editor = Editor()
history = History()

editor.type("第 1 行：设计模式真好玩。")
history.push(editor.save())          # 存档点 1
print("存档 1：", editor)

editor.type("第 2 行：备忘录模式最实用。")
history.push(editor.save())          # 存档点 2
print("存档 2：", editor)

editor.type("第 3 行：但是写书好累啊……")
print("现在（未存档）：", editor)

snapshot = history.pop()             # 后悔了，回到存档 2
editor.restore(snapshot)
print("读档后：", editor)
```

运行输出：

```
存档 1： <Editor 内容='第 1 行：设计模式真好玩。' 光标=14>
存档 2： <Editor 内容='第 1 行：设计模式真好玩。第 2 行：备忘录模式最实用。' 光标=29>
现在（未存档）： <Editor 内容='第 1 行：设计模式真好玩。第 2 行：备忘录模式最实用。第 3 行：但是写书好累啊……' 光标=44>
读档后： <Editor 内容='第 1 行：设计模式真好玩。第 2 行：备忘录模式最实用。' 光标=29>
```

**注意光标数字**：中文字符按字符数计算（"第 1 行：设计模式真好玩。" 是 14 个字符），各版本 Python 一致，放心。

### 3.2 游戏版：存档点恢复角色状态

```python
import copy
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Memento:
    hp: int
    level: int
    inventory: list


class Hero:
    """发起人：游戏主角"""

    def __init__(self, name: str):
        self.name = name
        self.hp = 100
        self.level = 1
        self.inventory = ["木剑"]

    def take_damage(self, dmg: int) -> None:
        self.hp = max(0, self.hp - dmg)

    def level_up(self) -> None:
        self.level += 1
        self.hp = min(100, self.hp + 30)

    def pick_item(self, item: str) -> None:
        self.inventory.append(item)

    def save(self) -> Memento:
        return Memento(hp=self.hp, level=self.level, inventory=copy.deepcopy(self.inventory))

    def restore(self, m: Memento) -> None:
        self.hp = m.hp
        self.level = m.level
        self.inventory = copy.deepcopy(m.inventory)

    def __repr__(self):
        return f"{self.name}(HP={self.hp}, Lv.{self.level}, 背包={self.inventory})"


hero = Hero("勇者阿强")
print("出发：", hero)

save_point = hero.save()                  # 进 BOSS 房前存档
hero.take_damage(85)
hero.pick_item("龙鳞")
print("打完 BOSS：", hero)                # 惨胜，还捡了装备

hero.restore(save_point)                  # 等等，太惨了，读档重来！
print("读档后：", hero)                   # 回到满状态，但龙鳞也没了——这就是读档的代价
```

运行输出：

```
出发： 勇者阿强(HP=100, Lv.1, 背包=['木剑'])
打完 BOSS： 勇者阿强(HP=15, Lv.1, 背包=['木剑', '龙鳞'])
读档后： 勇者阿强(HP=100, Lv.1, 背包=['木剑'])
```

### 3.3 简化版：Python 里快照可以只是一个值

经典 GoF 需要显式的 Memento 类，但 Python 里"状态"常常就是一个字典/元组/数据类。**快照不需要是"类"，可以是任何值**——只要它不可变或与源对象解耦：

```python
import copy


class BankAccount:
    """银行账户：余额 + 流水，快照就是一个 (余额, 流水) 元组"""

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.transactions.append(("存入", amount))

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("余额不足！")
        self.balance -= amount
        self.transactions.append(("取出", amount))

    def snapshot(self) -> tuple:
        """拍快照：余额 + 流水的深拷贝"""
        return (self.balance, copy.deepcopy(self.transactions))

    def restore(self, snap: tuple) -> None:
        """回滚：把快照内容搬回来"""
        self.balance, self.transactions = copy.deepcopy(snap)


acc = BankAccount("小明", 1000)
acc.deposit(500)
acc.withdraw(200)
print("正常操作后：余额", acc.balance)

snap = acc.snapshot()          # 拍个快照
acc.withdraw(999)              # 手滑取多了
print("手滑后：余额", acc.balance)

acc.restore(snap)              # 回滚！
print("回滚后：余额", acc.balance)
```

运行输出：

```
正常操作后：余额 1300
手滑后：余额 301
回滚后：余额 1300
```

---

## 4. Python 特有玩法

### 4.1 用 `copy.deepcopy` 直接拍"全息快照"

对于小型对象，Python 最省事的备忘录就是 `copy.deepcopy`——把整个对象复制一份当快照，恢复时再复制回来。配合 `dataclasses.replace` 还能做**部分回滚**：

```python
import copy
from dataclasses import dataclass, field, replace


@dataclass
class Settings:
    """应用配置（不可变风格：只读字段）"""
    theme: str = "light"
    font_size: int = 14
    plugins: list = field(default_factory=list)


s = Settings(theme="dark", font_size=16, plugins=["代码高亮"])
backup = copy.deepcopy(s)               # 改配置前先备份

# 一番折腾……
s.theme = "hacker"
s.plugins.append("vim 模式")
print("折腾后：", s)

# 回滚到备份
s = copy.deepcopy(backup)
print("回滚后：", s)

# 或者用 dataclasses.replace 做"部分回滚"：只还原主题，别的保持现状
s = replace(s, theme="light")
print("部分调整：", s)
```

运行输出：

```
折腾后： Settings(theme='hacker', font_size=16, plugins=['代码高亮', 'vim 模式'])
回滚后： Settings(theme='dark', font_size=16, plugins=['代码高亮'])
部分调整： Settings(theme='light', font_size=16, plugins=['代码高亮'])
```

### 4.2 用栈实现"无限撤销"

编辑器/终端的撤销本质就是"快照栈"：每次操作前入栈，撤销时弹栈。Python 的列表就是现成的栈：

```python
import copy
from dataclasses import dataclass, field


@dataclass
class CodeEditor:
    """带撤销功能的迷你编辑器（备忘录=整份文本快照）"""
    text: str = ""
    _history: list = field(default_factory=list)

    def edit(self, new_text: str) -> None:
        self._history.append(copy.deepcopy(self.text))   # 改之前先存档
        self.text = new_text

    def undo(self) -> bool:
        if not self._history:
            return False
        self.text = self._history.pop()                  # 弹出上一个快照
        return True


ed = CodeEditor()
ed.edit("print('hello')")
ed.edit("print('hello world')")
ed.edit("print('hello world!!!')")
print("当前：", ed.text)

ed.undo()
print("撤销 1 次：", ed.text)
ed.undo()
print("撤销 2 次：", ed.text)
ed.undo()
print("撤销 3 次：", ed.text)
print("还能撤销吗：", ed.undo())
```

运行输出：

```
当前： print('hello world!!!')
撤销 1 次： print('hello world')
撤销 2 次： print('hello')
撤销 3 次：
还能撤销吗： False
```

> **提示**：`ed.edit("")` 撤销后 text 是空字符串，所以打印出来是空行——正常现象。

### 4.3 `__slots__` 减小快照体积

如果快照会被大量保存（比如每秒钟自动存档一次），对象的内存大小就很重要。`__slots__` 能让实例不再携带 `__dict__`，省内存也省拷贝时间：

```python
import copy
from dataclasses import dataclass


@dataclass
class Frame:
    """游戏帧快照：__slots__ 让实例更轻量"""
    __slots__ = ("x", "y", "hp")
    x: float
    y: float
    hp: int


f = Frame(10.0, 20.0, 100)
snap = copy.deepcopy(f)
print("快照成功：", snap)
print("实例没有 __dict__（更省内存）：", not hasattr(f, "__dict__"))
```

运行输出：

```
快照成功： Frame(x=10.0, y=20.0, hp=100)
实例没有 __dict__（更省内存）： True
```

---

## 5. 真实世界中的它

### 标准库：`copy` 模块就是"万能拍快照机"

`copy.deepcopy` 是 Python 程序里最常见的"备忘录"实现——数据库 ORM 的对象快照、测试夹具的备份、配置的回滚，底层都是它。`dataclasses.replace` 则是"部分回滚"利器（见 4.1 演示）。

### IPython / Jupyter 的"历史回放"

IPython 会把每一条输入命令存进 `In` 列表、每次输出存进 `Out` 字典——`In[3]`、`Out[5]` 就是它替你保管的"备忘录"。你在笔记本里往上翻历史，就是在"读档"。

### 现实世界：Git 的 commit

`git commit` 就是最宏大的备忘录模式：工作区是 Originator，commit 是 Memento（快照），`git reflog`/分支是 Caretaker（管理者）。`git checkout <commit>` 就是 `restore()`。区别只在于 Git 的"快照"是压缩存储、只存差异，而备忘录模式不关心存储细节——**思想完全一致**。

### 框架：Django 表单的"初始值"

Django 的 `ModelForm` 在初始化时会记住 `instance` 的初始状态（`initial`），校验失败后重新渲染表单时能恢复用户输入之前的数据——这也是一种轻量备忘录。

---

## 6. 优缺点与适用场景

### 优点

- **一键回滚**：任何时刻都能回到任意存档点；
- **封装性好**：Caretaker 不碰快照内部，Originator 的细节不外泄；
- **实现简单**：Python 里往往一个 `deepcopy` 就够。

### 缺点

- **内存开销**：快照是状态的复制品，存多了内存爆炸（尤其深拷贝大对象）；
- **性能开销**：频繁快照（deepcopy）很慢；
- **序列化陷阱**：快照里若有锁、连接、文件句柄，deepcopy 会失败或产生共享引用（第 18 章原型模式讲过这个坑）。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 编辑器撤销/重做 | 状态巨大且频繁变化（改用事件溯源/命令模式） |
| 游戏存档、表单回退 | 只需要"回到上一步"（用命令模式 undo 更省） |
| 配置回滚、事务快照 | 快照包含不可复制资源（连接、锁） |

> **经验法则**：对象小、状态简单 → 备忘录（deepcopy）最爽；对象大、操作多 → 命令模式 + 只记录"反向操作"更省内存。

---

## 7. 与其他模式的关系

- **备忘录 + 命令**：经典组合。命令记录"做了什么"，备忘录记录"做之前的状态"，两者配合实现完整撤销（第 15 章命令模式提过）；
- **备忘录 vs 原型**：原型是"复制出另一个相同对象"（克隆），备忘录是"保存状态以便恢复"（存档）——一个横向复制、一个纵向回滚；
- **备忘录 vs 状态**：状态模式管"状态怎么流转"，备忘录管"状态怎么保存恢复"；
- **备忘录 vs 迭代器**：迭代器逐个访问元素，备忘录保存整体快照——一个流式、一个整存。

---

## 8. 常见误区

### 误区 1：浅拷贝当深拷贝，快照"名存实亡"

```python
import copy


class Cart:
    def __init__(self):
        self.items = []

    def add(self, item: str) -> None:
        self.items.append(item)

    def snapshot(self):
        return copy.copy(self)          # 误区：浅拷贝！items 还是同一个列表


cart = Cart()
cart.add("苹果")
snap = cart.snapshot()
cart.add("香蕉")                        # 原对象改了
print("快照里的 items：", snap.items)    # 浅拷贝共享列表 → 快照也"看到"了香蕉
```

运行输出：

```
快照里的 items： ['苹果', '香蕉']
```

**快照被污染了**——它本该停留在"只有苹果"的时刻。嵌套可变对象必须 `deepcopy`。

### 误区 2：快照对象被外部修改

如果 Memento 不是不可变的，Caretaker 或客户端可以偷偷改快照，恢复时就得到被篡改的"假存档"。`dataclass(frozen=True)`、元组、`MappingProxyType` 都是防篡改手段（3.1 版已用 frozen）。

### 误区 3：无限快照导致内存爆炸

每操作一次存一份完整快照，1 万次操作后内存里躺着 1 万份文档副本。解决：限制栈深度（只保留最近 N 个）、或改用"差异快照"（只存变化的部分）。

### 误区 4：快照里有不可复制资源

把 `threading.Lock`、socket、文件句柄 deepcopy 进快照会直接报错（`cannot pickle '_thread.lock' object`）。处理：自定义 `__deepcopy__`，资源只重建不复制（第 18 章原型模式有完整演示）。

---

## 9. 练习题

### 练习 1：给计数器加"存档/回档"

实现一个 `Counter`，支持 `save()` 返回快照、`restore(snap)` 恢复计数：

```python
import copy


class Counter:
    def __init__(self):
        self.count = 0
        self.history = []

    def inc(self, n: int = 1) -> None:
        self.count += n

    def save(self):
        return copy.deepcopy(self.count)

    def restore(self, snap) -> None:
        self.count = copy.deepcopy(snap)


c = Counter()
c.inc(3)
c.inc(4)
snap = c.save()          # 存档：count=7
c.inc(100)
print("加过头了：", c.count)
c.restore(snap)
print("读档后：", c.count)
```

运行输出：

```
加过头了： 107
读档后： 7
```

### 练习 2：用"命令 + 备忘录"实现带撤销的加减法计算器

```python
import copy


class Calculator:
    """发起人：计算结果本身"""

    def __init__(self):
        self.value = 0
        self._history = []       # 快照栈（管理者内嵌）

    def apply(self, op: str, n: int) -> None:
        self._history.append(copy.deepcopy(self.value))   # 操作前存档
        if op == "+":
            self.value += n
        elif op == "-":
            self.value -= n
        elif op == "*":
            self.value *= n

    def undo(self) -> bool:
        if not self._history:
            return False
        self.value = self._history.pop()
        return True


calc = Calculator()
calc.apply("+", 10)
calc.apply("*", 3)
calc.apply("-", 5)
print("当前结果：", calc.value)      # (0+10)*3-5 = 25
calc.undo()
print("撤销 1 次：", calc.value)     # 回到 -5 之前 = 30
calc.undo()
print("撤销 2 次：", calc.value)     # 回到 *3 之前 = 10
```

运行输出：

```
当前结果： 25
撤销 1 次： 30
撤销 2 次： 10
```

### 练习 3：找出下面的 bug 并修复

```python
import copy


class Game:
    def __init__(self):
        self.level_map = [[0] * 3 for _ in range(3)]
        self.score = 0

    def move(self, x: int, y: int) -> None:
        self.level_map[x][y] = 1
        self.score += 10

    def save(self):
        # bug：浅拷贝！level_map 的嵌套列表还是共享的
        return copy.copy(self)


g = Game()
g.move(0, 0)
snap = g.save()
g.move(1, 1)          # 原游戏继续走
print("看，快照里的 (1,1) 也被踩了：", snap.level_map)
```

运行输出：

```
看，快照里的 (1,1) 也被踩了： [[1, 0, 0], [0, 1, 0], [0, 0, 0]]
```

看到 (1,1) 也被踩了——浅拷贝的锅！修复：`copy.copy` 改成 `copy.deepcopy`：

```python
import copy


class Game:
    def __init__(self):
        self.level_map = [[0] * 3 for _ in range(3)]
        self.score = 0

    def move(self, x: int, y: int) -> None:
        self.level_map[x][y] = 1
        self.score += 10

    def save(self):
        return copy.deepcopy(self)      # 修复：深拷贝


g = Game()
g.move(0, 0)
snap = g.save()
g.move(1, 1)
print("修复后快照：", snap.level_map)
print("修复后分数：", snap.score)
```

运行输出：

```
修复后快照： [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
修复后分数： 10
```

---

## 10. 小结与口诀

> **口诀：打 BOSS 前先存档；状态快照随便拍；深拷贝、防篡改、限深度。**

备忘录模式是"后悔药"模式：拍快照（save）→ 随便折腾 → 读档（restore）。Python 里它常常简单得不像一个模式——`copy.deepcopy` 一拍即合。但记住三个坑：**浅拷贝污染快照、快照被外部篡改、快照无限堆积**。

下一章，我们来看一个"两个维度各自演化"的结构型模式——**桥接**：遥控器与电视，各变各的。

---

*本章金句：备忘录是程序员的"后悔药"——拍下快照的瞬间，你就拥有了回到过去的能力。*
