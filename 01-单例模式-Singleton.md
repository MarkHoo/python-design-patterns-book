# 第 1 章 单例模式（Singleton）

> **一句话总结**：保证一个类只有一个实例，并提供一个全局访问点。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 创建型 | ★☆☆☆☆ | ★★★★★ |

---

## 1. 引子：先讲个故事

想象你是一家创业公司的老板，公司只有一个打印机。按理说全公司应该共用这一台，结果你的员工小李自己买了一台，行政小王也自己买了一台，财务部又添了一台……每台打印机里存着不同的通讯录，小李更新了通讯录，其他人用的还是旧版——全公司乱成一锅粥。

程序世界里的"打印机"就是那些**整个程序只能有一份的资源**：配置文件、日志器、数据库连接池、线程池。如果不加约束，每个人各 new 一个，就会出现"改了白改"的诡异 bug：

```python
# 引子：没有单例的世界——配置文件各改各的
class ConfigManager:
    def __init__(self):
        self._config = {"theme": "light"}

    def set(self, key, value):
        self._config[key] = value

    def get(self, key):
        return self._config.get(key)


# 模块 A：想换主题
config_a = ConfigManager()
config_a.set("theme", "dark")

# 模块 B：完全不知情，拿到的还是旧配置
config_b = ConfigManager()
print("模块 B 看到的主题：", config_b.get("theme"))  # 还是 light，A 白改了
```

运行输出：

```
模块 B 看到的主题： light
```

问题出在哪？`config_a` 和 `config_b` 是两个**互不相干的对象**，各持一份配置。**单例模式**就是来解决这类问题的：全程序只允许存在一个实例，谁拿都是它。

---

## 2. 模式登场

### 定义

> **单例模式**：确保一个类只有一个实例，并提供一个访问它的全局点。

### 解决的问题

1. **实例唯一性**：配置、日志、连接池这类资源，多实例会互相打架；
2. **访问一致性**：所有调用方拿到的都是同一个对象，改一处，处处可见；
3. **节省资源**：昂贵的对象（数据库连接）只创建一次。

### 结构

```
┌───────────────────────────┐
│         Singleton          │
├───────────────────────────┤
│ - _instance: Singleton     │  ← 类属性：保存唯一实例
├───────────────────────────┤
│ + __new__(cls)             │  ← 创建拦截点：有则返回，无则建
│ + business_method()        │
└───────────────────────────┘
        ▲
        │ 每次调用都返回同一个 _instance
        │
   ┌──────────┐
   │  客户端    │  通过 Singleton() 或 get_instance() 获取
   └──────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **单例类** | 自己管自己的唯一实例（`_instance` 类属性 + 创建拦截） |
| **唯一实例** | 进程内仅此一份 |
| **全局访问点** | 客户端拿实例的统一入口 |
| **客户端** | 只管调用，不关心实例怎么来的 |

---

## 3. Python 实现

### 3.1 经典版：用 `__new__` 拦截创建

Python 里创建对象走两步：`__new__`（分配内存）→ `__init__`（初始化）。在 `__new__` 里做拦截，就能保证"只 new 一次"：

```python
class ConfigManager:
    """经典单例：用 __new__ 控制实例创建"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:                    # 还没有实例？
            cls._instance = super().__new__(cls)     # 创建唯一的一个
            cls._instance._init_config()             # 只在首次创建时初始化
        return cls._instance

    def _init_config(self) -> None:
        self._config = {"theme": "light", "lang": "zh"}

    def get(self, key: str):
        return self._config.get(key)

    def set(self, key: str, value) -> None:
        self._config[key] = value


a = ConfigManager()
b = ConfigManager()
print("a is b（同一个实例吗）:", a is b)

a.set("theme", "dark")
print("b 能看到 a 的修改:", b.get("theme"))
```

运行输出：

```
a is b（同一个实例吗）: True
b 能看到 a 的修改: dark
```

**关键点**：把初始化放进 `__new__` 里（而不是 `__init__`），因为 `__init__` 每次调用都会执行——后面"常见误区"里会演示这个坑。

### 3.2 懒加载版：第一次用的时候才创建

有些对象很贵（数据库连接、大模型），希望"模块导入时什么都不干，第一次真正用到才创建"：

```python
class BigResource:
    def __init__(self):
        print("BigResource 创建了（很贵的资源，比如数据库连接）")


_resource = None

def get_resource() -> BigResource:
    """懒加载：第一次调用才真正创建"""
    global _resource
    if _resource is None:
        _resource = BigResource()
    return _resource


print("模块已导入，但资源还没有创建")
r1 = get_resource()   # 这一刻才创建
r2 = get_resource()   # 直接返回已有的
print("r1 is r2:", r1 is r2)
```

运行输出：

```
模块已导入，但资源还没有创建
BigResource 创建了（很贵的资源，比如数据库连接）
r1 is r2: True
```

### 3.3 线程安全版：多线程环境下也不翻车

经典版有个隐患：两个线程同时发现 `_instance is None`，会各自 new 一个。解决方法是加锁 + **双重检查**：

```python
import threading


class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:        # 第一次检查：不加锁，快路径
            with cls._lock:              # 拿到锁
                if cls._instance is None:  # 第二次检查：防止重复创建
                    cls._instance = super().__new__(cls)
        return cls._instance


def worker(results):
    results.append(ThreadSafeSingleton())


results = []
threads = [threading.Thread(target=worker, args=(results,)) for _ in range(8)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("8 个线程拿到的都是同一个实例:", len({id(r) for r in results}) == 1)
```

运行输出：

```
8 个线程拿到的都是同一个实例: True
```

> **为什么双重检查？** 第一道不加锁的判断让"已经创建好"的情况直接返回，避免每次调用都抢锁（性能）；第二道加锁的判断保证"并发首次创建"时只有一个线程真正 new。

### 3.4 元类版：从"源头"上禁止重复创建

元类（metaclass）是"创建类的类"。`SingletonMeta.__call__` 控制的是**调用类时的行为**——`Logger()` 这个动作本身就被拦截了：

```python
class SingletonMeta(type):
    """元类版单例：所有用这个元类的类自动成为单例"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:              # 这个类还没有实例？
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    def __init__(self, name: str = "default"):
        print(f"初始化 Logger：{name}")   # 注意：只打印一次
        self.name = name


