# 第 2 章 简单工厂（Simple Factory）

> **一句话总结**：一个函数，按参数返回不同类型的对象。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 创建型（补充，非 GoF） | ★☆☆☆☆ | ★★★★★ |

---

## 1. 引子：先讲个故事

去奶茶店买奶茶，你从来不需要走进后厨。你只对前台说一句："一杯珍珠奶茶，三分糖"，前台就会转身，后厨就会出对应的那杯。你**报名字，人家出东西**——至于珍珠是哪个牌子、茶底是什么配方，你一概不用管。

写代码也一样。假设你在做一个支付系统，支持微信、支付宝两种渠道，你会发现一个尴尬的事实：**"怎么创建一个支付渠道"这段逻辑，被复制粘贴到了各个角落**——下单模块要建渠道、退款模块要建渠道、对账模块还要建渠道。每个人都在后厨自己泡奶茶：

```python
# 引子：没有工厂的世界——每个业务模块都自己写一遍"怎么创建支付渠道"
class WechatPay:
    def pay(self, amount):
        return f"微信支付 {amount} 元"


class Alipay:
    def pay(self, amount):
        return f"支付宝支付 {amount} 元"


# 模块 A：下单模块里的创建逻辑
def create_channel_a(name: str):
    if name == "wechat":
        return WechatPay()
    elif name == "alipay":
        return Alipay()
    else:
        raise ValueError(f"不支持的支付渠道：{name}")


# 模块 B：退款模块又抄了一遍
def create_channel_b(name: str):
    if name == "wechat":
        return WechatPay()
    elif name == "alipay":
        return Alipay()
    else:
        raise ValueError(f"不支持的支付渠道：{name}")


print(create_channel_a("wechat").pay(100))
print(create_channel_b("alipay").pay(50))
```

运行输出：

```
微信支付 100 元
支付宝支付 50 元
```

问题出在哪？等产品经理说"下周要接入银联"，你就得冲进每个模块把那段 `if-elif` 挨个改一遍——漏改一处就是线上事故。**创建逻辑散落各处，就是"每个业务员都自己泡奶茶"的代码版。**解决办法很简单：把"泡奶茶"这件事集中到前台一个人手里——这就是**简单工厂**。

---

## 2. 模式登场

### 定义

> **简单工厂（Simple Factory）**：用一个集中的"工厂"（通常是一个函数或类），根据传入的参数，返回不同类型的对象。客户端只报"名字"，不关心"对象是怎么造出来的"。

先泼一盆冷水：**简单工厂不是 GoF 23 个模式之一**。但它是实际开发中**使用频率最高的创建对象套路**——正因为太常用，很多书都忍不住把它收进来当"编外模式"。它还是后面第 7 章工厂方法、第 14 章抽象工厂的入门台阶。

### 解决的问题

1. **创建逻辑重复**：每个调用方都要写一遍 `if-elif`，加新类型要改 N 处；
2. **客户端与具体类耦合**：业务代码里直接 `WechatPay()`，换实现就要改业务代码；
3. **创建细节无人管理**：构造对象可能要传配置、做缓存、校验参数，这些杂活散落各处没人统一。

### 结构

```
┌──────────────────────────────┐
│      SimpleFactory（工厂）     │
├──────────────────────────────┤
│ + create(kind)               │  ← 按 kind 决定返回哪个对象
└──────────────┬───────────────┘
               │ 按 kind 返回
     ┌─────────┼──────────┐
     ▼         ▼          ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ProductA │ │ProductB │ │ProductC │
└─────────┘ └─────────┘ └─────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **工厂（Factory）** | 集中管理创建逻辑：选类型、处理创建细节 |
| **产品接口（Product）** | 所有产品的共同约定（Python 里常省略，鸭子类型说了算） |
| **具体产品（ConcreteProduct）** | 真正被创建出来的类 |
| **客户端（Client）** | 只传参数、拿对象，不关心具体类名 |

---

## 3. Python 实现

### 3.1 经典版：一个函数 + if-elif（支付渠道工厂）

最朴素的写法：一个工厂函数，内部用 `if-elif` 分支选择类。注意三个渠道类**没有继承任何公共基类**——Python 信奉鸭子类型，"长得像"就够了：

```python
class WechatPay:
    def pay(self, amount: float) -> str:
        return f"【微信支付】{amount} 元"


