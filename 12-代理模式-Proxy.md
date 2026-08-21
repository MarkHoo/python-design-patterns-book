# 第 12 章 代理模式（Proxy）

> **一句话总结**：经纪人替你办事：该拦的拦，该等的等，该转的转。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 结构型 | ★★★☆☆ | ★★★★☆ |

---

## 1. 引子：先讲个故事

想见一位当红明星？别想了。粉丝不能直接冲进片场找明星本人，得先联系**经纪人**。经纪人说"这周行程满了"（拦），说"下周三可以，先付定金"（等），说"商演的事我转给商务团队"（转）。明星该唱歌唱歌、该拍戏拍戏，但外界只能通过经纪人接触他——经纪人控制着"能不能见、什么时候见、怎么见"。

程序世界里，有些对象跟明星一样"贵"：加载一张 50MB 的高清大图要 3 秒，连一次数据库要几百毫秒，创建一个重量级服务要初始化一堆东西。如果客户端直接操作它们，就会这样：

```python
# 引子：打开相册就把所有高清大图全加载了——慢死了
class HeavyImage:
    """一张高清大图：加载很贵"""

    def __init__(self, filename):
        self.filename = filename
        print(f"正在从磁盘加载 {filename}（50MB，花了 3 秒）...")

    def display(self):
        print(f"显示 {self.filename}")

# 相册应用：一打开就把 3 张图全部加载
album = [HeavyImage(f"photo{i}.jpg") for i in range(1, 4)]
print("——用户其实只想看第 1 张——")
album[0].display()
```

运行输出：

```
正在从磁盘加载 photo1.jpg（50MB，花了 3 秒）...
正在从磁盘加载 photo2.jpg（50MB，花了 3 秒）...
正在从磁盘加载 photo3.jpg（50MB，花了 3 秒）...
——用户其实只想看第 1 张——
显示 photo1.jpg
```

用户只想看第 1 张，3 张图却全部加载完了——白白浪费 6 秒。**代理模式**就是给"明星"配个"经纪人"：客户端只跟代理打交道，代理决定什么时候才去惊动真实对象。

---

## 2. 模式登场

### 定义

> **代理模式**：为另一个对象提供一个替身或占位符，以控制对这个对象的访问。

### 解决的问题

1. **懒加载**：对象太贵，用到时才创建（虚拟代理）；
2. **权限控制**：不是谁都能访问，先检查资格（保护代理）；
3. **远程调用**：对象在别的机器上，代理负责网络传输（远程代理）；
4. **缓存**：重复的昂贵调用，代理直接给上次结果（缓存代理）。

### 结构

```
┌────────────────────────────┐
│    Subject（抽象主题/接口）    │
├────────────────────────────┤
│ + request()                │  ← 代理和真实对象实现同一个接口
└────────────────────────────┘
        ▲              ▲
        │ 实现          │ 实现
┌───────┴──────┐  ┌─────┴─────────────────┐
│  RealSubject  │  │        Proxy          │
│  （真实对象）  │  │      （代理/经纪人）     │
├──────────────┤  ├───────────────────────┤
│ + request()  │  │ - real: RealSubject   │  ← 持有真实对象引用
└──────────────┘  │ + request()           │  ← 控制访问：拦 / 等 / 转
                  └───────────────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **抽象主题 Subject** | 真实对象和代理共同实现的接口（经纪人"能做的事"和明星一样） |
| **真实对象 RealSubject** | 真正干活的对象（明星本人） |
| **代理 Proxy** | 持有真实对象的引用，控制对它的访问 |
| **客户端 Client** | 只跟代理打交道，完全不知道真实对象的存在 |

关键点：**代理与真实对象实现同一个接口**——客户端眼里代理就是真身，所以代理**不改变接口**（这点和适配器正好相反，见第 7 节）。

---

## 3. Python 实现

### 3.1 虚拟代理：该等的等（懒加载）

图片先不加载，用户真正要看哪张才加载哪张：

```python
class HeavyImage:
    """真实对象：加载很贵"""

    def __init__(self, filename):
        self.filename = filename
        print(f"正在从磁盘加载 {filename}（50MB，花了 3 秒）...")

    def display(self):
        print(f"显示 {self.filename}")