l1 = Logger("app")
l2 = Logger("app")
l3 = Logger("other")
print("l1 is l2:", l1 is l2)
print("l1 is l3:", l1 is l3, "（第二次传参被忽略，name 仍是第一次的）")
```

运行输出：

```
初始化 Logger：app
l1 is l2: True
l1 is l3: True （第二次传参被忽略，name 仍是第一次的）
```

元类版的好处：`__init__` 只执行一次，且**写业务类时完全无感知**（不用在类里写任何单例代码）。

---

## 4. Python 特有玩法

### 4.1 模块即单例（Python 社区最推崇的方式）

Python 有个天然机制：**一个模块在进程内只会被执行一次**（`sys.modules` 负责缓存）。所以"模块顶层的实例"天然就是单例，连 `__new__` 都不用写：

```python
# 把下面代码存成 settings.py，任何地方写 `from settings import settings`
# 拿到的都是同一个实例——这是 Python 里最地道的"单例"
class Settings:
    def __init__(self):
        self.debug: bool = True
        self.host: str = "127.0.0.1"

    def __repr__(self):
        return f"<Settings debug={self.debug} host={self.host}>"


# 模块顶层只执行一次，这就是那个"独一份"
settings = Settings()

# 模拟两个调用方各自 import（真实项目里就是 from settings import settings）
caller_a = settings
caller_b = settings
print("两边是同一个对象:", caller_a is caller_b)
print(caller_b)
```

运行输出：

```
两边是同一个对象: True
<Settings debug=True host=127.0.0.1>
```

**这是本书推荐的默认方案**：简单、无魔法、好测试。

### 4.2 类装饰器版：一行注解搞定

想给多个类快速套上单例？装饰器是 Python 的"批量生产工具"：

```python
import functools


def singleton(cls):
    """类装饰器：把任意类变成单例"""
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if wrapper.instance is None:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper


@singleton
class Cache:
    def __init__(self):
        self.data = {}


c1 = Cache()
c2 = Cache()
print("c1 is c2:", c1 is c2)
```

运行输出：

```
c1 is c2: True
```

### 4.3 `functools.lru_cache` 版："按参数区分"的单例

有时候我们想要的不是"全局一个"，而是"**每个参数组合一个**"——这就是连接池/注册表的典型需求：

```python
import functools


class ConnectionPool:
    def __init__(self, url: str):
        self.url = url
        self._conns = []

    def add(self, conn: str) -> None:
        self._conns.append(conn)

    def __repr__(self):
        return f"<Pool {self.url} 连接数={len(self._conns)}>"


