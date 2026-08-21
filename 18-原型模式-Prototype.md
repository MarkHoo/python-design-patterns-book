# 第 18 章 原型模式（Prototype）

> **一句话总结**：复制粘贴创建对象：克隆一个现成的，比从零造一个快。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 创建型 | ★★☆☆☆ | ★★☆☆☆ |

---

## 1. 引子：先讲个故事

生物课上老师说过，细胞分裂是最原始的"复制"：一个细胞一变二、二变四，每个新细胞都和母体一模一样，然后各自继续长大、各自演化。程序世界里也天天需要这种"复制粘贴"：游戏里刷一波小兵，总不能一个个手写构造函数；文档要做十个版本的方案，总不能把内容重新敲十遍。而现实中的复制，往往是这样的——每次要"再来一个"，就手动 new 一个对象，把字段抄一遍：

```python
# 引子：没有原型的世界——每次复制对象都手写一遍字段
class Soldier:
    def __init__(self, name, hp, weapons):
        self.name = name
        self.hp = hp
        self.weapons = weapons  # 武器列表


s1 = Soldier("列兵小强", 100, ["步枪", "手雷"])

# 复制一个士兵：手动 new + 手工抄字段（抄着抄着就漏了）
s2 = Soldier(s1.name, s1.hp, s1.weapons)

# 更糟的是：s2 和 s1 的 weapons 是同一个列表！
s2.weapons.append("急救包")
print("原版的武器：", s1.weapons)
print("复制品的武器：", s2.weapons)
```

运行输出：

```
原版的武器： ['步枪', '手雷', '急救包']
复制品的武器： ['步枪', '手雷', '急救包']
```

看出来了吗？手写复制有两个毛病：一是**累**——字段一多就抄漏，以后加个新字段，所有复制点都得跟着改；二是**险**——`weapons` 这个列表被两个对象共享了，给复制品加装备，原版也莫名其妙多了一把急救包。这就像你拿复印机复印了一份合同，结果发现两份合同共用同一支笔——改一份，另一份也跟着变。**原型模式**就是来解决这个问题的：让对象自己会"克隆"，复制时不用关心它内部有多少字段、嵌套多深。

---

## 2. 模式登场

### 定义

> **原型模式**：用"克隆一个现有对象"来代替"从零创建一个新对象"，客户端不关心具体类，只调用 `clone()`。

### 解决的问题

1. **创建成本高**：对象构造很贵（要连数据库、要算半天），复制一份现成的更快；
2. **创建细节多**：对象内部结构复杂（嵌套列表、字典、对象），手写复制容易漏、容易共享；
3. **客户端耦合**：客户端不想知道"要 new 哪个类"，只想说"照这个样子再来一个"。

### 结构

```
┌──────────────────────────┐
│        Prototype          │          ← 原型接口（约定 clone 行为）
├──────────────────────────┤
│ + clone()                 │
└──────────────────────────┘
        ▲
        │ 实现 clone()
┌──────────────────────────┐
│   ConcretePrototype       │          ← 具体原型（比如"标准士兵"）
├──────────────────────────┤
│ - 各种内部状态             │
├──────────────────────────┤
│ + clone()                 │  ← 返回自己的一份拷贝
└──────────────────────────┘
        ▲
        │ 只调用 clone()，不关心具体类
   ┌──────────┐
   │  客户端   │    （可选）原型注册表：登记多个原型，按名字克隆
   └──────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **Prototype（原型接口）** | 约定"能克隆自己"的统一入口（Python 里常省略，鸭子类型够用） |
| **ConcretePrototype（具体原型）** | 真正干活的对象，实现 `clone()` 返回自己的拷贝 |
| **客户端** | 拿着一个原型，随时 `clone()` 出新的，不关心具体类 |
| **原型注册表**（可选） | 一张"名字 → 原型"的表，按名字批量克隆（兼简单工厂职责） |

---

## 3. Python 实现

### 3.1 经典版：自己写 `clone()` 方法

经典写法是给类加一个 `clone()` 方法，内部"新建一个同类型的对象，把状态搬过去"。注意搬状态时要用 `copy.deepcopy` 处理嵌套结构，否则两个对象又会共享内部列表：

```python
import copy