class ImageProxy:
    """虚拟代理：先不加载，真正要显示时才创建真实对象"""

    def __init__(self, filename):
        self.filename = filename
        self._real = None          # 真实对象先不创建

    def display(self):
        if self._real is None:     # 第一次调用才加载（懒加载）
            self._real = HeavyImage(self.filename)
        self._real.display()

album = [ImageProxy(f"photo{i}.jpg") for i in range(1, 4)]
print("相册已打开，但一张图都没加载")
album[1].display()   # 只看第 2 张，只加载第 2 张
```

运行输出：

```
相册已打开，但一张图都没加载
正在从磁盘加载 photo2.jpg（50MB，花了 3 秒）...
显示 photo2.jpg
```

对比引子的坏味道：同样是 3 张图的相册，现在打开相册零开销，看到哪张才加载哪张。

### 3.2 保护代理：该拦的拦（权限检查）

代理在转发前先检查"你是谁、有没有资格"：

```python
class BankAccount:
    """真实对象：银行账户"""

    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance

    def withdraw(self, amount):
        if amount > self._balance:
            print(f"余额不足：只有 {self._balance} 元")
            return
        self._balance -= amount
        print(f"取款 {amount} 元成功，剩余 {self._balance} 元")

class AccountProxy:
    """保护代理：先检查权限，再放行"""

    def __init__(self, account, user):
        self._account = account
        self._user = user

    def withdraw(self, amount):
        if self._user != self._account.owner:
            print(f"拒绝：{self._user} 不是账户主人，无权取款")
            return
        self._account.withdraw(amount)

account = BankAccount("小明", 1000)
proxy = AccountProxy(account, "小红")
proxy.withdraw(500)          # 小红想取钱 → 被拦
proxy2 = AccountProxy(account, "小明")
proxy2.withdraw(500)         # 本人取钱 → 放行
```

运行输出：

```
拒绝：小红 不是账户主人，无权取款
取款 500 元成功，剩余 500 元
```

权限检查全在代理里，`BankAccount` 本身干净纯粹，不知道外面还有个"门卫"。

### 3.3 缓存代理：该存的存（结果复用）

重复的昂贵计算，代理记下第一次的结果，之后直接秒回：

```python
import time

class SlowCalculator:
    """真实对象：计算很慢"""

    def calculate(self, n):
        time.sleep(0.2)        # 模拟 0.2 秒的昂贵计算
        return n * n

class CacheProxy:
    """缓存代理：同样的请求直接返回上次结果"""

    def __init__(self, target):
        self._target = target
        self._cache = {}

    def calculate(self, n):
        if n not in self._cache:
            self._cache[n] = self._target.calculate(n)
            print(f"（首次计算 {n}²，慢）")
        else:
            print(f"（命中缓存 {n}²，秒回）")
        return self._cache[n]

proxy = CacheProxy(SlowCalculator())
print(proxy.calculate(7))
print(proxy.calculate(7))
print(proxy.calculate(8))
print(proxy.calculate(8))
```

运行输出：

```
（首次计算 7²，慢）
49
（命中缓存 7²，秒回）
49
（首次计算 8²，慢）
64
（命中缓存 8²，秒回）
64
```

Python 里这个思想已经内建成了 `functools.lru_cache` 装饰器（导读 0.5 节见过），但理解代理的"转发 + 拦截"本质依然重要——因为 lru_cache 只能管函数，管不了对象。

---

## 4. Python 特有玩法

### 4.1 `__getattr__` 万能转发代理

代理的骨架就是"转发"：把客户端的所有调用转给真实对象。Python 的 `__getattr__` 钩子让这个骨架二十行就能写完，真实对象想换就换：

```python
class GenericProxy:
    """通用代理：只负责转发，具体对象随便换"""

    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        # 代理自己没有的属性，全部转发给目标对象
        return getattr(self._target, name)

class Logger:
    def __init__(self, name):
        self.name = name

    def info(self, msg):
        print(f"[INFO] {self.name}: {msg}")

