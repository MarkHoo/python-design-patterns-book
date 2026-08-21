# 第 11 章 建造者模式（Builder）

> **一句话总结**：复杂对象，分步骤搭，最后一步才交货。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 创建型 | ★★★☆☆ | ★★★★☆ |

---

## 1. 引子：先讲个故事

你去电脑城装机，不会把一张写满 20 个参数的纸条丢给老板说"照着配"——你会一步一步来：先选 CPU，再挑内存，显卡要什么型号，硬盘多大，电源多少瓦……每选一样老板记一样，最后"点亮"验收，一台电脑才交付。每一步都有名字，选错了当场就能发现。

程序里那些"复杂对象"（配置、请求、查询条件、报告）跟电脑一样，零件多、可选项多。如果一股脑全塞进构造函数，就会变成这样：

```python
# 引子：用一堆位置参数构造复杂对象——第 4 个参数是啥来着？
class Computer:
    def __init__(self, cpu, memory, gpu, storage, power, case, os_name, has_wifi):
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu
        self.storage = storage
        self.power = power
        self.case = case
        self.os_name = os_name
        self.has_wifi = has_wifi

# 8 个位置参数，谁还记得第 4 个是硬盘还是电源？
pc = Computer("i7-13700K", 32, "RTX 4070", "1TB SSD", "750W", "中塔机箱", "Windows 11", True)
print(f"组装了一台 {pc.cpu} + {pc.gpu} 的电脑")
```

运行输出：

```
组装了一台 i7-13700K + RTX 4070 的电脑
```

这段代码能跑，但浑身是病：调用处看不懂每个参数是啥；传参顺序一错，编译器不拦、程序不报错，只是行为悄悄变歪；以后加一个"水冷"选项，所有调用处都要跟着改。**建造者模式**就是为这类"零件多、步骤多"的对象设计的：把"搭积木"和"交货"分开，一步一步来，每一步都有名字。

---

## 2. 模式登场

### 定义

> **建造者模式**：将一个复杂对象的构建过程与它的表示分离，让同样的构建过程可以构建出不同的表示。

### 解决的问题

1. **参数爆炸**：构造函数参数太多，可读性差、顺序易错；
2. **可选组合多**：对象有很多可选项，组合方式五花八门（披萨的配料有 100 种搭配）。

### 结构

```
┌───────────────────────────────┐
│         Director（导演）         │
├───────────────────────────────┤
│ + construct()                 │  ← 控制构建顺序（可选角色）
└───────────────┬───────────────┘
                │ 指挥
                ▼
┌───────────────────────────────┐
│          Builder（建造者）       │
├───────────────────────────────┤
│ + set_part_a()                │  ← 分步设置零件
│ + set_part_b()                │
│ + build(): Product            │  ← 最后一步交货
└───────────────┬───────────────┘
                │ 构建
                ▼
┌───────────────────────────────┐
│         Product（产品）         │  ← 被搭出来的复杂对象
└───────────────────────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **产品 Product** | 被构建的复杂对象（电脑、请求、披萨） |
| **建造者 Builder** | 提供分步设置零件的方法 + 一个 `build()` 交货 |
| **导演 Director** | 可选：封装"固定的构建顺序/配方"，让调用方不用记步骤 |
| **客户端 Client** | 拿 Builder 分步设置，或直接把 Director 的成品拿走 |

关键点：**`build()` 之前，产品还没"交货"**——你只是在攒零件；`build()` 那一刻才拿到完整对象。

---

## 3. Python 实现

### 3.1 经典版：Builder + Director（披萨定制）

先看教科书式的写法：Builder 提供分步方法，Director 封装"常见配方"，客户端要什么配方直接点单：

```python
class Pizza:
    """产品：披萨"""

    def __init__(self):
        self.size = None
        self.toppings = []
        self.cheese = None
        self.sauce = None

    def __repr__(self):
        return f"<披萨 {self.size}寸 配料={'、'.join(self.toppings)} 奶酪={self.cheese} 酱料={self.sauce}>"

class PizzaBuilder:
    """建造者：分步提供配置项（经典版，方法不返回 self）"""

    def __init__(self):
        self._pizza = Pizza()

    def set_size(self, size):
        self._pizza.size = size

    def add_topping(self, topping):
        self._pizza.toppings.append(topping)

    def set_cheese(self, cheese):
        self._pizza.cheese = cheese

    def set_sauce(self, sauce):
        self._pizza.sauce = sauce

    def build(self):
        """最后一步：交货"""
        pizza = self._pizza
        self._pizza = Pizza()      # 构建完重置，防止下次复用脏数据
        return pizza

