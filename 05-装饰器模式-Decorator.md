# 第 5 章 装饰器模式（Decorator）

> **一句话总结**：一层层包装，不动原物，功能叠加。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 结构型 | ★★★☆☆ | ★★★★★ |

---

## 1. 引子：先讲个故事

新手机到手，你第一件事是什么？贴膜、套壳、挂绳——**手机本体一个零件没动，功能却一层层加上去**：膜防刮、壳防摔、挂绳防丢。哪天不喜欢挂绳了，摘掉就行，手机还是那个手机。

写代码也一样。你的"下单"函数是核心业务，结果产品经理的需求一个接一个来：先要记日志，再要权限校验，说不定还要计时、要缓存、要重试。如果你把这些**全都写进函数里**，核心业务就会被杂七杂八的逻辑淹没：

```python
# 引子：没有装饰器的世界——需求一个一个来，函数越改越臃肿
def order(user: str, product: str) -> str:
    # 需求 1：加日志
    print(f"[日志] {user} 下单 {product}")
    # 需求 2：加权限校验（插在业务中间）
    if user == "黑名单用户":
        return "下单失败：无权限"
    # —— 核心业务 ——
    return f"订单创建成功：{product}"


print(order("小明", "键盘"))
print(order("黑名单用户", "鼠标"))
```

运行输出：

```
[日志] 小明 下单 键盘
订单创建成功：键盘
[日志] 黑名单用户 下单 鼠标
下单失败：无权限
```

更糟的是：这些"附加功能"**别的函数也要用**（退款要记日志、改价要校验权限），你只能复制粘贴，改一处漏十处。**装饰器模式**就是来治这个病的：像贴膜一样，把附加功能"包"在函数外面，原函数一行不改，功能随便叠加、随时拆卸。

---

## 2. 模式登场

### 定义

> **装饰器模式（Decorator）**：动态地给一个对象（或函数）添加额外的职责，而不改变它本身。就增加功能来说，装饰器比生成子类更灵活。

### 核心思想

Python 里的装饰器，本质就一句话：**一个接收函数、返回新函数的函数**。`@` 语法糖只是把它写得更优雅：

```python
# @log 等价于：
# order = log(order)
```

装饰器返回的"包装函数"在调用原函数**前后**插入附加逻辑——就像贴膜在手机外面，但手机还是那个手机。

### 结构

```
┌────────────────────────────────┐
│       Component（组件接口）       │
│   + operation()                │
└───────────────┬────────────────┘
                │
    ┌───────────┴───────────┐
    ▼                       ▼
┌──────────────┐      ┌─────────────────┐
│  核心对象      │      │   Decorator     │
│  operation() │      │  （装饰器）       │
└──────────────┘      ├─────────────────┤
                      │ - wrapped       │ ← 持有被装饰对象
                      │ + operation()   │
                      └────────┬────────┘
                               │ 具体装饰器：日志 / 计时 / 缓存……
                               ▼
                        ┌──────────────┐
                        │ 具体装饰器     │
                        │（包装 + 增强）  │
                        └──────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **组件（Component）** | 被装饰对象的抽象（Python 里常常省略） |
| **核心对象** | 真正的业务逻辑：被装饰的原函数/原对象 |
| **装饰器（Decorator）** | 持有一个"被包装者"的引用 |
| **具体装饰器** | 在调用被包装者前后附加功能（日志、计时、缓存……） |

---

## 3. Python 实现

### 3.1 装饰器的本质：函数接收函数，返回函数

先不看 `@`，手写一次包装，把机制看清楚：

```python
def add_logging(func):
    """包装函数：调用前打日志"""
    def wrapper(*args, **kwargs):
        print(f"[日志] 调用 {func.__name__}，参数 {args}")
        return func(*args, **kwargs)
    return wrapper


def add(a: int, b: int) -> int:
    return a + b