proxy = GenericProxy(Logger("订单服务"))
proxy.info("收到新订单")     # 代理没有 info → 转发给 Logger
print("代理能拿到属性：", proxy.name)
```

运行输出：

```
[INFO] 订单服务: 收到新订单
代理能拿到属性： 订单服务
```

注意转发的是**绑定到真实对象的方法**，所以调用时 `self` 是真实对象，不会串到代理身上。

### 4.2 `weakref.proxy`：不增加生命周期的代理

标准库 `weakref.proxy` 提供一种特殊的代理：它不阻止真实对象被垃圾回收。适合"缓存引用但不想长期霸占对象"的场景：

```python
import weakref

class BigData:
    def __init__(self, size):
        self.size = size
        print(f"加载了 {size} 条数据")

    def summary(self):
        return f"共 {self.size} 条数据"

data = BigData(10000)
ref = weakref.proxy(data)      # 弱引用代理：不阻止对象被回收
print("通过代理访问：", ref.summary())

del data                        # 真实对象被销毁
try:
    print(ref.summary())        # 代理指向的对象没了 → 报错
except ReferenceError:
    print("代理报错：原对象已被回收（ReferenceError）")
```

运行输出：

```
加载了 10000 条数据
通过代理访问： 共 10000 条数据
代理报错：原对象已被回收（ReferenceError）
```

普通代理会"拖住"真实对象不让它死，`weakref.proxy` 恰恰相反：对象该死就死，代理跟着失效——这就是"弱引用"的含义。

### 4.3 类装饰器生成代理

想给一批类统一套上"日志代理"？用类装饰器批量生产：

```python
def logging_proxy(cls):
    """类装饰器：把类的所有方法包上一层日志，返回一个代理类"""
    class Proxy:
        def __init__(self, *args, **kwargs):
            self._real = cls(*args, **kwargs)

        def __getattr__(self, name):
            attr = getattr(self._real, name)
            if callable(attr):
                def wrapper(*a, **kw):
                    print(f"[日志] 调用 {name}({a}{kw})")
                    return attr(*a, **kw)
                return wrapper
            return attr
    return Proxy

@logging_proxy
class Calculator:
    def add(self, x, y):
        return x + y

calc = Calculator()
print("add 结果：", calc.add(3, 4))
```

运行输出：

```
[日志] 调用 add((3, 4){})
add 结果： 7
```

原类 `Calculator` 一行没改，只是"注册"了一下，就多了一整套日志能力——这正符合**开闭原则**。

---

## 5. 真实世界中的它

### 标准库：`weakref.proxy` 与弱引用缓存

4.2 演示的 `weakref.proxy` 就是标准库自带的最小代理：弱引用、不阻止回收。真实项目里更常用的是它的"亲戚" `weakref.WeakValueDictionary`——用弱引用做缓存表，对象没人用时自动从缓存消失，不会造成内存泄漏（原理同 4.2，只是从"单个对象"变成"一张表"）。

### 框架：Django 的 `LazyObject` 与懒加载 settings

Django 的 `django.utils.functional.LazyObject` 是一个虚拟代理基类：对象创建时**不真正初始化**，第一次访问属性时才把"幕后真实对象"造出来。Django 的 `settings` 就是它的经典应用——`from django.conf import settings` 时什么都没加载，第一次 `settings.DEBUG` 才读取配置文件。整个 Web 框架的"启动飞快"就有它一份功劳。

### 框架：SQLAlchemy 的懒加载

ORM 框架 SQLAlchemy 里，`session.query(User).all()` 返回的 User 对象，关联属性（比如 `user.orders`）默认是**懒加载**的：访问 `orders` 那一刻才去数据库查。这里用的就是虚拟代理——查询代理替你挡着，等你真要数据了才发 SQL。

---

## 6. 优缺点与适用场景

### 优点

- **性能优化**：懒加载、缓存，把昂贵操作推迟或复用；
- **安全控制**：权限、日志、监控统一收口在代理里，真实对象保持纯粹（**单一职责**）；
- **解耦**：客户端不知道真实对象在哪台机器、什么时候创建；
- **开闭原则**：加控制逻辑不用改真实对象。

### 缺点

- **多一层间接**：调用变慢一点点，出错时多一层栈要查；
- **可能引入复杂性**：代理和真实对象容易"长得太像"，读者分不清谁是谁；
- **生命周期陷阱**：弱引用代理可能"突然失效"，懒加载代理有线程安全问题（见误区 3）。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 大对象懒加载（图片、连接、模型） | 对象创建本来就便宜 |
| 需要统一的权限/日志/监控控制 | 控制逻辑只有一两处，直接写在对象里更简单 |
| 远程调用（RPC、网络服务） | 本地对象间"隔着代理"纯属多余 |
| 频繁重复的昂贵计算（缓存） | 可以直接用 `functools.lru_cache` 的纯函数 |

---

## 7. 与其他模式的关系

- **代理 vs 适配器**：代理**不改接口**（和真实对象长得一模一样），适配器**改接口**。代理是"替身"，适配器是"翻译"；
- **代理 vs 装饰器**：代理**控制访问**（拦不拦、什么时候放行），装饰器**增强功能**（加日志、加缓存但从不拒绝调用）。装饰器像给手机贴膜，代理像给明星请保镖；
- **代理 vs 外观**：代理控制**单个对象**的访问，外观简化**一组对象**的接口；
- **代理 + 工厂**：工厂负责创建"真实对象还是代理"，客户端无感知地拿到代理。

---

## 8. 常见误区

### 误区 1：把代理和装饰器混为一谈

装饰器**增强**功能（调用必达，只是顺带加点料）；代理**控制**访问（可能直接拒绝，根本不到真实对象）。看例子：

```python
# 装饰器：给对象"加功能"（不拦访问）
def shoutify(cls):
    """装饰器：把 hello 的结果喊出来"""
    original = cls.hello

    def hello(self):
        return original(self).upper() + "！"

    cls.hello = hello
    return cls