class Enemy:
    """经典原型：敌人单位，clone() 返回一份独立拷贝"""
    def __init__(self, kind, hp, skills):
        self.kind = kind
        self.hp = hp
        self.skills = skills  # 技能列表（嵌套结构）
    def clone(self):
        # 新建同类型对象，deepcopy 复制 skills，避免两份共享列表
        return Enemy(self.kind, self.hp, copy.deepcopy(self.skills))
    def __repr__(self):
        return f"<Enemy {self.kind} hp={self.hp} skills={self.skills}>"


zombie = Enemy("僵尸", 50, ["撕咬", "感染"])
zombie2 = zombie.clone()

zombie2.hp = 80              # 给复制品加血量
zombie2.skills.append("自爆")  # 给复制品加技能

print("原版：", zombie)
print("复制品：", zombie2)
print("互不影响：", zombie.skills == ["撕咬", "感染"])
```

运行输出：

```
原版： <Enemy 僵尸 hp=50 skills=['撕咬', '感染']>
复制品： <Enemy 僵尸 hp=80 skills=['撕咬', '感染', '自爆']>
互不影响： True
```

### 3.2 游戏单位克隆：复制一个士兵再改属性

原型最经典的用法：**克隆 + 微调**。先造一个"标准步兵"当原型，刷兵时克隆一堆，再各自改属性——不用重复写构造函数，也不用重新初始化公共状态：

```python
import copy


class Unit:
    """游戏单位：克隆原型 + 改属性 = 快速造兵"""
    def __init__(self, name, hp, attack, buffs):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.buffs = buffs  # 身上挂的 buff 列表
    def clone(self):
        return copy.deepcopy(self)
    def __repr__(self):
        return f"<Unit {self.name} hp={self.hp} atk={self.attack} buffs={self.buffs}>"


# 先造一个"标准步兵"作为原型
infantry_prototype = Unit("步兵", 100, 10, ["士气+1"])

a = infantry_prototype.clone()
a.name = "精英步兵"
a.attack = 15

b = infantry_prototype.clone()
b.hp = 120

c = infantry_prototype.clone()

print(a)
print(b)
print(c)
print("三份互不影响（buff 列表各自独立）:", a.buffs is not b.buffs and b.buffs is not c.buffs)
```

运行输出：

```
<Unit 精英步兵 hp=100 atk=15 buffs=['士气+1']>
<Unit 步兵 hp=120 atk=10 buffs=['士气+1']>
<Unit 步兵 hp=100 atk=10 buffs=['士气+1']>
三份互不影响（buff 列表各自独立）: True
```

### 3.3 原型注册表：按名字批量克隆

游戏里有几十种怪，与其到处 new，不如把"原型"都登记到一张表里，按名字克隆——这就是**原型注册表**（Prototype Registry）。它同时承担了"简单工厂"的职责（按名字出对象），但创建方式是克隆而不是构造：

```python
import copy


class Boss:
    """Boss 原型"""
    def __init__(self, name, hp, skill):
        self.name = name
        self.hp = hp
        self.skill = skill
    def clone(self):
        return copy.deepcopy(self)
    def __repr__(self):
        return f"<Boss {self.name} hp={self.hp} skill={self.skill}>"


class PrototypeRegistry:
    """原型注册表：登记好各种原型，按名字取用克隆"""
    def __init__(self):
        self._prototypes = {}
    def register(self, name, prototype):
        self._prototypes[name] = prototype
    def create(self, name):
        """按名字克隆出一个新对象"""
        if name not in self._prototypes:
            raise KeyError(f"没有登记叫 {name} 的原型")
        return self._prototypes[name].clone()


registry = PrototypeRegistry()
registry.register("史莱姆王", Boss("史莱姆王", 500, "分裂"))
registry.register("骷髅王", Boss("骷髅王", 800, "召唤骷髅"))
registry.register("最终魔王", Boss("最终魔王", 3000, "灭世一击"))

# 打副本：同一关要刷 3 只骷髅王（每只独立，血量微调）
for i in range(3):
    sk = registry.create("骷髅王")
    sk.hp += i * 50
    print(f"第 {i + 1} 只：{sk}")