@functools.lru_cache(maxsize=None)
def get_pool(url: str) -> ConnectionPool:
    print(f"新建连接池：{url}")
    return ConnectionPool(url)


p1 = get_pool("mysql://主库")
p2 = get_pool("mysql://主库")
p3 = get_pool("mysql://读库")
p1.add("conn-1")
print("同 URL 共享同一池:", p1 is p2)
print("不同 URL 各自独立:", p1 is not p3)
print("p2 能看到 p1 添加的连接:", p2)
```

运行输出：

```
新建连接池：mysql://主库
新建连接池：mysql://读库
同 URL 共享同一池: True
不同 URL 各自独立: True
p2 能看到 p1 添加的连接: <Pool mysql://主库 连接数=1>
```

---

## 5. 真实世界中的它

### 标准库：`logging.getLogger`

Python 标准库的 `logging` 模块就内置了一个"注册表式单例"：`getLogger(name)` 对同名 name 永远返回同一个 logger 对象：

```python
import logging

# getLogger 内部维护了一张 {名字: logger} 的表，
# 同名返回同一个对象——这就是单例思想（每个名字一个实例）
app_logger_a = logging.getLogger("my_app")
app_logger_b = logging.getLogger("my_app")
other_logger = logging.getLogger("other_app")

print("同名 logger 是同一个对象:", app_logger_a is app_logger_b)
print("不同名 logger 各自独立:", app_logger_a is other_logger)
```

运行输出：

```
同名 logger 是同一个对象: True
不同名 logger 各自独立: False
```

你写的 `logging.getLogger(__name__)` 能"处处拿到同一个 logger"，靠的就是这个机制。

### 框架：Django 的 `settings`

Django 的配置对象 `django.conf.settings` 是经典的单例：全项目任何地方 `from django.conf import settings` 拿到的都是同一个配置对象，且实现了懒加载（第一次访问才读取配置文件）。`django.utils.functional.LazyObject` 就是为这类场景设计的工具类。

### 解释器层面：小整数与 `None`

Python 解释器自己也是"单例狂魔"：`None`、`True`、`False` 全局唯一（所以你能写 `x is None`）；小整数（CPython 中通常是 -5～256）也做了缓存——`256 is 256` 为 `True`。这些都是解释器层面的"单例"。

---

## 6. 优缺点与适用场景

### 优点

- **保证唯一**：全局只有一份，杜绝"改了两处，只生效一处"；
- **统一入口**：访问点明确，调用方代码简洁；
- **节省资源**：昂贵对象只建一次；
- **懒加载**：可以推迟到真正使用时才创建。

### 缺点（Python 开发者尤其要警惕）

- **全局状态是测试的天敌**：单例对象会在测试用例之间"串味"，污染测试数据；
- **隐藏依赖**：类内部直接拿单例，导致依赖关系不透明，难以替换（比如测试时想换个假的数据库）；
- **多线程**：不加锁的实现有并发风险；
- **过度使用**：很多"单例"其实只需要一个模块级变量。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 配置中心（settings/config） | 有状态、需要频繁重置的对象 |
| 日志器、监控上报器 | 需要多实例才能测试的场景 |
| 连接池、线程池、缓存 | 可以用依赖注入替代的地方 |
| 全局计数器、ID 生成器 | 只是"不想传参"的偷懒场景 |

> **Python 圈的共识**：能用模块级变量就用模块级变量，能依赖注入就依赖注入；"单例类"留给确实需要"类"的场合（比如需要继承、需要懒加载的复杂资源）。

---

## 7. 与其他模式的关系

- **单例 + 工厂**：工厂方法/抽象工厂的"注册表"常常用单例实现（比如日志器工厂）；
- **单例 + 外观**：外观对象常常设计成单例（一个系统一个门面）；
- **单例 + 状态**：状态机中的"上下文"常是单例；
- **单例 vs 原型**：单例是"只造一个"，原型是"造很多个拷贝"，正好相反；
- **单例 vs 享元**：享元是"共享多个实例"，单例是"共享一个实例"，理念相近但粒度不同。

---

## 8. 常见误区

### 误区 1：以为 `__init__` 只执行一次

`__new__` 拦得住"创建"，拦不住"初始化"——每次 `Singleton()` 都会重新跑一遍 `__init__`：

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print("__init__ 又被调用了一次！")


s1 = Singleton()
s2 = Singleton()
```

运行输出：

```
__init__ 又被调用了一次！
__init__ 又被调用了一次！
```

