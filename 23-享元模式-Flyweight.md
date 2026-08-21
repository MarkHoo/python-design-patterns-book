# 第 23 章 享元模式（Flyweight）

> **一句话总结**：重复的东西别反复造，共享一份。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 结构型 | ★★★★☆ | ★☆☆☆☆ |

---

## 1. 引子：先讲个故事

想象一座图书馆：藏书几万册，读者成千上万。如果每个读者都把读过的书"复印一份带回家"，图书馆早就塌了。正确的做法是——**书只有一份，谁借谁看**；借的时候记下"这本书现在在谁手里、翻到第几页"。书是共享的，阅读位置是私人的。

程序世界里最典型的"图书馆"是文字渲染：翻来覆去就那么几十个字符，却要为每个字符都存一份"字符 + 字体 + 字号 + 颜色"。一页 3000 字、一本书 300 页，就是上百万个重复对象：

```python
# 引子：没有享元的世界——每个字符都自带一套完整样式
class Character:
    def __init__(self, ch: str, font: str, size: int, color: str):
        self.ch = ch
        self.font = font
        self.size = size
        self.color = color

text = "hello" * 2000      # 一页文章：1 万个字符
chars = [Character(c, "微软雅黑", 12, "#333333") for c in text]

unique = len({c.ch for c in chars})
print(f"共创建 {len(chars)} 个字符对象")
print(f"其中不同的字符只有 {unique} 种")
print("字体、字号、颜色被重复存了", len(chars), "份")
```

运行输出：

```
共创建 10000 个字符对象
其中不同的字符只有 4 种
字体、字号、颜色被重复存了 10000 份
```

问题在哪？`"hello"` 只有 4 种字符，样式（微软雅黑、12 号、#333333）更是完全一样——**同样的数据被复制了 1 万份**。享元模式就是来解决这个问题的：把重复的部分抽出来共享，把随位置变化的部分（坐标、颜色）留给调用方每次传入。

---

## 2. 模式登场

### 定义

> **享元模式**：把对象的"可共享状态"抽出来共享，让成千上万个对象共用同一份，从而大幅节省内存。

### 核心概念：内部状态 vs 外部状态

这是享元模式最重要的划分，也是它最难的地方：

| 状态 | 含义 | 例子 | 谁持有 |
|------|------|------|--------|
| **内部状态（intrinsic）** | 不随环境变化、可以共享的部分 | 字符、字体、贴图、纹理 | 享元对象自己（只读） |
| **外部状态（extrinsic）** | 随使用场景变化的部分 | 坐标、颜色、速度、页码 | 客户端，每次调用时传入 |

### 结构

```
   ┌──────────────────────────────┐
   │      FlyweightFactory        │
   │        （享元工厂/池）         │
   ├──────────────────────────────┤
   │ - pool: dict                 │
   ├──────────────────────────────┤
   │ + get(key)                   │  ← 有缓存返回，没缓存新建
   └──────────────────────────────┘
            │ 返回共享实例
            ▼
   ┌──────────────────────────────┐
   │        Flyweight             │
   │         （享元对象）           │
   ├──────────────────────────────┤
   │ - intrinsic: 内部状态（共享）  │
   ├──────────────────────────────┤
   │ + operation(extrinsic)       │  ← 外部状态每次传入
   └──────────────────────────────┘
            ▲
            │
   ┌────────┴────────┐
   │     Client      │   持有享元引用 + 各自的外部状态
   └─────────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **Flyweight（享元）** | 包含内部状态的共享对象 |
| **FlyweightFactory（享元工厂）** | 维护享元池，`get` 时"有就返回，没有就建" |
| **Client（客户端）** | 持有享元引用，使用时传入外部状态 |

---

## 3. Python 实现

### 3.1 文字渲染：字符共享字体

字符 + 字体 + 字号是内部状态（共享一份），坐标 + 颜色是外部状态（渲染时传入）：

```python
# 文字渲染：字符+字体是内部状态（共享），位置+颜色是外部状态（每次传）
class Glyph:
    def __init__(self, ch: str, font: str, size: int):
        self.ch = ch
        self.font = font
        self.size = size

    def render(self, x: int, y: int, color: str) -> str:
        return f"{self.ch!r}({self.font},{self.size}) 画在({x},{y}) 颜色{color}"

class GlyphFactory:
    """享元工厂：同一个字符+样式，只创建一个对象"""

    def __init__(self):
        self._pool = {}

    def get(self, ch: str, font: str, size: int) -> Glyph:
        key = (ch, font, size)
        if key not in self._pool:
            self._pool[key] = Glyph(ch, font, size)
        return self._pool[key]

    def size(self) -> int:
        return len(self._pool)