```

运行输出：

```
第 1 只：<Boss 骷髅王 hp=800 skill=召唤骷髅>
第 2 只：<Boss 骷髅王 hp=850 skill=召唤骷髅>
第 3 只：<Boss 骷髅王 hp=900 skill=召唤骷髅>
```

---

## 4. Python 特有玩法

其他语言要实现原型，得自己写 `clone()`、自己处理深拷贝、自己维护注册表。而 Python 的 `copy` 模块把最难的部分（深拷贝）直接内建了——很多场景下，**原型模式在 Python 里就是一行 `copy.deepcopy(obj)`**。

### 4.1 `copy.copy` vs `copy.deepcopy`：浅拷贝与深拷贝

这是本章最重要的一张图，请记住：**浅拷贝只复制外壳，内部对象还是共享的；深拷贝连内部对象一起复制，完全独立**。

```python
import copy


class Skill:
    def __init__(self, name, level):
        self.name = name
        self.level = level
    def __repr__(self):
        return f"Skill({self.name}, Lv{self.level})"


class Character:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills


hero = Character("勇者", [Skill("斩击", 3), Skill("火球", 2)])

shallow = copy.copy(hero)      # 浅拷贝：只复制外壳
deep = copy.deepcopy(hero)     # 深拷贝：连内部对象一起复制

print("浅拷贝共享技能列表：", shallow.skills is hero.skills)   # True
print("深拷贝技能列表独立：", deep.skills is hero.skills)      # False

# 修改浅拷贝里的技能等级，原版跟着变——经典 bug！
shallow.skills[0].level = 9
print("原版技能等级：", [s.level for s in hero.skills])    # 被改成了 9
print("深拷贝技能等级：", [s.level for s in deep.skills])   # 还是 3
```

运行输出：

```
浅拷贝共享技能列表： True
深拷贝技能列表独立： False
原版技能等级： [9, 2]
深拷贝技能等级： [3, 2]
```

### 4.2 `dataclasses.replace`：只替换部分字段生成新对象

用 `dataclass` 定义的数据类，可以借助 `dataclasses.replace` 实现"克隆一份，只改其中几个字段"——比 `deepcopy` 再手动改字段更清晰：

```python
from dataclasses import dataclass, replace


@dataclass
class Weapon:
    name: str
    damage: int


@dataclass
class Soldier:
    name: str
    hp: int
    weapon: Weapon


s1 = Soldier("小强", 100, Weapon("步枪", 30))

# replace 只替换指定字段，其余字段原样复制——天然的原型操作
s2 = replace(s1, name="阿伟")
s3 = replace(s1, hp=150, weapon=Weapon("狙击枪", 90))

print(s1)
print(s2)
print(s3)

# 注意：replace 是"浅"的——没替换的 weapon 还是同一个对象
s2.weapon.damage = 999
print("改 s2 的武器，原版也遭殃：", s1.weapon.damage)
```

运行输出：

```
Soldier(name='小强', hp=100, weapon=Weapon(name='步枪', damage=30))
Soldier(name='阿伟', hp=100, weapon=Weapon(name='步枪', damage=30))
Soldier(name='小强', hp=150, weapon=Weapon(name='狙击枪', damage=90))
改 s2 的武器，原版也遭殃： 999
```

### 4.3 自定义 `__copy__` / `__deepcopy__`

有些对象"不能照搬"：比如数据库连接、socket，复制一份连接等于复制一份网络资源。这时可以自定义拷贝行为——复制配置，但复用连接资源本身；`__copy__` 同理，可以决定"哪些字段该复制、哪些该共享"：

```python
import copy


class DatabaseConnection:
    """数据库连接：复制时只复制"配置"，连接资源直接复用"""
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._socket = f"<socket {host}:{port}>"  # 模拟真实的连接资源
    def __deepcopy__(self, memo):
        """深拷贝时只复制配置，不复制连接资源本身"""
        print(f"深拷贝 {self.host}:{self.port}，连接资源复用")
        new = DatabaseConnection(self.host, self.port)
        new._socket = self._socket   # 关键：复用同一个连接资源
        memo[id(self)] = new
        return new
    def __repr__(self):
        return f"<DB {self.host}:{self.port} {self._socket}>"


class Player:
    """自定义 __copy__：浅拷贝时只复制部分字段"""
    def __init__(self, name, level, inventory):
        self.name = name
        self.level = level
        self.inventory = inventory  # 背包列表
    def __copy__(self):
        """浅拷贝：只复制名字和等级，背包给个新的空列表"""
        print("调用自定义 __copy__")
        return Player(self.name, self.level, [])
    def __repr__(self):
        return f"<Player {self.name} Lv{self.level} 背包={self.inventory}>"