class Alipay:
    def pay(self, amount: float) -> str:
        return f"【支付宝】{amount} 元"


class UnionPay:
    def pay(self, amount: float) -> str:
        return f"【银联支付】{amount} 元"


def create_channel(name: str):
    """简单工厂：报一个名字，返回对应的支付渠道"""
    if name == "wechat":
        return WechatPay()
    elif name == "alipay":
        return Alipay()
    elif name == "unionpay":
        return UnionPay()
    else:
        raise ValueError(f"未知支付渠道：{name}")


for name in ["wechat", "alipay", "unionpay"]:
    channel = create_channel(name)
    print(channel.pay(99.9))
```

运行输出：

```
【微信支付】99.9 元
【支付宝】99.9 元
【银联支付】99.9 元
```

对比引子里的代码：**创建逻辑从"每个模块一份"变成"全项目一份"**。以后加渠道，只有工厂一个地方要改（这仍是简单工厂的软肋，见第 8 节）。

### 3.2 类版工厂：除了选类型，还能顺手做点别的

工厂不一定要是函数，也可以是类。类的优势是**可以持有状态**——比如给解析器加个缓存，同一个格式不重复创建：

```python
import json


class JsonParser:
    def parse(self, text: str):
        return json.loads(text)


class PlainParser:
    def parse(self, text: str):
        return text.strip()


class ParserFactory:
    """类版工厂：选类型 + 顺手做缓存"""

    def __init__(self):
        self._cache = {}

    def get_parser(self, fmt: str):
        if fmt not in self._cache:
            if fmt == "json":
                self._cache[fmt] = JsonParser()
            elif fmt == "plain":
                self._cache[fmt] = PlainParser()
            else:
                raise ValueError(f"未知格式：{fmt}")
            print(f"首次创建 {fmt} 解析器")
        return self._cache[fmt]


factory = ParserFactory()
p1 = factory.get_parser("json")
p2 = factory.get_parser("json")
print("JSON 解析结果：", p1.parse('{"name": "小明", "age": 18}'))
print("同一个 json 解析器被复用：", p1 is p2)
```

运行输出：

```
首次创建 json 解析器
JSON 解析结果： {'name': '小明', 'age': 18}
同一个 json 解析器被复用： True
```

工厂不只是"选类"，它还能把"创建 + 缓存 + 校验"这些杂活集中起来——这就是它比到处 `new` 更值得用的原因。

### 3.3 动物工厂：创建完直接统一使用

工厂的终极价值：**客户端拿到对象后，根本不需要知道具体是什么类**。造出来是狗是猫，统一 `speak()` 就完事：

```python
class Dog:
    def speak(self) -> str:
        return "汪汪！"


class Cat:
    def speak(self) -> str:
        return "喵～"


class Duck:
    def speak(self) -> str:
        return "嘎嘎！"


def create_animal(kind: str):
    """动物工厂：报个种类，返回对应的动物"""
    if kind == "dog":
        return Dog()
    elif kind == "cat":
        return Cat()
    elif kind == "duck":
        return Duck()
    else:
        raise ValueError(f"没有这种动物：{kind}")


for kind in ["dog", "cat", "duck"]:
    print(f"{kind}：{create_animal(kind).speak()}")
```

运行输出：

```
dog：汪汪！
cat：喵～
duck：嘎嘎！
```

---

## 4. Python 特有玩法

### 4.1 字典注册表工厂：告别 if-elif 地狱

Python 里有个祖传妙招：**把 if-elif 换成字典**。"名字 → 类"的映射本身就是一张表，查表比分支清晰得多：

```python
class WechatPay:
    def pay(self, amount):
        return f"微信支付 {amount} 元"

class Alipay:
    def pay(self, amount):
        return f"支付宝 {amount} 元"

class UnionPay:
    def pay(self, amount):
        return f"银联支付 {amount} 元"


# 注册表：名字 → 类 的映射集中在这里
CHANNELS = {
    "wechat": WechatPay,
    "alipay": Alipay,
    "unionpay": UnionPay,
}