class PizzaDirector:
    """导演：封装常见"配方"，控制构建顺序"""

    def __init__(self, builder):
        self._builder = builder

    def make_meat_lover(self):
        b = self._builder
        b.set_size(12)
        b.add_topping("培根")
        b.add_topping("香肠")
        b.set_cheese("马苏里拉")
        b.set_sauce("番茄酱")
        return b.build()

    def make_veggie(self):
        b = self._builder
        b.set_size(10)
        b.add_topping("蘑菇")
        b.add_topping("青椒")
        b.set_cheese("素食奶酪")
        b.set_sauce("蒜香酱")
        return b.build()

director = PizzaDirector(PizzaBuilder())
print(director.make_meat_lover())
print(director.make_veggie())
```

运行输出：

```
<披萨 12寸 配料=培根、香肠 奶酪=马苏里拉 酱料=番茄酱>
<披萨 10寸 配料=蘑菇、青椒 奶酪=素食奶酪 酱料=蒜香酱>
```

调用方只跟 Director 打交道："来个肉食主义"，至于先放芝士还是先放酱，Director 内部搞定。

### 3.2 链式调用版：方法返回 `self`（HTTP 请求）

Python 社区最常见的建造者写法是**链式调用**：每个设置方法返回 `self`，调用方一口气连下去，像在读一句人话：

```python
class HttpRequest:
    """产品：HTTP 请求"""

    def __init__(self):
        self.method = "GET"
        self.url = ""
        self.headers = {}
        self.body = None
        self.timeout = 30

    def __repr__(self):
        return f"<请求 {self.method} {self.url} headers={self.headers} body={self.body} 超时={self.timeout}s>"

class RequestBuilder:
    """建造者：每个方法返回 self，支持链式调用"""

    def __init__(self, url):
        self._req = HttpRequest()
        self._req.url = url

    def method(self, m):
        self._req.method = m
        return self

    def header(self, key, value):
        self._req.headers[key] = value
        return self

    def body(self, data):
        self._req.body = data
        return self

    def timeout(self, seconds):
        self._req.timeout = seconds
        return self

    def build(self):
        return self._req

req = (RequestBuilder("https://api.example.com/orders")
       .method("POST")
       .header("Content-Type", "application/json")
       .header("Authorization", "Bearer token123")
       .body('{"amount": 99.9}')
       .timeout(10)
       .build())
print(req)
```

运行输出：

```
<请求 POST https://api.example.com/orders headers={'Content-Type': 'application/json', 'Authorization': 'Bearer token123'} body={"amount": 99.9} 超时=10s>
```

读这段代码就像读需求单：方法 POST、加两个头、塞个 JSON 体、超时 10 秒——每一项都自带名字。

### 3.3 对比：与"一堆构造参数"差在哪

同样一个电脑对象，直接构造和用建造者，差别一眼可见（为简洁只列 3 项配置）：

```python
class Computer:
    """直接构造：位置参数"""

    def __init__(self, cpu, memory, gpu):
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu

    def __repr__(self):
        return f"<电脑 {self.cpu} / 内存{self.memory}G / {self.gpu}>"

class ComputerBuilder:
    """建造者：每个配置项都有名字"""

    def __init__(self):
        self._c = Computer(None, None, None)

    def cpu(self, v):
        self._c.cpu = v
        return self

    def memory(self, v):
        self._c.memory = v
        return self

    def gpu(self, v):
        self._c.gpu = v
        return self

    def build(self):
        return self._c

# 方案 A：位置参数——第 3 个到底是显卡还是内存？顺序错了没人拦
pc_a = Computer("i7-13700K", 32, "RTX 4070")

# 方案 B：建造者——每个配置都有名字，读代码像读配置单
pc_b = (ComputerBuilder()
        .cpu("i7-13700K")
        .memory(32)
        .gpu("RTX 4070")
        .build())

print("方案 A：", pc_a)
print("方案 B：", pc_b)
```

运行输出：

```
方案 A： <电脑 i7-13700K / 内存32G / RTX 4070>
方案 B： <电脑 i7-13700K / 内存32G / RTX 4070>
```

---

## 4. Python 特有玩法

### 4.1 `dataclass` + Builder：产品类一行顶十行

Python 的 `dataclass` 自动生成 `__init__`、`__repr__`、`__eq__`，产品类变得极薄，Builder 专心管"分步组装"：

```python
from dataclasses import dataclass, field