conn = DatabaseConnection("192.168.1.1", 3306)
conn_copy = copy.deepcopy(conn)
print("原连接：", conn)
print("复制品：", conn_copy)
print("连接资源被复用（同一个 socket）:", conn._socket is conn_copy._socket)

p = Player("阿伟", 10, ["木剑", "药水"])
p2 = copy.copy(p)
p2.inventory.append("屠龙刀")
print("原版：", p)
print("复制品：", p2)
```

运行输出：

```
深拷贝 192.168.1.1:3306，连接资源复用
原连接： <DB 192.168.1.1:3306 <socket 192.168.1.1:3306>>
复制品： <DB 192.168.1.1:3306 <socket 192.168.1.1:3306>>
连接资源被复用（同一个 socket）: True
调用自定义 __copy__
原版： <Player 阿伟 Lv10 背包=['木剑', '药水']>
复制品： <Player 阿伟 Lv10 背包=['屠龙刀']>
```

---

## 5. 真实世界中的它

### 标准库：`copy` 模块

Python 的 `copy` 模块就是"内置的原型模式工具包"，`deepcopy` 还藏着一个普通手写克隆做不到的细节：**它保持对象间的别名关系**——同一个对象被引用两次，深拷贝后两个引用仍然指向同一个新对象：

```python
import copy

data = [1, 2]
original = [data, data]   # 同一个列表被引用两次

cloned = copy.deepcopy(original)
print("克隆后两个元素仍是同一个对象:", cloned[0] is cloned[1])
print("但与原版已经无关:", cloned[0] is not original[0])
```

运行输出：

```
克隆后两个元素仍是同一个对象: True
但与原版已经无关: True
```

### 标准库：`dataclasses.replace`

`dataclasses.replace`（Python 3.7+）本质就是一个"克隆 + 换字段"的工厂函数，在配置管理、事件溯源里非常常用。拿它模拟"函数参数防副作用"——把传进来的对象先克隆一份再改，绝不污染调用方的原对象：

```python
import copy


class Unit:
    def __init__(self, name, buffs):
        self.name = name
        self.buffs = buffs


def apply_buff(unit, buff_name):
    new_unit = copy.deepcopy(unit)
    new_unit.buffs.append(buff_name)
    return new_unit