def create_channel(name: str):
    cls = CHANNELS.get(name)
    if cls is None:
        raise ValueError(f"未知支付渠道：{name}")
    return cls()


# 加新渠道 = 加一个类 + 注册表加一行，工厂函数体永远不用动
print(create_channel("wechat").pay(100))
print(create_channel("unionpay").pay(200))
```

运行输出：

```
微信支付 100 元
银联支付 200 元
```

这种"注册表式工厂"是 Python 社区最地道的写法，也是缓解"加类型要改工厂"（开闭原则）的主要手段——新类型只是**新增**一个条目，而不是**修改**工厂的判断逻辑。

### 4.2 classmethod 工厂：让类自己当工厂

"工厂"不一定是外部函数，**类方法（classmethod）本身就是工厂**。`datetime.fromtimestamp`、`dict.fromkeys` 都是这个套路——同一个类，换一种创建方式：

```python
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @classmethod
    def from_dict(cls, data: dict):
        """工厂：从字典创建"""
        return cls(data["name"], data["age"])

    def __repr__(self):
        return f"User({self.name}, {self.age})"


u1 = User("小明", 18)
u2 = User.from_dict({"name": "小红", "age": 20})
print("直接构造：", u1)
print("from_dict 工厂：", u2)
```

运行输出：

```
直接构造： User(小明, 18)
from_dict 工厂： User(小红, 20)
```

注意 `from_dict` 返回的是 `cls(...)`——子类调用它时会自动创建子类实例，这是 classmethod 工厂比普通函数工厂更"懂继承"的地方。

### 4.3 函数式工厂：工厂本身就是一个函数

在 Python 里，**工厂不需要是类，一个函数就够了**（Java 里你得专门写一个 `Factory` 类）。既然工厂是函数，它就能像普通函数一样被传来传去：

```python
class Car:
    def drive(self):
        return "汽车出发 🚗"


class Bike:
    def ride(self):
        return "自行车出发 🚲"


def make_car():
    return Car()

def make_bike():
    return Bike()


def deliver(vehicle_factory):
    return vehicle_factory()      # 把工厂函数当参数，需要时再调用


print(deliver(make_car).drive())
print(deliver(make_bike).ride())
```

运行输出：

```
汽车出发 🚗
自行车出发 🚲
```

---

## 5. 真实世界中的它

### `datetime.strptime`：按"格式字符串"返回 datetime

标准库里到处是简单工厂。`datetime.strptime` 就是典型的"按参数出对象"——你给不同的格式字符串，它返回按该格式解析出的 `datetime`：

```python
from datetime import datetime

d1 = datetime.strptime("2024-01-15 10:30:00", "%Y-%m-%d %H:%M:%S")
d2 = datetime.strptime("15/01/2024", "%d/%m/%Y")
print("第一种格式解析：", d1)
print("第二种格式解析：", d2)
```

运行输出：

```
第一种格式解析： 2024-01-15 10:30:00
第二种格式解析： 2024-01-15 00:00:00
```

### `json.loads`：按"内容"返回不同结构

更绝的是 `json.loads`——它连参数都不看，**直接看内容长什么样**：内容是 `{...}` 就返回 `dict`，是 `[...]` 就返回 `list`，是字符串就返回 `str`：

```python
import json

result_a = json.loads('{"name": "小明"}')   # 内容是对象 → dict
result_b = json.loads('[1, 2, 3]')          # 内容是数组 → list
result_c = json.loads('"hello"')            # 内容是字符串 → str

print("类型 1：", type(result_a).__name__, result_a)
print("类型 2：", type(result_b).__name__, result_b)
print("类型 3：", type(result_c).__name__, result_c)
```

运行输出：

```
类型 1： dict {'name': '小明'}
类型 2： list [1, 2, 3]
类型 3： str hello
```

### 内建 `open()`：路径 + 模式 → 文件对象

`open()` 也是工厂：同一个函数，传 `"r"` 返回文本模式的文件对象，传 `"rb"` 返回二进制模式的文件对象。**一个入口，多种产出**：

```python
import os
import tempfile

with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
    f.write("临时文件内容")
    path = f.name