@dataclass
class Query:
    """产品：数据库查询。dataclass 自动生成 __init__ 和 __repr__"""
    table: str
    columns: list[str] = field(default_factory=list)
    where: str = ""
    order_by: str = ""
    limit: int = 0

class QueryBuilder:
    def __init__(self, table):
        self._q = Query(table=table)

    def select(self, *cols):
        self._q.columns.extend(cols)
        return self

    def filter(self, condition):
        self._q.where = condition
        return self

    def sort(self, col):
        self._q.order_by = col
        return self

    def take(self, n):
        self._q.limit = n
        return self

    def build(self):
        return self._q

q = (QueryBuilder("orders")
     .select("id", "amount")
     .filter("amount > 100")
     .sort("created_at")
     .take(50)
     .build())
print(q)
print("生成的 SQL：", f"SELECT {', '.join(q.columns)} FROM {q.table} WHERE {q.where} ORDER BY {q.order_by} LIMIT {q.limit}")
```

运行输出：

```
Query(table='orders', columns=['id', 'amount'], where='amount > 100', order_by='created_at', limit=50)
生成的 SQL： SELECT id, amount FROM orders WHERE amount > 100 ORDER BY created_at LIMIT 50
```

注意 `columns: list[str] = field(default_factory=list)`——可变默认值必须用 `field(default_factory=...)`，直接写 `= []` 会让所有实例共享同一个列表（这是个经典 Python 坑）。

### 4.2 不写 Director 直接链式：什么时候才需要 Director？

Python 社区的实际做法是：**大多数情况下不写 Director**（3.2 的 HTTP 请求就是纯链式，没有 Director），调用方自己链式调用就够了。Director 只在两种情况下值得出场：

1. **有大量"固定配方"**：比如报告有 5 种固定模板、披萨有 10 种固定搭配，封装成 Director 方法后，调用方一句话点单（3.1 的 `make_meat_lover` 就是这种）；
2. **构建顺序有强约束**：必须先 A 后 B，防止调用方乱序。

---

## 5. 真实世界中的它

### 框架：Django 的 QuerySet 链式 API

Django 的 `QuerySet` 是建造者思想的教科书案例：`User.objects.filter(age__gt=18).order_by("-id")[:10]`——每一步返回新的 QuerySet，最后才真正执行 SQL（`build()` 的时机是**惰性求值**，只有被迭代时才发查询）。用简单类模拟一下这个"链式攒条件、最后才执行"的套路：

```python
class QuerySet:
    """迷你版 Django QuerySet：每个方法返回"新对象"（不可变链式）"""

    def __init__(self, data, filters=None, order=None):
        self._data = data
        self._filters = filters or []
        self._order = order

    def filter(self, predicate):
        """返回新的 QuerySet，原对象不受影响"""
        return QuerySet(self._data, self._filters + [predicate], self._order)

    def order_by(self, key):
        return QuerySet(self._data, self._filters, key)

    def execute(self):
        """相当于真正发 SQL 的那一下"""
        result = self._data
        for f in self._filters:
            result = [x for x in result if f(x)]
        if self._order:
            result = sorted(result, key=self._order)
        return result

products = [
    {"name": "键盘", "price": 199, "stock": 3},
    {"name": "鼠标", "price": 99, "stock": 20},
    {"name": "显示器", "price": 1299, "stock": 5},
]

qs = (QuerySet(products)
      .filter(lambda p: p["stock"] > 0)
      .filter(lambda p: p["price"] < 1000)
      .order_by(lambda p: p["price"]))
for p in qs.execute():
    print(p)
```

运行输出：

```
{'name': '鼠标', 'price': 99, 'stock': 20}
{'name': '键盘', 'price': 199, 'stock': 3}
```

注意这个版本的 `filter` 返回的是**新对象**而不是改自己——这叫"不可变链式"，每一步都在原基础上派生，旧条件不会串味，比"可变 Builder"更安全。

### 标准库：`argparse` 的 `add_argument` 链式

Python 标准库的 `argparse` 也是建造者思想的体现：`ArgumentParser` 就是 Builder，`add_argument` 就是"分步添加零件"，`parse_args()` 就是最后的 `build()`：

```python
import argparse

parser = argparse.ArgumentParser(description="命令行工具")
parser.add_argument("--host", default="127.0.0.1", help="监听地址")
parser.add_argument("--port", type=int, default=8080, help="端口号")
parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")