u = Unit("剑士", ["攻击+1"])
u2 = apply_buff(u, "暴击+5")
print("原单位 buff：", u.buffs)
print("新单位 buff：", u2.buffs)
```

运行输出：

```
原单位 buff： ['攻击+1']
新单位 buff： ['攻击+1', '暴击+5']
```

### 框架：Django 的 QuerySet

Django 的 `QuerySet` 实现了 `copy()` 方法（内部叫 `_chain()`），每个查询集操作（`.filter()`、`.exclude()`、`.order_by()`）返回的都是**原查询集的拷贝**，而不是修改原对象——所以你可以放心链式调用而不污染前面的查询。而且 QuerySet 是惰性的，拷贝只是复制"查询条件"，不复制数据，成本极低。你在源码里看到的 `self._chain()` 就是原型思想的直接体现。

另外，Python 内置的 `list.copy()`、`dict.copy()`、`set.copy()` 以及切片 `a[:]` 都是最朴素的浅拷贝原型——我们其实天天在用原型模式而不自知。

---

## 6. 优缺点与适用场景

### 优点

- **创建更快**：复制通常比从零构造便宜，尤其对象初始化很贵时（连库、读配置、算默认值）；
- **隐藏创建细节、批量变体轻松**：客户端只调 `clone()` 不知道内部结构；"克隆 + 微调"一条龙，10 个略有差异的对象几分钟搞定；
- **运行时动态加种类**：原型注册表可以在程序运行时登记新原型，不用改已有代码（开闭原则）。

### 缺点

- **深拷贝可能很贵**：嵌套很深的对象，deepcopy 的时间和内存开销可能超过直接构造；
- **深拷贝有坑**：循环引用、不可复制的资源（锁、socket）、共享状态没处理好，都会出诡异 bug；
- **每个类都要实现克隆、且模式被"内建"了大半**：类一多 `clone()` 代码重复；而 `copy.deepcopy` 太强，很多时候你只需要一行代码，不需要"模式"的架子——别为了模式而模式。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 对象构造昂贵、但复制便宜 | 对象太简单，直接 new 更直观 |
| 需要大量相似对象（游戏单位、报表变体） | 深拷贝成本高于直接构造 |
| 想隐藏创建细节、解耦客户端 | 对象含不可复制的资源（socket、文件句柄） |
| 运行时需要动态登记新"物种"（注册表） | 只需要一个固定对象（用单例或工厂） |

> **一句话权衡**：复制比构造便宜、且要"批量微调"时用原型；否则直接构造，别为了用模式而用模式。

---

## 7. 与其他模式的关系

- **与工厂、备忘录**：工厂是"new 一个"，原型是"克隆一个"；原型注册表本质是"用克隆实现的简单工厂"。备忘录是"保存状态快照以便恢复"（第 20 章），原型是"复制对象以便创建新对象"——快照 vs 克隆：一个回到过去，一个再造一个。
- **与单例**：正好相反——单例是"只造一个、谁拿都是它"，原型是"造很多个、每份都独立"（第 1 章里就提过这对反义词）。
- **与享元**：享元是"共享实例省内存"（第 23 章），原型是"复制实例"——一个求同、一个求异，理念相反。
- **与建造者、组合**：建造者一步步搭建复杂对象（第 11 章），原型一次性复制现成对象；组合模式的对象树（第 17 章）用 `deepcopy` 克隆特别顺手——一棵树整体复制，内部关系全保留。

---

## 8. 常见误区

### 误区 1：浅拷贝当深拷贝用（经典 bug）

这是原型模式最大的坑：只复制了外壳，内部嵌套对象还是共享的，改复制品，原版跟着变——4.1 里 `shallow.skills[0].level = 9` 把原版的技能等级也改成了 9，就是这个 bug 的完整演示。**判断标准**：对象里有列表、字典或其他对象时，先问一句"我改复制品，原版会跟着变吗？"会，就用深拷贝。

### 误区 2：拷贝了含锁/连接的对象

锁、socket、文件句柄这类"资源"被复制是危险的——要么复制失败，要么复制出两个对象共享同一把锁：

```python
import copy
import threading

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    def increment(self):
        with self.lock:
            self.value += 1
            return self.value


c1 = Counter()
try:
    c2 = copy.deepcopy(c1)   # 想复制一个计数器？
except TypeError as e:
    print("深拷贝失败：", e)

print("原因：锁是资源，不允许被复制")
```

运行输出：

```
深拷贝失败： cannot pickle '_thread.lock' object
原因：锁是资源，不允许被复制
```

`threading.Lock` 这类对象被设计成"不可复制"——在 Python 3.12 里 deepcopy 会直接抛 `TypeError`。socket、文件句柄、数据库连接同理：要么复制失败，要么复制出两个对象共享同一份资源。处理办法：自定义 `__deepcopy__`（见 4.3），只复制数据、复用或重建资源。

### 误区 3：以为原型能解决一切复制问题

`deepcopy` 不是银弹：对象很深、很大时，深拷贝可能比直接构造还慢；而且 deepcopy 也不是万能的——有些第三方对象不支持拷贝。另外要注意，深拷贝对**循环引用**处理得很好，但如果你手写克隆（自己 new + 抄字段），遇到"A 引用 B、B 又引用 A"的环就直接死循环了：

```python
import copy

# 循环引用：A 引用 B，B 又引用 A——deepcopy 能优雅处理
class Node:
    def __init__(self, name):
        self.name = name
        self.friend = None


a = Node("阿伟")
b = Node("小明")
a.friend = b
b.friend = a

a2 = copy.deepcopy(a)
print("克隆体内部引用也成环:", a2.friend.friend is a2)
print("与原版完全无关:", a2 is not a and a2.friend is not b)
```

运行输出：

```
克隆体内部引用也成环: True
与原版完全无关: True
```

> 教训：能用 `copy.deepcopy` 就别手写克隆；手写克隆时，务必想清楚嵌套结构和循环引用。

### 误区 4：用 `=` 赋值当拷贝

`b = a` 不是拷贝，只是给同一个对象起了个新名字（别名）：`b.append(x)` 改的就是 `a`。想复制，必须显式调用 `copy.copy` / `copy.deepcopy` / `clone()`——这是最基础也最容易被忽略的一条。

---

## 9. 练习题

### 练习 1：为文档类实现 `clone()`

有一个 `Document` 类，内部有段落列表（每个段落是字典）。请实现 `clone()`，要求克隆体与原文档完全独立（改克隆体不影响原版）：

```python
import copy