with open(path, "r", encoding="utf-8") as f_text:
    print("文本模式返回：", type(f_text).__name__)
with open(path, "rb") as f_bin:
    print("二进制模式返回：", type(f_bin).__name__)
os.unlink(path)
```

运行输出：

```
文本模式返回： TextIOWrapper
二进制模式返回： BufferedReader
```

再往大了说：`str()`、`int()`、`list()`、`dict()` 这些内建"构造器"，本质上也都是工厂。**简单工厂的思想早就在你的日常里了。**

---

## 6. 优缺点与适用场景

### 优点

- **创建逻辑集中**：全项目只有一个地方知道"怎么造对象"，改一处生效处处；
- **客户端解耦**：业务代码不再依赖具体类名，只认工厂和产品接口（依赖倒置原则的雏形）；
- **统一管理细节**：缓存、参数校验、日志这些"创建时的杂活"可以集中处理（见 3.2）；
- **实现极简**：一个函数就能落地，零框架零依赖。

### 缺点

- **违反开闭原则**：加新类型要**修改**工厂函数（可以靠注册表缓解）；
- **if-elif 会膨胀**：产品类型一多，工厂内部就变成"if-elif 地狱"；
- **职责集中**：所有创建逻辑挤在一个地方，类型很多时工厂类会变得臃肿。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 产品类型不多（十几个以内）且相对稳定 | 类型很多、还频繁新增（改用工厂方法，第 7 章） |
| 创建逻辑需要统一管理（校验/缓存/日志） | 创建过程复杂、需要分步组装（改用建造者，第 11 章） |
| 想对客户端隐藏具体类名 | 只有一个类、直接 `new` 就完事的场景 |
| 作为工厂方法/抽象工厂的入门替代 | 需要"不同工厂生产不同产品族"（用抽象工厂，第 14 章） |

---

## 7. 与其他模式的关系

- **简单工厂 → 工厂方法 → 抽象工厂**：这是"创建型三连"的升级路线。简单工厂把创建逻辑集中在一个函数里（加类型要改它）；工厂方法把创建逻辑**下放给子类**（加类型 = 加子类，父类不用改）；抽象工厂再升级为"一套产品成套生产"。简单工厂是后两者的地基。
- **简单工厂 vs 策略模式**：一字之差，天壤之别。简单工厂管**创建**——"返回什么对象"；策略模式管**行为**——"对象怎么做这件事"。一个发生在 `new` 之前，一个发生在 `new` 之后。
- **简单工厂 + 单例**：工厂内部经常配合单例做缓存（3.2 里的 `_cache` 就是"每类一个实例"的迷你单例注册表）。
- **简单工厂 + 外观**：工厂是"创建的门面"，外观是"整个子系统的门面"（第 6 章），理念相通。

---

## 8. 常见误区

### 误区 1：以为加新类型"不用改任何旧代码"

简单工厂最大的坑：**每加一种产品，都要回头改工厂**。这就是开闭原则（对扩展开放、对修改关闭）在简单工厂身上的破绽：

```python
class WechatPay:
    def pay(self, amount):
        return f"微信 {amount} 元"


class Alipay:
    def pay(self, amount):
        return f"支付宝 {amount} 元"


def create_channel(name):
    if name == "wechat":
        return WechatPay()
    elif name == "alipay":
        return Alipay()
    else:
        raise ValueError(f"未知渠道：{name}")


print(create_channel("wechat").pay(100))
print(create_channel("alipay").pay(50))
print("（半年后要加银联？还是得回来改 create_channel 本体）")
```

运行输出：

```
微信 100 元
支付宝 50 元
（半年后要加银联？还是得回来改 create_channel 本体）
```

**缓解办法**：用 4.1 的"字典注册表"——新类型 = 新类 + 注册表加一行，工厂函数体不用动；再进一步，就是用工厂方法模式把"创建逻辑"交给子类（第 7 章）。

### 误区 2：把工厂当万能钥匙，什么都往里塞

有人觉得"工厂很高级"，于是把**所有**对象的创建都丢进一个工厂，连毫无关联的东西也塞进去，最后工厂里躺着几百行 if-elif，成了一个"上帝类"。工厂适合的是"**同一类东西、不同变体**"的创建——毫不相干的类（比如 `Logger` 和 `Order`）没有共同接口，硬塞进去只会变成垃圾场。判断标准：**它们能被当成同一个接口用吗？不能就别进同一个工厂。**

### 误区 3：工厂和直接 new 混用

同一个对象，一会儿走工厂、一会儿直接 `new`——创建逻辑又分裂成两处，工厂升级了，直 new 的地方还在用老配置：

```python
class Logger:
    def __init__(self, level: str = "INFO"):
        self.level = level

    def log(self, msg: str):
        print(f"[{self.level}] {msg}")