add_with_log = add_logging(add)      # 手动包装：add 本体没动
print("结果：", add_with_log(1, 2))
print("原函数还是原函数：", add(1, 2))
```

运行输出：

```
[日志] 调用 add，参数 (1, 2)
结果： 3
原函数还是原函数： 3
```

`add_logging` 接收 `add`，返回 `wrapper`；`wrapper` 在调用 `add` 前先打日志。**`add` 本身一行没改**——这就是"贴膜不拆机"。

### 3.2 `@` 语法糖：日志 + 权限，一层层包

回到引子的下单场景，用装饰器重写——日志、权限各自独立成装饰器：

```python
import functools


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[日志] 调用 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def check_permission(func):
    """权限校验装饰器：黑名单用户直接拒绝"""
    BLACKLIST = {"黑名单用户"}

    @functools.wraps(func)
    def wrapper(user: str, *args, **kwargs):
        if user in BLACKLIST:
            return "下单失败：无权限"
        return func(user, *args, **kwargs)
    return wrapper


@log
@check_permission
def order(user: str, product: str) -> str:
    return f"订单创建成功：{product}（下单人：{user}）"


print(order("小明", "键盘"))
print(order("黑名单用户", "鼠标"))
```

运行输出：

```
[日志] 调用 order
订单创建成功：键盘（下单人：小明）
[日志] 调用 order
下单失败：无权限
```

`order` 函数本身只剩核心业务。加个新功能？写个新装饰器叠上去就行；不想要了？摘掉 `@` 那一行——**开闭原则**：对扩展开放，对修改关闭。

### 3.3 带参数的装饰器：三层函数

`@repeat(3)` 这种带参数的装饰器，比普通装饰器多一层——**外层收参数、中层收函数、内层收调用参数**：

```python
def repeat(times: int):
    """装饰器工厂：让函数重复执行 times 次"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper

    return decorator


@repeat(3)
def roll_dice() -> str:
    return "🎲 掷出 6 点"


print(roll_dice())
```

运行输出：

```
['🎲 掷出 6 点', '🎲 掷出 6 点', '🎲 掷出 6 点']
```

记不住三层？口诀：**参数 → 函数 → 调用参数**，一层套一层，像套娃。

### 3.4 叠加顺序：从下往上包装，从外到内执行

多个装饰器叠在一起时，顺序有讲究——**`@` 越靠下越先包装（离函数越近），调用时越先执行**：

```python
def layer_a(func):
    def wrapper(*args, **kwargs):
        print("进入 A（最外层）")
        result = func(*args, **kwargs)
        print("离开 A（最外层）")
        return result
    return wrapper


def layer_b(func):
    def wrapper(*args, **kwargs):
        print("进入 B")
        result = func(*args, **kwargs)
        print("离开 B")
        return result
    return wrapper


@layer_a
@layer_b
def core():
    print("核心业务执行中")


core()
```

运行输出：

```
进入 A（最外层）
进入 B
核心业务执行中
离开 B
离开 A（最外层）
```

看输出顺序：**A 包着 B，B 包着 core**。执行时 A 先进、B 再进、core 执行、B 退出、A 退出——像剥洋葱，也像穿衣服：先穿内衣（B），再穿外套（A），脱的时候先脱外套。

---

## 4. Python 特有玩法

### 4.1 `functools.wraps`：保住函数的"身份证"

包装函数有个副作用：原函数的 `__name__`、`__doc__` 会被 `wrapper` 顶替。`functools.wraps` 就是来"过户"的：

```python
import functools


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@log
def hello():
    """我是 hello 函数的文档"""
    return "你好"


print("函数名：", hello.__name__)
print("文档：", hello.__doc__)
```

运行输出：

```
函数名： hello
文档： 我是 hello 函数的文档
```

**写装饰器，第一行就写 `@functools.wraps(func)`**——这是 Python 社区的共识。

### 4.2 用类实现装饰器：`__call__`

装饰器不一定是函数，**类也可以**——`__init__` 收函数，`__call__` 让实例像函数一样被调用。好处：可以在实例上存状态：

```python
import functools


class CountCalls:
    """类装饰器：统计函数被调用了多少次"""

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        print(f"第 {self.calls} 次调用 {self.func.__name__}")
        return self.func(*args, **kwargs)


@CountCalls
def ping():
    return "pong"


print(ping())
print(ping())
print(ping())
```

运行输出：

```
第 1 次调用 ping
pong
第 2 次调用 ping
pong
第 3 次调用 ping
pong
```

### 4.3 装饰器也能装饰类

装饰器的"被包装者"不限于函数——**类也能被装饰**，批量给类加功能：

```python
def add_repr(cls):
    """类装饰器：自动生成 __repr__（列出所有实例属性）"""
    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls


@add_repr
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


u = User("小明", 18)
print(u)               # 没写 __repr__，但装饰器给补上了
```

运行输出：

```
User(name=小明, age=18)
```

### 4.4 内置装饰器：`@property` / `@staticmethod`

Python 标准库本身就是装饰器大户——`@property` 把方法变成属性、`@staticmethod` 把方法变成静态方法，全是"不改原函数、只改调用方式"：

```python
class Circle:
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def area(self) -> float:
        """把方法变成属性：调用时不加括号"""
        return 3.14159 * self._radius ** 2

    @staticmethod
    def describe() -> str:
        """静态方法：不依赖实例"""
        return "我是一个圆"


c = Circle(2.0)
print("面积（当属性用）：", c.area)
print("静态方法：", Circle.describe())
```

运行输出：

```
面积（当属性用）： 12.56636
静态方法： 我是一个圆
```

---

## 5. 真实世界中的它

### `functools.lru_cache`：标准库的"缓存装饰器"

最常用的标准库装饰器之一：给函数加缓存，相同参数不重复计算：

```python
import functools


@functools.lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print("fib(40) =", fib(40))
print("缓存统计：", fib.cache_info())
```

运行输出：

```
fib(40) = 102334155
缓存统计： CacheInfo(hits=38, misses=41, maxsize=None, currsize=41)
```

没加缓存时 `fib(40)` 的重复计算量以亿计（约 3.3 亿次递归调用）；加上一行 `@lru_cache`，立刻变成 41 次计算 + 38 次命中——**一行装饰器，性能起飞**。

### `@dataclass`：一行生成 `__init__`/`__repr__`/`__eq__`

`dataclasses.dataclass` 是"装饰类"的典范——你只写字段，它自动生成构造、显示、比较方法：

```python
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    stock: int = 0


p1 = Product("键盘", 199.0, 50)
p2 = Product("键盘", 199.0, 50)
print("自动生成的 __init__ 和 __repr__：", p1)
print("自动生成的 __eq__：", p1 == p2)
```

运行输出：

```
自动生成的 __init__ 和 __repr__： Product(name='键盘', price=199.0, stock=50)
自动生成的 __eq__： True
```

### Flask 的路由装饰器（文字提及）

Flask 里你天天写的 `@app.route("/")` 就是装饰器模式：**装饰器把"这个 URL 对应这个函数"的注册信息附加到视图函数上**，视图函数本身一行不改。Django 的 `@login_required`、`@cache_page` 同理——框架用装饰器把"横切关注点"从业务函数里剥离。

---

## 6. 优缺点与适用场景

### 优点

- **核心逻辑零侵入**：原函数一行不改；
- **功能可叠加、可拆卸**：加功能 = 加装饰器，去功能 = 删一行；
- **符合单一职责**：每个装饰器只干一件事；
- **Python 原生支持**：`@` 语法糖 + 标准库大量内置。

### 缺点

- **调用链变长**：装饰器多了，排查问题时得一层层剥洋葱；
- **顺序敏感**：装饰器顺序不同，行为可能不同；
- **过度使用会"魔法化"**：满屏 `@` 会让新人看不懂执行顺序。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 横切关注点：日志、计时、缓存、权限、校验 | 核心业务逻辑本身（别把业务写进装饰器） |
| 多个函数共享同一附加功能 | 只需要一两次的简单包装 |
| 功能需要灵活叠加/拆卸 | 装饰器顺序影响正确性且难调试的场景 |
| 框架的路由/中间件式扩展 | 被包装者本身很简单，包装反而绕 |

---

## 7. 与其他模式的关系

- **装饰器 vs 代理**：长得像，心思不同。装饰器是**增强**功能（贴膜：加功能），代理是**控制**访问（经纪人：管你能不能见到明星）——第 12 章会细讲。
- **装饰器 vs 组合**：装饰器本质是"单链组合"——一个包一个，串成链（第 17 章讲树形组合，装饰器是它的线性版本）。
- **装饰器 vs 适配器**：适配器**改接口**（换个插头），装饰器**加功能不改接口**（贴个膜）。
- **装饰器 vs 继承**：给类加 N 种功能，继承要写 2^N 个子类，装饰器组合 N 个就行——"组合优于继承"的活教材。

---

## 8. 常见误区

### 误区 1：忘了 `functools.wraps`，函数"身份证"丢了

不包 `wraps`，被装饰函数的名字、文档全被 `wrapper` 顶替——调试、文档生成、序列化都会出问题：

```python
def log_bad(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@log_bad
def hello():
    """你好函数"""
    return "你好"


print("函数名变成了：", hello.__name__)   # 应该是 hello，却是 wrapper
print("文档也没了：", hello.__doc__)
```

运行输出：

```
函数名变成了： wrapper
文档也没了： None
```

### 误区 2：搞不清叠加顺序

有人以为 `@a @b` 是"先执行 a 再执行 b"——错！**`@a @b` 等价于 `a(b(func))`**，`b` 先包装、离函数最近，执行时 `a` 先进入（见 3.4 的洋葱演示）。顺序反了，日志和权限的执行先后就反了——**写多装饰器时，把"靠近函数"的当成"最里层的内衣"来想**。

### 误区 3：包装函数忘了透传参数

装饰器里调用原函数时，**必须把 `*args, **kwargs` 原样传下去**。少传一个，装饰后的函数一调用就炸：

```python
def log(func):
    def wrapper(*args, **kwargs):
        print("记录日志...")
        return func()              # 忘了把参数传下去！
    return wrapper


@log
def greet(name: str) -> str:
    return f"你好，{name}"


try:
    greet("小明")
except TypeError as e:
    print("报错：", e)
```

运行输出：

```
记录日志...
报错： greet() missing 1 required positional argument: 'name'
```

---

## 9. 练习题

### 练习 1：写一个 `retry` 重试装饰器

函数抛异常时自动重试，最多重试 `times` 次：

```python
def retry(times: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ValueError as e:
                    print(f"第 {attempt} 次失败：{e}")
            raise ValueError(f"重试 {times} 次仍失败")
        return wrapper
    return decorator


@retry(3)
def flaky():
    """前两次失败，第三次成功"""
    flaky.calls = getattr(flaky, "calls", 0) + 1
    if flaky.calls < 3:
        raise ValueError("网络抖动")
    return "请求成功"


print(flaky())
```

运行输出：

```
第 1 次失败：网络抖动
第 2 次失败：网络抖动
请求成功
```

### 练习 2：手写一个简单的 `memoize` 缓存装饰器

用字典缓存"参数 → 结果"，相同参数不再重复计算：

```python
def memoize(func):
    cache = {}

    def wrapper(n: int) -> int:
        if n not in cache:
            cache[n] = func(n)
            print(f"计算 fib({n})")
        return cache[n]
    return wrapper


@memoize
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print("fib(6) =", fib(6))
```

运行输出：

```
计算 fib(1)
计算 fib(0)
计算 fib(2)
计算 fib(3)
计算 fib(4)
计算 fib(5)
计算 fib(6)
fib(6) = 8
```

### 练习 3：写一个 `require_role` 权限装饰器

角色不在白名单里就直接拒绝，不执行原函数：

```python
def require_role(allowed_roles):
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if user["role"] not in allowed_roles:
                return f"拒绝访问：{user['name']} 没有权限（需要角色：{'/'.join(allowed_roles)}）"
            return func(user, *args, **kwargs)
        return wrapper
    return decorator


@require_role(["admin"])
def delete_user(user, target: str) -> str:
    return f"{user['name']} 删除了用户 {target}"


admin = {"name": "管理员", "role": "admin"}
guest = {"name": "访客", "role": "guest"}
print(delete_user(admin, "小明"))
print(delete_user(guest, "小明"))
```

运行输出：

```
管理员 删除了用户 小明
拒绝访问：访客 没有权限（需要角色：admin）
```

---

## 10. 小结与口诀

> **口诀：包装不动原函数，功能一层层；wraps 保身份，顺序如洋葱。**

装饰器模式是 Python 里"语法即模式"的代表——你写的每个 `@` 都是在用装饰器模式。记住三条：

1. **装饰器本质**：接收函数、返回函数；`@` 只是语法糖；
2. **写装饰器第一行就 `@functools.wraps(func)`**，保住原函数身份；
3. **叠加顺序**：从下往上包装、从外到内执行，想清楚再叠。

下一章，我们来看另一个"门面"级别的结构型模式——**外观模式**：一个前台，搞定一切。

---

*本章金句：装饰器是"贴膜不拆机"——核心逻辑永远干净，附加功能随贴随撕。*