@shoutify
class Greeter:
    def hello(self):
        return "你好"

print(Greeter().hello())     # 功能被增强了：你好 → 你好！

# 代理：控制"能不能访问"（不改变功能）
class Secret:
    def hello(self):
        return "秘密内容"

class GuardProxy:
    """保护代理：权限不够就拦截"""

    def __init__(self, target, allowed):
        self._target = target
        self._allowed = allowed

    def hello(self):
        if not self._allowed:
            return "无权访问"
        return self._target.hello()

print(GuardProxy(Secret(), allowed=False).hello())
print(GuardProxy(Secret(), allowed=True).hello())
```

运行输出：

```
你好！
无权访问
秘密内容
```

一句话区分：**装饰器保证"事一定办成"（最多锦上添花），代理可能"事直接不办"**。

### 误区 2：`__getattr__` 转发时的无限递归

`__getattr__` 里一旦访问**自身不存在的属性**，就会再次触发 `__getattr__`，形成死循环：

```python
class RecursiveProxy:
    """反面教材：转发时访问了自己不存在的属性 → 无限递归"""

    def __getattr__(self, name):
        return self.missing_attribute   # self.missing_attribute 又不存在 → 又触发 __getattr__

try:
    RecursiveProxy().foo
except RecursionError:
    print("触发 RecursionError：__getattr__ 无限递归")
```

运行输出：

```
触发 RecursionError：__getattr__ 无限递归
```

正确姿势：在 `__getattr__` 里用 `object.__getattribute__(self, "_target")` 强制走实例字典，不再触发 `__getattr__`——4.1 的 `GenericProxy` 就是这样写的：`_target` 存在实例字典里，访问它不会再次触发 `__getattr__`，转发目标也不存在时记得 `raise AttributeError(name)`。

### 误区 3：懒加载代理的线程安全问题

"第一次访问才创建"的懒加载，在**多线程**下可能被多个线程同时创建出多个真实对象。加锁 + 双重检查是标准解法：

```python
import threading
import time

class Heavy:
    def __init__(self):
        time.sleep(0.05)
        self.ready = True

class LazyProxy:
    """线程安全懒加载代理：加锁 + 双重检查"""

    def __init__(self, factory):
        self._factory = factory
        self._real = None
        self._lock = threading.Lock()

    def get(self):
        if self._real is None:            # 第一次检查：不加锁，快路径
            with self._lock:
                if self._real is None:    # 第二次检查：防止重复创建
                    self._real = self._factory()
        return self._real