class Document:
    def __init__(self, title, sections):
        self.title = title
        self.sections = sections  # 段落列表，每个段落是一个 dict
    def clone(self):
        return copy.deepcopy(self)
    def __repr__(self):
        return f"<Document {self.title!r} 段落数={len(self.sections)}>"


doc = Document("周报", [{"标题": "本周进展", "内容": "完成了登录模块"}])
backup = doc.clone()
backup.sections.append({"标题": "下周计划", "内容": "写测试"})

print("原文档段落数：", len(doc.sections))
print("备份段落数：", len(backup.sections))
print("互不影响：", len(doc.sections) == 1)
```

运行输出：

```
原文档段落数： 1
备份段落数： 2
互不影响： True
```

### 练习 2：用 `dataclasses.replace` 生成配置变体

有一个 `AppConfig` 数据类，请用 `replace` 生成"生产配置"（8 个 worker、关闭 debug）和"开发配置"（打开 debug），且不修改基础配置：

```python
from dataclasses import dataclass, replace


@dataclass
class AppConfig:
    host: str
    port: int
    debug: bool = False
    workers: int = 4


base = AppConfig(host="0.0.0.0", port=8000)
prod = replace(base, debug=False, workers=8)
dev = replace(base, debug=True)

print("基础配置：", base)
print("生产配置：", prod)
print("开发配置：", dev)
print("基础配置未被改动：", base.port == 8000 and base.workers == 4)
```

运行输出：

```
基础配置： AppConfig(host='0.0.0.0', port=8000, debug=False, workers=4)
生产配置： AppConfig(host='0.0.0.0', port=8000, debug=False, workers=8)
开发配置： AppConfig(host='0.0.0.0', port=8000, debug=True, workers=4)
基础配置未被改动： True
```

### 练习 3：用原型注册表批量刷怪

写一个怪物注册表：登记"史莱姆"和"哥布林"两种原型，每种刷 3 只，血量依次 +0/+5/+10，并保证每只怪物独立（掉落列表互不影响）：

```python
import copy


class Monster:
    def __init__(self, name, hp, drops):
        self.name = name
        self.hp = hp
        self.drops = drops
    def clone(self):
        return copy.deepcopy(self)
    def __repr__(self):
        return f"{self.name}(hp={self.hp}) 掉落:{self.drops}"


registry = {
    "史莱姆": Monster("史莱姆", 30, ["黏液"]),
    "哥布林": Monster("哥布林", 60, ["短剑"]),
}

for kind in ("史莱姆", "哥布林"):
    for i in range(3):
        m = registry[kind].clone()
        m.hp += i * 5
        print(f"{kind} 第{i + 1}只：{m}")
```

运行输出：

```
史莱姆 第1只：史莱姆(hp=30) 掉落:['黏液']
史莱姆 第2只：史莱姆(hp=35) 掉落:['黏液']
史莱姆 第3只：史莱姆(hp=40) 掉落:['黏液']
哥布林 第1只：哥布林(hp=60) 掉落:['短剑']
哥布林 第2只：哥布林(hp=65) 掉落:['短剑']
哥布林 第3只：哥布林(hp=70) 掉落:['短剑']
```

---

## 10. 小结与口诀

> **口诀：复制粘贴创建对象；浅拷贝坑别踩；深拷贝一锤定音；克隆加微调，批量出对象。**

原型模式的本质就一句话：**别从零造，复制现成的**。它把"创建对象"从"调用构造函数"变成"调用 clone()"，客户端从此不关心对象内部结构。但 Python 开发者要清醒：`copy.deepcopy` 把原型模式最难的部分（深拷贝、循环引用、别名保持）都内建了，所以这个模式在 Python 里往往"退化成一行代码"。真正需要你动脑的，是**判断什么时候该复制、复制多深、以及哪些资源不能复制**——想清楚这三点，原型模式就是你的造兵工厂。下一章，我们来看一个让"多对多"变成"多对一"的模式——**中介者**：别互相喊话，都通过中间人。

---

*本章金句：原型模式的哲学：与其从零建造，不如复制一份再微调——前提是深拷贝别踩坑。*