def create_logger(level: str = "INFO"):
    """工厂：以后想统一给 logger 加时间戳，改这里就行"""
    return Logger(level)


logger_a = create_logger("DEBUG")   # 模块 A：老老实实走工厂
logger_b = Logger("INFO")           # 模块 B：图省事直接 new

logger_a.log("A 的日志")
logger_b.log("B 的日志")
print("两个 logger 配置是否一致：", logger_a.level == logger_b.level)
```

运行输出：

```
[DEBUG] A 的日志
[INFO] B 的日志
两个 logger 配置是否一致： False
```

**规则：既然决定用工厂，就全员走工厂**。混用等于没有工厂。

---

## 9. 练习题

### 练习 1：把 if-elif 工厂改写成"字典注册表"版

下面是一个用 if-elif 写的形状工厂（`circle`/`square` 两个分支），请把它改造成"字典注册表"版（答案见代码块）：

```python
class Circle:
    def draw(self):
        return "画圆 ⭕"


class Square:
    def draw(self):
        return "画方 ⬜"


SHAPES = {
    "circle": Circle,
    "square": Square,
}


def create_shape(name):
    cls = SHAPES.get(name)
    if cls is None:
        raise ValueError(f"未知形状：{name}")
    return cls()


print(create_shape("circle").draw())
print(create_shape("square").draw())
```

运行输出：

```
画圆 ⭕
画方 ⬜
```

### 练习 2：给"动物工厂"加一种鸡

给下面的动物工厂加上 `chicken` 类型，让"咯咯咯"也能被创建出来（提示：加一个 `Chicken` 类 + 一个分支）：

```python
class Dog:
    def speak(self):
        return "汪汪！"


class Cat:
    def speak(self):
        return "喵～"


class Chicken:
    def speak(self):
        return "咯咯咯！"


def create_animal(kind):
    if kind == "dog":
        return Dog()
    elif kind == "cat":
        return Cat()
    elif kind == "chicken":
        return Chicken()
    else:
        raise ValueError(f"没有这种动物：{kind}")


for kind in ["dog", "cat", "chicken"]:
    print(f"{kind}：{create_animal(kind).speak()}")
```

运行输出：

```
dog：汪汪！
cat：喵～
chicken：咯咯咯！
```

### 练习 3：给 Time 类写一个 classmethod 工厂 `from_seconds`

让 `Time.from_seconds(3725)` 返回 `01:02:05`：

```python
class Time:
    def __init__(self, hour: int, minute: int, second: int):
        self.hour, self.minute, self.second = hour, minute, second

    @classmethod
    def from_seconds(cls, total: int):
        """工厂：把总秒数换算成 时:分:秒 再构造"""
        hour, rem = divmod(total, 3600)
        minute, second = divmod(rem, 60)
        return cls(hour, minute, second)

    def __repr__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"


t = Time.from_seconds(3725)
print(t)
```

运行输出：

```
01:02:05
```

---

## 10. 小结与口诀

> **口诀：创建都走工厂门，报个名字拿对象；类型一多上注册表，别让分支遍地长。**

简单工厂不是 GoF 正统，却是 Python 日常开发里出现频率最高的创建套路。记住三条：**创建逻辑集中一处**，别让每个模块自己泡奶茶；**用字典注册表代替 if-elif**，新类型只增不改；产品类型多了、变快了，就升级到**工厂方法**（第 7 章）。

下一章，我们来看行为型里使用率第一的**策略模式**——算法可插拔，运行时换。

---

*本章金句：简单工厂是"报名字拿对象"——它管的是"造出什么"，至于造出来之后怎么用，那是策略模式的事。*