# parse_args() 才是"交货"——把攒好的参数解析成对象
args = parser.parse_args(["--port", "9000", "-v"])
print(f"host={args.host} port={args.port} verbose={args.verbose}")
```

运行输出：

```
host=127.0.0.1 port=9000 verbose=True
```

> 真实项目里还有很多建造者的影子：`requests` 用关键字参数拼请求、SQLAlchemy 的查询构造器、`http.client` 的分步构建——套路都是同一个：**分步攒，最后 build**。

---

## 6. 优缺点与适用场景

### 优点

- **可读性**：每个配置项都有方法名，代码即文档；
- **防错**：参数顺序错、漏传都能在"设置时"被发现，而不是最后运行时炸；
- **灵活性**：同一个 Builder 能造出无数种组合的产品；
- **开闭原则**：加一个新配置项，只动 Builder，产品类和调用方都不用改。

### 缺点

- **代码量增加**：每个配置项都要写一个方法，类数量变多；
- **对象可能"半成品"**：Builder 存在期间，产品处于未完成状态，误用会有风险；
- **简单对象没必要**：两个参数的对象用 Builder 是杀鸡用牛刀。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 构造函数参数多（>5 个）且多为可选 | 参数只有两三个 |
| 对象组合方式非常多（披萨、配置、请求） | 对象只有一种固定形态 |
| 构建过程有固定步骤需要复用 | 可以直接用 `**kwargs` 表达清楚的简单场景 |

---

## 7. 与其他模式的关系

- **建造者 vs 工厂**：工厂**一步到位**（`create()` 直接给你成品），建造者**分步定制**（先选这个再选那个，最后 `build()`）。工厂像快餐店"点一份套餐"，建造者像自助餐"自己夹菜"；
- **建造者 vs 原型**：建造者搭出对象后，可以用原型模式**复制**它，批量生成相似对象；
- **建造者 vs 组合**：建造者特别适合构建**树形结构**（文档、目录树、表达式树）——每层节点都是"零件"，`build()` 时拼成整棵树；
- **建造者 + 抽象工厂**：Director 可以搭配不同 Builder 产出不同系列的产品（同一个配方，素食店和肉食店做出来的披萨不一样）。

---

## 8. 常见误区

### 误区 1：把 Builder 写成"带默认参数的大构造函数"

给构造函数加一堆默认参数 ≠ Builder。Builder 的核心是**分步**和**命名**，不是把参数换个位置：

```python
# 反面教材：这只是一个"带默认参数的大构造函数"，不是 Builder
class Config:
    def __init__(self, host="localhost", port=8080, timeout=30, debug=False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.debug = debug

# Builder 的意义在于"分步"和"命名清晰"
class ConfigBuilder:
    def __init__(self):
        self.host = "localhost"
        self.port = 8080
        self.timeout = 30
        self.debug = False

    def with_timeout(self, t):
        self.timeout = t
        return self

    def debug_on(self):
        self.debug = True
        return self

    def build(self):
        return Config(self.host, self.port, self.timeout, self.debug)

c = (ConfigBuilder().with_timeout(60).debug_on().build())
print(f"host={c.host} port={c.port} timeout={c.timeout} debug={c.debug}")
```

运行输出：

```
host=localhost port=8080 timeout=60 debug=True
```

判断标准：调用处能不能"只看一眼就懂配了啥"？大构造函数做不到，Builder 可以。

### 误区 2：Director 过度设计

只有一两个固定配方、调用方自己就记得顺序，硬塞一个 Director 纯属增加类数量。**模式是解决问题的手段，不是必须凑齐的角色清单**——Python 社区里大量 Builder 根本没有 Director，照样工作得很好（3.2 的链式写法就是证明）。等"配方"真的多到记不住时，再请 Director 也不迟。

### 误区 3：可变 Builder 复用导致脏数据

同一个 Builder 连续 build 两次，如果 `build()` 不重置内部状态，第二个产品会带上第一个的残留零件：

```python
class DirtyBuilder:
    """反面教材：build 后不重置，复用会串数据"""

    def __init__(self):
        self.parts = []

    def add(self, part):
        self.parts.append(part)
        return self

    def build(self):
        return self.parts    # 直接把内部列表交出去

b = DirtyBuilder()
first = b.add("CPU").add("内存").build()
second = b.add("显卡").build()          # 复用同一个 builder
print("第一个：", first)
print("第二个：", second)
```

运行输出：

```
第一个： ['CPU', '内存', '显卡']
第二个： ['CPU', '内存', '显卡']
```

更糟的是：因为 `build()` 把内部列表直接交了出去，`first` 和 Builder 内部共享同一个列表——后面 `add("显卡")` 把**第一个产品也污染了**。修复办法有两种：**`build()` 时重置内部状态**（见 3.1 的 `self._pizza = Pizza()`），并且返回产品副本而不是内部列表；或者**每次构建都新建一个 Builder**。

---

## 9. 练习题

### 练习 1：给"优惠券"写一个建造者

优惠券有标题、折扣金额、有效期、适用范围四个可选项，用链式 Builder 构造一张"新人专享"优惠券：

```python
# 答案：链式建造者
class Coupon:
    def __init__(self, title, discount, expire_days, scope):
        self.title = title
        self.discount = discount
        self.expire_days = expire_days
        self.scope = scope

    def __repr__(self):
        return f"<优惠券 {self.title} 立减{self.discount}元 有效期{self.expire_days}天 适用{self.scope}>"

class CouponBuilder:
    def __init__(self):
        self.title = "通用优惠券"
        self.discount = 0
        self.expire_days = 7
        self.scope = "全店"

    def named(self, title):
        self.title = title
        return self

    def cut(self, amount):
        self.discount = amount
        return self

    def valid_for(self, days):
        self.expire_days = days
        return self

    def only_for(self, scope):
        self.scope = scope
        return self

    def build(self):
        return Coupon(self.title, self.discount, self.expire_days, self.scope)

coupon = (CouponBuilder()
          .named("新人专享")
          .cut(20)
          .valid_for(30)
          .only_for("数码类")
          .build())
print(coupon)
```

运行输出：

```
<优惠券 新人专享 立减20元 有效期30天 适用数码类>
```

### 练习 2：写一个搜索条件构造器

实现 `SearchBuilder`，支持链式添加关键词、分类、价格区间，最后 `build()` 出条件字典：

```python
# 答案：
class SearchBuilder:
    def __init__(self):
        self._cond = {"keyword": "", "category": None, "min_price": None, "max_price": None}

    def keyword(self, kw):
        self._cond["keyword"] = kw
        return self

    def category(self, c):
        self._cond["category"] = c
        return self

    def price_range(self, low, high):
        self._cond["min_price"] = low
        self._cond["max_price"] = high
        return self

    def build(self):
        return dict(self._cond)     # 返回副本，防止外部改到内部

cond = (SearchBuilder()
        .keyword("机械键盘")
        .category("外设")
        .price_range(100, 500)
        .build())
print(cond)
```

运行输出：

```
{'keyword': '机械键盘', 'category': '外设', 'min_price': 100, 'max_price': 500}
```

### 练习 3：修复 Builder 复用的脏数据问题

下面的 Builder 连续 build 两次会串数据，请修复（提示：`build()` 时重置，或返回副本）：

```python
# 答案：build 时返回副本并重置内部状态
class SmoothieBuilder:
    """果汁 builder：连续做两杯互不干扰"""

    def __init__(self):
        self.ingredients = []

    def add(self, item):
        self.ingredients.append(item)
        return self

    def build(self):
        result = list(self.ingredients)   # 返回副本，外部改不到内部
        self.ingredients = []             # 重置，下一杯从零开始
        return result

b = SmoothieBuilder()
print("第一杯：", b.add("草莓").add("酸奶").build())
print("第二杯：", b.add("芒果").add("牛奶").build())
```

运行输出：

```
第一杯： ['草莓', '酸奶']
第二杯： ['芒果', '牛奶']
```

---

## 10. 小结与口诀

> **口诀：复杂对象分步搭，链式方法一把梭；最后一步才交货，复用之前要重置。**

建造者模式解决的痛点是"构造函数参数爆炸"：把"搭积木"变成一串有名字的步骤，最后 `build()` 交货。记住三条：

1. 配置项多且可选 → 上 Builder，方法名就是文档；
2. 默认**不写 Director**，配方真的多了再请它出山；
3. `build()` 要**重置状态**（或每次新建 Builder），防止复用串数据。

下一章，我们来看结构型模式里的"经纪人"——**代理模式**：经纪人替你办事，该拦的拦，该等的等，该转的转。

---

*本章金句：建造者的优雅在于"最后一步才交货"——过程可以分步试错，结果必须一步到位。*