factory = GlyphFactory()
text = "hello"
glyphs = [factory.get(c, "微软雅黑", 12) for c in text]
print(f"创建了 {len(glyphs)} 个引用，但对象只有 {factory.size()} 个")
print("所有 'l' 是同一个对象:", glyphs[2] is glyphs[3])

# 渲染时传入位置和颜色（外部状态）
print(glyphs[0].render(0, 0, "黑色"))
print(glyphs[4].render(10, 0, "红色"))
```

运行输出：

```
创建了 5 个引用，但对象只有 4 个
所有 'l' 是同一个对象: True
'h'(微软雅黑,12) 画在(0,0) 颜色黑色
'o'(微软雅黑,12) 画在(10,0) 颜色红色
```

`hello` 里有两个 `l`，但工厂只造了一个 `Glyph('l', ...)`——两个位置共享同一个对象，这就是享元。

### 3.2 粒子系统：海量粒子共享贴图

游戏里一屏几千个粒子，每个粒子都带一张贴图会直接撑爆内存。正确做法：贴图按种类共享，粒子自己只留"位置 + 速度"：

```python
# 粒子系统：贴图/颜色是内部状态（共享），位置/速度是外部状态（每个粒子独有）
class ParticleType:
    """享元：一种粒子的贴图与颜色"""

    def __init__(self, name: str, texture: str, color: str):
        self.name = name
        self.texture = texture
        self.color = color

    def __repr__(self):
        return f"<粒子类型 {self.name} {self.color}>"

class Particle:
    """普通粒子：持有类型引用 + 自己的运动状态"""

    def __init__(self, ptype: ParticleType, x: float, y: float, vx: float, vy: float):
        self.ptype = ptype
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self) -> None:
        self.x += self.vx
        self.y += self.vy

    def draw(self) -> str:
        return f"在({self.x:.0f},{self.y:.0f}) 画 {self.ptype}"

class ParticleFactory:
    def __init__(self):
        self._types = {}

    def get_type(self, name: str, texture: str, color: str) -> ParticleType:
        key = (name, texture, color)
        if key not in self._types:
            self._types[key] = ParticleType(name, texture, color)
        return self._types[key]

factory = ParticleFactory()
explosion = factory.get_type("爆炸", "fire.png", "橙红")
spark = factory.get_type("火花", "spark.png", "金黄")

particles = [Particle(explosion, i, 0, 0.1, -1) for i in range(1000)]
particles += [Particle(spark, i, 100, 0.2, 2) for i in range(500)]

print(f"1500 个粒子，但贴图对象只有 {len(factory._types)} 种")
p = particles[0]
print(p.draw())
p.move()
print("移动后：", p.draw())
```

运行输出：

```
1500 个粒子，但贴图对象只有 2 种
在(0,0) 画 <粒子类型 爆炸 橙红>
移动后： 在(0,-1) 画 <粒子类型 爆炸 橙红>
```

1500 个粒子共享 2 个贴图对象——省下的内存可以让游戏多开 100 个特效。

### 3.3 通用享元池：一个 dict 搞定

享元池的本质是"**带缓存的工厂**"。把"怎么创建对象"抽成一个函数，池子本身谁都能用：

```python
# 通用享元池：把任意"构造逻辑"变成享元工厂
class FlyweightFactory:
    """按参数键去重：同一个键只创建一次"""

    def __init__(self, builder):
        self._builder = builder
        self._pool = {}

    def get(self, *args):
        if args not in self._pool:
            self._pool[args] = self._builder(*args)
            print(f"新建并缓存：{args}")
        return self._pool[args]

def make_user(name: str, dept: str):
    """真实的"昂贵"对象构造（这里用 dict 模拟）"""
    return {"name": name, "dept": dept}

users = FlyweightFactory(make_user)
u1 = users.get("小明", "研发部")
u2 = users.get("小明", "研发部")
u3 = users.get("小红", "研发部")
print("同名同部门是同一个对象:", u1 is u2)
print("不同名字各自独立:", u1 is not u3)
print("池子大小:", len(users._pool))
```

运行输出：

```
新建并缓存：('小明', '研发部')
新建并缓存：('小红', '研发部')
同名同部门是同一个对象: True
不同名字各自独立: True
池子大小: 2
```

注意 `get` 的返回值在 Python 里天然是共享的：第二次 `get` 拿到的是同一个 dict——这正是享元池想要的语义。

---

## 4. Python 特有玩法

### 4.1 `sys.intern`：字符串驻留

CPython 把一部分字符串"驻留"（intern）在全局表里，相同的字符串只存一份，比较时可以直接比 `is`（快）。`sys.intern` 让我们手动把**运行时拼出来的字符串**也收编进驻留表：

```python
# sys.intern：把运行时拼出来的字符串"收编"进驻留表，共享一份
import sys