如果 `__init__` 里有重置状态的逻辑，单例就会被悄悄"重置"。解决：初始化放 `__new__`（见 3.1），或者用元类版（见 3.4）。

### 误区 2：多线程环境下"偶尔"出现两个实例

经典版在并发首次创建时可能被 new 出两个（见 3.3 的演示）。**"大多数时候对"和"永远对"是两码事**——线上 bug 往往就是那 0.1% 的概率。

### 误区 3：以为单例可以随便子类化

单例 + 继承是个大坑：子类和父类的 `_instance` 是同一个类属性，容易串实例。若确有继承需求，优先考虑元类版（每个类在 `_instances` 字典里有独立条目）。

### 误区 4：用 `pickle`/`copy` 绕过单例

反序列化会**绕过 `__new__`**，直接造出新实例。需要用 pickle 的单例，得自己实现 `__reduce__` 返回现有实例——一般不建议自找麻烦，序列化单例前先想清楚它是不是真的需要是单例。

### 误区 5：把"单例"当成"全局变量"的遮羞布

单例本质是全局状态。如果只是想"少传几个参数"，那是在用单例掩盖设计问题——优先考虑依赖注入或模块级变量。

---

## 9. 练习题

### 练习 1：修复线程安全隐患

下面的 `SafeConfig` 单例在多线程下可能被创建两次，请加锁修复：

```python
import threading


class SafeConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# 答案：加锁 + 双重检查
class SafeConfig:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance


instances = []
threads = [threading.Thread(target=lambda: instances.append(SafeConfig())) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print("10 个线程拿到同一实例:", len({id(i) for i in instances}) == 1)
```

运行输出：

```
10 个线程拿到同一实例: True
```

### 练习 2：用"模块级变量"重写单例

把下面的类改造成模块级单例的写法（提示：实例放在模块顶层）：

```python
# 答案：模块级单例（真实项目里存成 cache.py，然后 `from cache import cache`）
class Cache:
    def __init__(self):
        self._store = {}

    def put(self, key, value):
        self._store[key] = value

    def get(self, key):
        return self._store.get(key)


cache = Cache()  # 模块顶层只执行一次 → 天然单例

# 模拟两个调用方各自 import
caller_a = cache
caller_b = cache
caller_a.put("user:1", "小明")
print("调用方 B 能看到 A 写入的数据:", caller_b.get("user:1"))
print("两边是同一个对象:", caller_a is caller_b)
```

运行输出：

```
调用方 B 能看到 A 写入的数据: 小明
两边是同一个对象: True
```

### 练习 3：用 `lru_cache` 实现"每个参数一个实例"的注册表

实现一个 `get_driver(db_name)`，同一个 `db_name` 永远返回同一个驱动对象，不同名字各自独立：

```python
# 答案：functools.lru_cache 天然就是"按参数去重"的注册表
import functools


class Driver:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.sessions = 0

    def connect(self):
        self.sessions += 1
        return f"{self.db_name} 第 {self.sessions} 个会话"


@functools.lru_cache(maxsize=None)
def get_driver(db_name: str) -> Driver:
    print(f"创建驱动：{db_name}")
    return Driver(db_name)


d1 = get_driver("订单库")
d2 = get_driver("订单库")
d3 = get_driver("用户库")
d1.connect()
print("同库共享驱动:", d1 is d2)
print("不同库独立:", d1 is not d3)
print("d2.connect():", d2.connect(), "（会话数共享，证明是同一个）")
```

运行输出：

```
创建驱动：订单库
创建驱动：用户库
同库共享驱动: True
不同库独立: True
d2.connect(): 订单库 第 2 个会话 （会话数共享，证明是同一个）
```

---

## 10. 小结与口诀

> **口诀：独一份，全局拿；多线程，锁一下；Python 里，模块化。**

单例模式是设计模式里"最简单也最受争议"的一个：实现简单，但全局状态带来的测试问题让它在 Python 社区口碑两极。记住三条：

1. **默认用模块级变量**实现"全局唯一"，别急着写 `__new__`；
2. 真需要类单例时，**初始化放 `__new__`、并发加锁**（或直接用元类版）；
3. 单例是"资源管理"的手段，不是"懒得传参"的借口。

下一章，我们来看比单例更常见的创建套路——**简单工厂**：一个函数，按参数出对象。

---

*本章金句：单例解决的是"资源唯一性"，不是"懒得传参"——全局状态是能力，也是枷锁。*