proxy = LazyProxy(lambda: Heavy())
results = []
lock = threading.Lock()

def worker():
    obj = proxy.get()
    with lock:
        results.append(obj)

threads = [threading.Thread(target=worker) for _ in range(8)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("8 个线程拿到的都是同一个实例：", len({id(r) for r in results}) == 1)
```

运行输出：

```
8 个线程拿到的都是同一个实例： True
```

---

## 9. 练习题

### 练习 1：给文件服务写一个保护代理

员工只能读自己部门的文件，且没有删除权限。用保护代理实现：

```python
# 答案：保护代理
class FileService:
    def read(self, filename):
        return f"{filename} 的内容"

    def delete(self, filename):
        return f"{filename} 已删除"

class SecureFileProxy:
    """保护代理：部门匹配才能读，一律不能删"""

    def __init__(self, service, user, department):
        self._service = service
        self._user = user
        self._department = department

    def read(self, filename):
        if self._department not in filename:
            return f"拒绝：{self._user} 无权读取 {filename}"
        return self._service.read(filename)

    def delete(self, filename):
        return f"拒绝：普通员工没有删除权限"

svc = FileService()
proxy = SecureFileProxy(svc, "小王", "研发部")
print(proxy.read("研发部-需求文档.md"))
print(proxy.read("财务部-工资表.xlsx"))
print(proxy.delete("研发部-需求文档.md"))
```

运行输出：

```
研发部-需求文档.md 的内容
拒绝：小王 无权读取 财务部-工资表.xlsx
拒绝：普通员工没有删除权限
```

### 练习 2：给"报告生成"写一个虚拟代理

生成报告很慢（要 5 秒），希望代理创建时不生成、第一次 `show()` 才生成：

```python
# 答案：虚拟代理（懒加载）
class Report:
    def __init__(self, title):
        print(f"正在生成报告《{title}》，需要 5 秒……")
        self.title = title

    def show(self):
        return f"《{self.title}》报告内容"

class ReportProxy:
    def __init__(self, title):
        self.title = title
        self._real = None

    def show(self):
        if self._real is None:
            self._real = Report(self.title)
        return self._real.show()

proxy = ReportProxy("年度总结")
print("代理已创建，报告还没生成")
print(proxy.show())
print(proxy.show())   # 第二次不再生成
```

运行输出：

```
代理已创建，报告还没生成
正在生成报告《年度总结》，需要 5 秒……
《年度总结》报告内容
《年度总结》报告内容
```

### 练习 3：写一个"日志代理"

用 `__getattr__` 写一个通用代理：转发所有方法，每次调用前打印日志：

```python
# 答案：__getattr__ 转发 + 调用前打日志
class LogProxy:
    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        attr = getattr(self._target, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                print(f"[日志] 调用 {name}，参数 {args}")
                return attr(*args, **kwargs)
            return wrapper
        return attr

class OrderService:
    def create(self, order_id):
        return f"订单 {order_id} 已创建"

    def cancel(self, order_id):
        return f"订单 {order_id} 已取消"

proxy = LogProxy(OrderService())
print(proxy.create(1001))
print(proxy.cancel(1001))
```

运行输出：

```
[日志] 调用 create，参数 (1001,)
订单 1001 已创建
[日志] 调用 cancel，参数 (1001,)
订单 1001 已取消
```

---

## 10. 小结与口诀

> **口诀：经纪人代办三件事——该等的等（懒加载），该拦的拦（权限），该转的转（转发）；接口不变，只做中间人。**

代理模式是"给对象配经纪人"：客户端只认代理，代理决定何时、能否、怎样访问真实对象。记住三条：

1. 代理**不改变接口**——这是它与适配器最根本的区别；
2. 四类代理各司其职：虚拟（懒加载）、保护（权限）、远程（RPC）、缓存（复用）；
3. 写 `__getattr__` 转发时警惕递归，多线程懒加载记得加锁。

下一章，我们来看行为型模式里的"层层审批"——**责任链模式**：层层审批，传到为止；谁接得住谁处理。

---

*本章金句：代理模式是"对象的经纪人"——该等的等，该拦的拦，该转的转，接口却原封不动。*