# 运行时拼出来的字符串：默认各自独立
s1 = "".join(["设", "计", "模", "式"])
s2 = "".join(["设", "计", "模", "式"])
print("运行时拼接，s1 is s2:", s1 is s2)          # False

# intern 之后：指向同一份
i1 = sys.intern(s1)
i2 = sys.intern(s2)
print("intern 之后，i1 is i2:", i1 is i2)          # True
print("内容相等:", i1 == i2)
```

运行输出：

```
运行时拼接，s1 is s2: False
intern 之后，i1 is i2: True
内容相等: True
```


### 4.2 CPython 小整数缓存

CPython 把 **-5 ~ 256** 的小整数常驻内存，谁用都是同一份。注意：要用**运行时算出来的值**才能看清缓存边界——直接写 `257 is 257` 会被编译器合并成同一个常量，看不出效果：

```python
# CPython 小整数缓存：-5~256 常驻，谁用都是同一份
base = 100
a = base + 156      # 运行时算出 256
b = base + 156
print("运行时 256 is 256:", a is b)    # True：命中缓存

c = base + 157      # 运行时算出 257
d = base + 157
print("运行时 257 is 257:", c is d)    # False：超出缓存，各自新建

e = base - 105      # -5
f = base - 105
print("运行时 -5 is -5:", e is f)      # True：下边界之内

g = base - 106      # -6
h = base - 106
print("运行时 -6 is -6:", g is h)      # False：越界
```

运行输出：

```
运行时 256 is 256: True
运行时 257 is 257: False
运行时 -5 is -5: True
运行时 -6 is -6: False
```

看到没？256 和 -5 是"共享的"，257 和 -6 是"每次新建的"——解释器自己就是个享元大师。

### 4.3 `functools.lru_cache`：标准库自带的享元池

想给任意函数套上"按参数去重"的享元池？`lru_cache` 一行搞定：

```python
# functools.lru_cache：标准库自带的"享元工厂"
import functools

@functools.lru_cache(maxsize=None)
def get_glyph(ch: str, font: str) -> tuple:
    print(f"构造字形：{ch!r}/{font}")
    return (ch, font)

g1 = get_glyph("A", "宋体")
g2 = get_glyph("A", "宋体")
g3 = get_glyph("B", "宋体")
print("同参数共享:", g1 is g2)
print("不同参数独立:", g1 is not g3)
```

运行输出：

```
构造字形：'A'/宋体
构造字形：'B'/宋体
同参数共享: True
不同参数独立: True
```

---

## 5. 真实世界中的它

### 5.1 CPython 解释器：最大的享元用户

解释器自己就是享元狂魔：`None`、`True`、`False` 全局唯一，字符串字面量自动驻留，小整数自动共享：

```python
# CPython 解释器自己是"享元大师"：None、字面量、小整数全都共享
print("None 全局唯一:", None is None)
print("True 全局唯一:", True is True)

a = "hello"
b = "hello"
print("字符串字面量自动共享:", a is b)

c = 256
d = 256
print("小整数自动共享:", c is d)
```

运行输出：

```
None 全局唯一: True
True 全局唯一: True
字符串字面量自动共享: True
小整数自动共享: True
```

所以你才能放心写 `x is None`——因为 `None` 全宇宙只有一个。这就是为什么 Python 官方建议：**`is` 只用来比较 `None`/`True`/`False` 和单例**，其他情况用 `==`。

### 5.2 小整数缓存的"坑"：字面量会被编译器合并

网上流传的"`257 is 257` 为 False"其实不靠谱：同一个代码对象里的相同字面量会被编译器合并成同一个常量。真实的边界要用**运行时创建**的值才能看清：

```python
# 小整数缓存的"坑"：字面量合并 vs 运行时新建
a = 257
b = 257
print("同一代码对象里，字面量 257 被合并:", a is b)   # True（编译器优化）

x = int("257")
y = int("257")
print("运行时各自创建:", x is y)                     # False（缓存之外）
```

运行输出：

```
同一代码对象里，字面量 257 被合并: True
运行时各自创建: False
```

写代码时记住结论就好：**依赖"小整数共享"是不可靠的，别拿 `is` 比较整数**——要比较值就用 `==`，要比较身份就用 `id()` 或 `is`（仅限 None/单例）。

### 5.3 其他真实案例（文字）

- **CPython 源码**：解释器内部大量复用单字母变量（`i`、`j`、`k`），这些标识符都在驻留表里共享；`dict` 的键、`str` 的方法返回值也大量复用已驻留的字符串。
- **数据库连接池**（psycopg2 等）：连接对象按配置复用，本质是"每个键一个实例"的享元池 + 对象池思想的结合。

---

## 6. 优缺点与适用场景

### 优点

- **大幅省内存**：海量细粒度对象共享内部状态，内存占用从 O(对象数) 降到 O(种类数)；
- **创建成本分摊**：昂贵的加载（贴图、字体）只做一次。

### 缺点

- **内外状态划分难**：分错了就是经典 bug（见误区 1）；
- **共享对象必须只读**：内部状态一旦被改，所有使用者一起遭殃；
- **复杂度与收益不成正比**：对象没到"海量"级别，享元就是纯负担。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 大量重复的细粒度对象（字符、粒子、树、订单行） | 对象数量少、差异大 |
| 内部状态占大头、外部状态很小 | 内部状态几乎为零 |
| 对象创建成本高（加载贴图、解析字体） | 简单对象（直接 new 更快） |
| 内存紧张的场景（游戏、移动端） | 代码可读性优先的小工具 |

> **Python 圈的共识**：Python 对象本身就有不小的内存开销，享元的收益往往比 C++/Java 更明显——但前提依然是"对象真的多"。

---

## 7. 与其他模式的关系

- **享元 vs 单例**：单例是"全局一个实例"，享元池是"**每个键一个实例**的注册表"——理念同源，粒度不同；
- **享元 + 工厂**：享元池本质是**带缓存的工厂**，工厂方法决定"怎么造"，池子决定"造不造新的"；
- **享元 vs 原型**：原型是"复制出多个"，享元是"共享同一个"——正好相反；复制成本高时，优先考虑享元；
- **享元 + 状态**：状态模式中"每个状态一个对象"的场景，常配合享元让状态对象全局共享。

---

## 8. 常见误区

### 误区 1：外部状态混进共享对象（经典 bug）

把本该"每次传入"的颜色写进了共享的 `ParticleType`——一个粒子改颜色，**全体跟着变**：

```python
# 误区：把外部状态写进共享对象——一个粒子改颜色，全体跟着变
class ParticleType:
    def __init__(self, texture: str):
        self.texture = texture
        self.color = "白色"    # 共享的"默认颜色"

class Particle:
    def __init__(self, ptype: ParticleType, x: float, y: float):
        self.ptype = ptype
        self.x = x
        self.y = y

    def set_color(self, color: str) -> None:
        self.ptype.color = color   # 错误！改的是共享对象

explosion = ParticleType("fire.png")
p1 = Particle(explosion, 1, 1)
p2 = Particle(explosion, 2, 2)

p1.set_color("红色")               # p1 想把自己染红
print("p1 看到的颜色：", p1.ptype.color)
print("p2 看到的颜色：", p2.ptype.color, "← 被 p1 连累了！")
```

运行输出：

```
p1 看到的颜色： 红色
p2 看到的颜色： 红色 ← 被 p1 连累了！
```

**正确做法**：颜色是外部状态，放进 `draw(x, y, color)` 的参数里，或者存在 `Particle` 自己身上（`Particle` 不是享元，它只是持有享元引用）。

### 误区 2：过度优化

享元只在"**海量重复对象**"时才划算。Python 创建 1 万个简单对象只需几毫秒，池子本身的字典查找反而更慢。判断标准很简单：**先 profile，再优化**。对象没到十万、百万级别，或者每个对象内部状态都不一样，别上享元——收益小、复杂度高，还容易引入共享状态的坑。

### 误区 3：忘记线程安全

多线程同时 `get` 同一个键，可能重复创建、甚至拿到半个对象。加锁 + 双重检查是标准解法：

```python
import threading

class SafeFactory:
    """线程安全的享元工厂：加锁 + 双重检查"""

    def __init__(self):
        self._pool = {}
        self._lock = threading.Lock()

    def get(self, key):
        if key not in self._pool:          # 快速路径：不加锁
            with self._lock:               # 慢路径：加锁
                if key not in self._pool:  # 双重检查
                    self._pool[key] = (key, len(self._pool))
        return self._pool[key]

factory = SafeFactory()
results = []

def worker():
    results.append(factory.get("共享资源"))

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("10 个线程拿到的都是同一个对象:", len({id(r) for r in results}) == 1)
```

运行输出：

```
10 个线程拿到的都是同一个对象: True
```

---

## 9. 练习题

### 练习 1：订单系统的商品享元

1000 笔订单、每笔 2 行，但商品只有两种。用享元让"商品对象"只创建 2 个：

```python
# 答案：商品信息共享，订单行各自只存数量
class Product:
    def __init__(self, sku: str, name: str, price: float):
        self.sku = sku
        self.name = name
        self.price = price

class OrderLine:
    def __init__(self, product: Product, qty: int):
        self.product = product
        self.qty = qty

    def total(self) -> float:
        return self.product.price * self.qty

class ProductFactory:
    def __init__(self):
        self._pool = {}

    def get(self, sku: str, name: str, price: float) -> Product:
        if sku not in self._pool:
            self._pool[sku] = Product(sku, name, price)
        return self._pool[sku]

factory = ProductFactory()
lines = []
for i in range(1000):
    lines.append(OrderLine(factory.get("A001", "机械键盘", 399), i % 3 + 1))
    lines.append(OrderLine(factory.get("B002", "鼠标垫", 29), i % 5 + 1))

print("订单行数：", len(lines))
print("商品对象数：", len(factory._pool))
print("第一条订单金额：", lines[0].total())
```

运行输出：

```
订单行数： 2000
商品对象数： 2
第一条订单金额： 399
```

### 练习 2：用 `lru_cache` 实现字形工厂

把 3.1 的手写 `GlyphFactory` 换成 `functools.lru_cache` 实现：

```python
# 答案：用 lru_cache 实现字形工厂（一行搞定缓存）
import functools

@functools.lru_cache(maxsize=None)
def get_glyph(ch: str, font: str, size: int) -> tuple:
    return (ch, font, size)

text = "abracadabra"
glyphs = [get_glyph(c, "黑体", 14) for c in text]
print("字符数：", len(glyphs), "，共享字形数：", get_glyph.cache_info().currsize)
print("两个 'a' 是同一份:", get_glyph("a", "黑体", 14) is get_glyph("a", "黑体", 14))
```

运行输出：

```
字符数： 11 ，共享字形数： 5
两个 'a' 是同一份: True
```

### 练习 3：给森林游戏划分内外状态

1000 棵树，只有 2 个树种。把"树种"抽成享元，每棵树只保留自己的坐标：

```python
# 答案：把共享的"树种"抽成享元，坐标留给每棵树自己
class TreeType:
    """享元：树种（贴图、颜色）"""

    def __init__(self, name: str, texture: str, color: str):
        self.name = name
        self.texture = texture
        self.color = color

class Tree:
    """外部状态：每棵树自己的位置"""

    def __init__(self, tree_type: TreeType, x: float, y: float):
        self.tree_type = tree_type
        self.x = x
        self.y = y

    def draw(self) -> str:
        return f"{self.tree_type.name} 种在 ({self.x}, {self.y})"

class TreeFactory:
    def __init__(self):
        self._pool = {}

    def get(self, name: str, texture: str, color: str) -> TreeType:
        if name not in self._pool:
            self._pool[name] = TreeType(name, texture, color)
        return self._pool[name]

factory = TreeFactory()
forest = [Tree(factory.get("橡树", "oak.png", "绿"), i, i % 10) for i in range(500)]
forest += [Tree(factory.get("枫树", "maple.png", "红"), i, i % 7) for i in range(500)]
print("1000 棵树，树种对象只有", len(factory._pool), "种")
print(forest[0].draw())
```

运行输出：

```
1000 棵树，树种对象只有 2 种
橡树 种在 (0, 0)
```

---

## 10. 小结与口诀

> **口诀：内部状态共享，外部状态传参；重复对象上百万，享元池里省一半。**

享元模式是"用共享换内存"的典型：把对象劈成"共享的内部状态"和"随用的外部状态"两半，前者放进享元池，后者每次传入。它使用率低，是因为大多数程序的对象量级根本到不了需要优化的程度——但一旦到了（游戏、渲染、大数据），它就是救命的那个模式。

下一章，我们挑战全书的"终极大 Boss"——**解释器模式**：定义一门小语言，写个程序解释它。

---

*本章金句：享元是"抠门"的艺术——能共享的绝不重复造，省下的内存都是利润。*
