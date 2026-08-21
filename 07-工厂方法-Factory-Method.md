# 第 7 章 工厂方法（Factory Method）

> **一句话总结**：把"创建谁"的决定权交给子类。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 创建型 | ★★☆☆☆ | ★★★★☆ |

---

## 1. 引子：先讲个故事

你加盟了一家连锁奶茶店。总部给了你一本厚厚的《开店手册》：招牌怎么做、杯子用哪款、封口机怎么调，全有统一规定。但总部很聪明——手册里只规定"**每个加盟店必须做出合格的招牌**"，至于你的招牌是灯箱还是霓虹灯、挂在左边还是右边，**由你自己决定**。加盟店千千万，总部不可能替每家店定制招牌，它只负责定规矩，把"招牌怎么做"这件事的**决定权下放**。

程序里也有类似的烦恼。假设你的项目要支持多种日志器：控制台日志、文件日志……你写了一个"工厂函数"来按名字创建：

```python
# 引子：简单工厂的"增长烦恼"——每加一种类型，就要改一次 create_logger
import os
import tempfile


class ConsoleLogger:
    def log(self, msg):
        print(f"[控制台] {msg}")


class FileLogger:
    def __init__(self, path):
        self._path = path

    def log(self, msg):
        with open(self._path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")


def create_logger(kind, **kwargs):
    """简单工厂：所有分支挤在一个函数里"""
    if kind == "console":
        return ConsoleLogger()
    elif kind == "file":
        return FileLogger(kwargs["path"])
    # 以后加 email 日志？加 database 日志？都得来这里改！——违反开闭原则
    raise ValueError(f"未知的日志类型：{kind}")


with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
    tmp_path = f.name

try:
    create_logger("console").log("启动系统")
    create_logger("file", path=tmp_path).log("写入文件日志")
    print("文件内容：", open(tmp_path, encoding="utf-8").read().strip())
finally:
    os.unlink(tmp_path)
```

运行输出：

```
[控制台] 启动系统
文件内容： 写入文件日志
```

这个"简单工厂"（第 2 章讲过）用起来很方便，但它有个致命伤：**每新增一种日志器，就要打开 `create_logger` 函数，在 if-elif 链上再添一个分支**。改的次数多了，这个函数会越来越臃肿，而且每次修改都可能碰坏旧分支——**对修改开放，对扩展关闭**，和开闭原则正好拧着来。

**工厂方法模式**就是来治这个病的：总部（抽象工厂）只规定"你要能造出日志器"，至于造哪种、怎么造，**交给子类（加盟店）自己决定**。

---

## 2. 模式登场

### 定义

> **工厂方法模式**：定义一个创建对象的接口（工厂方法），让子类决定实例化哪一个具体类。工厂方法把"实例化"延迟到子类。

### 解决的问题

1. **消除 if-elif 集中分支**：创建逻辑不再堆在一个函数里，而是分散到各个子类；
2. **符合开闭原则**：新增产品类型 = 新增一对子类，旧代码一行不改；
3. **面向抽象编程**：客户端只依赖抽象的 Creator 和 Product，替换实现无感。

### 结构

```
        ┌─────────────────────────────┐
        │      Creator（抽象工厂）        │
        ├─────────────────────────────┤
        │ + factory_method(): Product │  ← 抽象：子类实现
        │ + operation()               │
        └──────────────┬──────────────┘
                       ▲
          ┌────────────┴────────────┐
          ▼                         ▼
┌───────────────────┐   ┌───────────────────┐
│ ConcreteCreatorA  │   │ ConcreteCreatorB  │
├───────────────────┤   ├───────────────────┤
│ + factory_method()│   │ + factory_method()│
└─────────┬─────────┘   └─────────┬─────────┘
          │ 返回                   │ 返回
          ▼                       ▼
┌───────────────────┐   ┌───────────────────┐
│     ProductA      │   │     ProductB      │
└───────────────────┘   └───────────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **Product（产品）** | 抽象产品，定义产品的公共接口 |
| **ConcreteProduct（具体产品）** | 具体的产品类 |
| **Creator（抽象工厂）** | 声明工厂方法，返回 Product 类型 |
| **ConcreteCreator（具体工厂）** | 实现工厂方法，返回具体的 ConcreteProduct |

> 核心一句话：**"造什么"由子类决定，"怎么用"由客户端决定。**

---

## 3. Python 实现

### 3.1 经典版：日志器工厂

把引子里的"if-elif 函数"拆成"抽象工厂 + 子类工厂"，每个子类负责造一种产品：

```python
import abc
import os
import tempfile


class Logger(abc.ABC):
    """产品：日志器"""

    @abc.abstractmethod
    def log(self, message: str) -> None:
        pass


class ConsoleLogger(Logger):
    def log(self, message: str) -> None:
        print(f"[控制台] {message}")


class FileLogger(Logger):
    def __init__(self, path: str):
        self._path = path

    def log(self, message: str) -> None:
        with open(self._path, "a", encoding="utf-8") as f:
            f.write(message + "\n")


class LoggerFactory(abc.ABC):
    """抽象工厂：只规定"你要能造出 Logger"，不规定怎么造"""

    @abc.abstractmethod
    def create_logger(self) -> Logger:
        """工厂方法：创建逻辑下沉到子类"""
        pass


class ConsoleLoggerFactory(LoggerFactory):
    def create_logger(self) -> Logger:
        return ConsoleLogger()


class FileLoggerFactory(LoggerFactory):
    def __init__(self, path: str):
        self._path = path

    def create_logger(self) -> Logger:
        return FileLogger(self._path)


# 客户端面向抽象编程：只认 LoggerFactory，不认具体工厂
def use_factory(factory: LoggerFactory) -> None:
    logger = factory.create_logger()   # 工厂方法在此被调用
    logger.log("这是一条日志")


use_factory(ConsoleLoggerFactory())
with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
    tmp_path = f.name
try:
    use_factory(FileLoggerFactory(tmp_path))
    print("文件日志内容：", open(tmp_path, encoding="utf-8").read().strip())
finally:
    os.unlink(tmp_path)
```

运行输出：

```
[控制台] 这是一条日志
文件日志内容： 这是一条日志
```

对比引子：想加一种 `EmailLogger`？加一个 `EmailLogger` 类和 `EmailLoggerFactory` 类，`use_factory` 一行不用动。**创建逻辑从"集中修改"变成了"分散扩展"。**

> **关键点**：客户端拿到的永远声明为抽象类型 `Logger`，具体是谁不重要——这正是**依赖倒置原则**：高层模块依赖抽象，不依赖具体。

### 3.2 变体：图片解码器

真实项目里，工厂方法的"产品"往往是一族有公共接口的对象。图片解码器就是典型：PNG、JPEG、WebP 各有各的解析方式，但都提供同一个 `decode` 接口：

```python
import abc


class ImageDecoder(abc.ABC):
    """产品：图片解码器"""

    @abc.abstractmethod
    def decode(self, data: bytes) -> str:
        pass


class PngDecoder(ImageDecoder):
    def decode(self, data: bytes) -> str:
        return f"PNG 图片，{len(data)} 字节，支持透明通道"


class JpgDecoder(ImageDecoder):
    def decode(self, data: bytes) -> str:
        return f"JPEG 图片，{len(data)} 字节，适合照片"


class WebpDecoder(ImageDecoder):
    def decode(self, data: bytes) -> str:
        return f"WebP 图片，{len(data)} 字节，体积更小"


class ImageDecoderFactory(abc.ABC):
    """抽象工厂：负责产出解码器"""

    @abc.abstractmethod
    def create_decoder(self) -> ImageDecoder:
        pass


class PngDecoderFactory(ImageDecoderFactory):
    def create_decoder(self) -> ImageDecoder:
        return PngDecoder()


class JpgDecoderFactory(ImageDecoderFactory):
    def create_decoder(self) -> ImageDecoder:
        return JpgDecoder()


class WebpDecoderFactory(ImageDecoderFactory):
    def create_decoder(self) -> ImageDecoder:
        return WebpDecoder()


# 客户端只认抽象：新增格式 = 新增一对类，旧代码不动
def decode_file(data: bytes, factory: ImageDecoderFactory) -> str:
    decoder = factory.create_decoder()   # 工厂方法
    return decoder.decode(data)


print(decode_file(b"\x89PNG\r\n\x1a\n" + b"0" * 100, PngDecoderFactory()))
print(decode_file(b"\xff\xd8\xff\xe0" + b"0" * 100, JpgDecoderFactory()))
print(decode_file(b"RIFF" + b"0" * 64, WebpDecoderFactory()))
```

运行输出：

```
PNG 图片，108 字节，支持透明通道
JPEG 图片，104 字节，适合照片
WebP 图片，68 字节，体积更小
```

下次要支持 GIF，写一个 `GifDecoder` 和 `GifDecoderFactory` 就行——`decode_file` 这个"总流程"永远不需要知道世界上有多少种图片格式。

### 3.3 对比：简单工厂 vs 工厂方法

两者的区别就一句话：**简单工厂把 if-elif 集中在一个函数里（加类型 = 改函数）；工厂方法把创建逻辑下沉到子类（加类型 = 加类）**：

```python
# ===== 简单工厂：加一种动物就要改函数（修改）=====
class Dog:
    def speak(self):
        return "汪汪"


class Cat:
    def speak(self):
        return "喵喵"


def animal_factory_simple(kind: str):
    if kind == "dog":
        return Dog()
    elif kind == "cat":
        return Cat()
    # 加 Duck？改这个函数！——违反开闭原则


# ===== 工厂方法：加一种动物 = 加一对新类（扩展）=====
import abc


class Animal(abc.ABC):
    @abc.abstractmethod
    def speak(self) -> str:
        pass


class Duck(Animal):
    def speak(self) -> str:
        return "嘎嘎"


class AnimalCreator(abc.ABC):
    @abc.abstractmethod
    def create(self) -> Animal:
        pass


class DuckCreator(AnimalCreator):
    def create(self) -> Animal:
        return Duck()   # 新功能 = 新代码，旧代码一行不动


print("简单工厂：", animal_factory_simple("dog").speak())
print("工厂方法：", DuckCreator().create().speak())
```

运行输出：

```
简单工厂： 汪汪
工厂方法： 嘎嘎
```

> 简单工厂不是 GoF 23 模式之一，但它太常用、又是理解工厂方法的入口，所以第 2 章单独讲过。**当 if-elif 开始变多、类型开始频繁增加时，就该从简单工厂"升级"到工厂方法了。**

---

## 4. Python 特有玩法

### 4.1 `classmethod` 作为工厂方法：类方法多态

Python 里最地道的工厂方法，常常就是产品类上的一个 `classmethod`。妙处在于 `cls`：**子类调用继承来的 classmethod 时，`cls` 自动变成子类自己**——同一个方法，自动"造出"正确类型的对象：

```python
class Animal:
    """产品基类：同时充当自己的工厂"""

    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "……"

    @classmethod
    def from_line(cls, line: str):
        """工厂方法：从一行文本创建实例。
        关键在 cls——子类调用时，cls 自动是子类自己！"""
        name = line.strip().split(":")[0]
        return cls(name)


class Dog(Animal):
    def speak(self) -> str:
        return "汪汪"


class Cat(Animal):
    def speak(self) -> str:
        return "喵喵"


# 同一个工厂方法，子类调用自动返回子类实例——"类方法多态"
for animal in [Dog.from_line("旺财"), Cat.from_line("咪咪")]:
    print(f"{animal.name}说：{animal.speak()}")
```

运行输出：

```
旺财说：汪汪
咪咪说：喵喵
```

`from_line` 里没有一处 `if`，却能在 `Dog` 上造出狗、在 `Cat` 上造出猫——`cls` 就是那个"隐形的分派器"。

### 4.2 用 `abc` 定义工厂钩子：爬虫解析器

工厂方法经常和模板方法（第 8 章）配合：**主流程在基类里，创建对象的钩子留给子类**。看一个爬虫的例子——爬虫的主流程完全一致，只有"用什么解析器"不同：

```python
import abc
import json
from html.parser import HTMLParser


class PageParser(abc.ABC):
    """产品：网页解析器——从文本里提取链接"""

    @abc.abstractmethod
    def parse(self, text: str) -> list[str]:
        pass


class JsonApiParser(PageParser):
    """解析 JSON 接口返回里的 url 字段"""

    def parse(self, text: str) -> list[str]:
        data = json.loads(text)
        return [item["url"] for item in data["items"]]


class LinkCollector(HTMLParser):
    """收集 HTML 里的所有链接"""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for key, value in attrs:
                if key == "href":
                    self.links.append(value)


class HtmlLinkParser(PageParser):
    def parse(self, text: str) -> list[str]:
        collector = LinkCollector()
        collector.feed(text)
        return collector.links


class CrawlerFactory(abc.ABC):
    """抽象工厂：爬虫用什么解析器，由子类决定"""

    @abc.abstractmethod
    def create_parser(self) -> PageParser:
        pass


class JsonCrawlerFactory(CrawlerFactory):
    def create_parser(self) -> PageParser:
        return JsonApiParser()


class HtmlCrawlerFactory(CrawlerFactory):
    def create_parser(self) -> PageParser:
        return HtmlLinkParser()


def crawl(url: str, text: str, factory: CrawlerFactory) -> list[str]:
    """爬虫主流程：只依赖抽象，不关心具体解析器"""
    parser = factory.create_parser()   # 工厂方法：解析器从这里来
    links = parser.parse(text)
    print(f"从 {url} 提取到 {len(links)} 个链接")
    return links


json_text = '{"items": [{"url": "/a"}, {"url": "/b"}]}'
html_text = '<a href="/home">首页</a><a href="/about">关于</a>'
print(crawl("api.example.com", json_text, JsonCrawlerFactory()))
print(crawl("www.example.com", html_text, HtmlCrawlerFactory()))
```

运行输出：

```
从 api.example.com 提取到 2 个链接
['/a', '/b']
从 www.example.com 提取到 2 个链接
['/home', '/about']
```

### 4.3 注册表版：子类自己报名

Python 里还有一种常见玩法：**产品子类用装饰器把自己登记进注册表**，基类的 `create` 类方法按名字查找并创建。新增类型时连工厂类都不用写：

```python
class MessageEncoder:
    """产品基类 + 注册表：子类注册自己，create 按名字造"""

    _registry = {}

    @classmethod
    def register(cls, name: str):
        """装饰器：把子类登记进注册表"""
        def decorator(subclass):
            cls._registry[name] = subclass
            return subclass
        return decorator

    @classmethod
    def create(cls, name: str) -> "MessageEncoder":
        """工厂方法：按名字查注册表创建"""
        if name not in cls._registry:
            raise ValueError(f"未知编码器：{name}")
        return cls._registry[name]()

    def encode(self, text: str) -> str:
        raise NotImplementedError


@MessageEncoder.register("plain")
class PlainEncoder(MessageEncoder):
    def encode(self, text: str) -> str:
        return text


@MessageEncoder.register("upper")
class UpperEncoder(MessageEncoder):
    def encode(self, text: str) -> str:
        return text.upper()


# 新增编码器：加一个带 @register 的类即可，create 不用改
@MessageEncoder.register("reverse")
class ReverseEncoder(MessageEncoder):
    def encode(self, text: str) -> str:
        return text[::-1]


for name in ("plain", "upper", "reverse"):
    encoder = MessageEncoder.create(name)
    print(f"{name:>7}：{encoder.encode('你好世界')}")
```

运行输出：

```
  plain：你好世界
  upper：你好世界
 reverse：界世好你
```

这种"注册表 + 工厂方法"的组合在框架源码里遍地都是——Django 的缓存后端、logging 的处理器注册，思路同源。

---

## 5. 真实世界中的它

### 标准库：`asyncio` 的事件循环策略

`asyncio` 用"策略（Policy）"来决定创建哪种事件循环：`EventLoopPolicy.new_event_loop()` 就是一个工厂方法，不同平台（Windows / Unix）的策略子类返回不同的事件循环实现。你也可以继承默认策略、覆盖这个工厂方法，让整个程序都用上你的"特制循环"：

```python
import asyncio


class MyEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    """自定义策略：工厂方法 new_event_loop 由子类决定"""

    def new_event_loop(self):
        loop = super().new_event_loop()
        print("（自定义策略）事件循环已创建")
        return loop


policy = MyEventLoopPolicy()
loop = policy.new_event_loop()      # 工厂方法：造一个事件循环
print("是个合格的事件循环：", isinstance(loop, asyncio.AbstractEventLoop))
loop.close()
```

运行输出：

```
（自定义策略）事件循环已创建
是个合格的事件循环： True
```

平时你写 `asyncio.run(...)` 从不关心"循环怎么造的"——因为策略这个"工厂"已经在背后替你决定了。

### 框架：Django 的 `ModelForm` 元类机制

Django 的 `ModelForm` 也用到了工厂思想（不过是元类版）：你写 `class XForm(forms.ModelForm)` 并声明 `class Meta: model = X`，元类会读取模型定义，**自动生成**对应的表单字段类。你只负责"声明要什么"，字段怎么造、验证规则怎么配，由框架的元类工厂在背后完成。

### 框架：`unittest.TestLoader`

`unittest` 的 `TestLoader` 负责"从测试类里找出所有测试方法并实例化测试用例"——"测试对象从哪来、怎么造"由加载器决定，测试作者只需要按 `test_` 前缀命名。

---

## 6. 优缺点与适用场景

### 优点

- **符合开闭原则**：新增产品类型只加类，不改旧代码；
- **解耦**：客户端只依赖抽象 Creator / Product，替换实现无感；
- **创建逻辑内聚**：每个具体工厂只管自己那一种产品，职责单一。

### 缺点

- **类数量膨胀**：每加一种产品，就要加"产品 + 工厂"两个类，小项目里显得笨重；
- **抽象增加理解成本**：简单场景里，一个 if-elif 比五个类直白得多；
- **容易过度设计**：产品种类很少、几乎不变时，工厂方法纯属仪式感。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 产品类型经常增加、且需要统一创建入口 | 产品就一两种、也不会再变 |
| 客户端需要面向抽象编程（依赖倒置） | 简单场景（一个函数就能说清） |
| 创建过程复杂（参数校验、默认值、日志） | 创建只是 `return SomeClass()` 一行 |
| 框架/库要留给用户扩展点 | 代码库很小、团队不大时 |

> **Python 圈的共识**：能用 `classmethod`、注册表这些轻量玩法就别造一堆工厂类；工厂方法在 Python 里常常"缩水"成一个类方法。

---

## 7. 与其他模式的关系

- **工厂方法 vs 简单工厂**：简单工厂是"一个函数集中 if-elif"，工厂方法是"创建逻辑下沉子类"——前者是后者的退化版，后者是前者的开闭原则版（见 3.3）；
- **工厂方法 vs 抽象工厂**：抽象工厂是"**一组**工厂方法的集合"，负责生产**一族**相关的产品（第 14 章）；工厂方法只管**一种**产品；
- **工厂方法 + 模板方法**：模板方法（第 8 章）的骨架流程里，经常调用工厂方法去获得需要的对象——基类定流程，子类定"造什么"；
- **工厂方法 + 单例**：具体工厂常常做成单例（第 1 章），避免每次创建都 new 一个工厂对象。

---

## 8. 常见误区

### 误区 1：把工厂方法当成"换了个名字的简单工厂"

有人声明了抽象工厂类，结果实现里还是 if-elif 一串——**这只是把简单工厂搬了个家**。工厂方法的核心是"**子类覆盖 `create` 方法**"：

```python
class ConsoleLogger:
    def log(self, m):
        print(f"[控制台] {m}")


class FileLogger:
    def log(self, m):
        print(f"[文件] {m}")


class FakeFactory:
    """反面教材：抽象工厂里写 if-elif——本质还是简单工厂"""
    def create_logger(self, kind):
        if kind == "console":
            return ConsoleLogger()
        elif kind == "file":
            return FileLogger()
        raise ValueError(kind)


FakeFactory().create_logger("console").log("你好")
```

运行输出：

```
[控制台] 你好
```

判断标准很简单：**如果"加一种产品"还是要改这个工厂类，那它就不是工厂方法。**

### 误区 2：滥用工厂——简单场景也套工厂

只有一个产品、创建就是一行 `return`，也硬套一层工厂——这是为了模式而模式：

```python
# 反面：只有一个实现也套工厂——为了模式而模式
class Database:
    def connect(self):
        print("连接数据库")


class DatabaseFactory:
    """就一个产品，工厂毫无存在意义"""
    def create(self):
        return Database()


Database().connect()                 # 直接 new 就完了
DatabaseFactory().create().connect() # 工厂版没带来任何灵活性
```

运行输出：

```
连接数据库
连接数据库
```

工厂的价值在于"多态创建 + 扩展点"。没有这两样需求，别硬造工厂。

### 误区 3：工厂方法忘记返回"抽象类型"

工厂方法的返回值应该声明为抽象类型，否则客户端一依赖具体类，替换时就处处要改：

```python
# 反面：工厂方法返回具体类，调用方被迫依赖实现细节
class Notifier:
    def send(self, msg):
        print(f"通知：{msg}")


class EmailNotifier(Notifier):
    def send(self, msg):
        print(f"邮件：{msg}")


class BadFactory:
    def create(self) -> EmailNotifier:   # 返回类型写死成具体类
        return EmailNotifier()


# 想换 SmsNotifier？create 的签名、调用方的类型标注都要跟着改
class SmsNotifier(Notifier):
    def send(self, msg):
        print(f"短信：{msg}")


class GoodFactory:
    def create(self) -> Notifier:        # 返回抽象类型，替换无感
        return SmsNotifier()


print(type(BadFactory().create()).__name__)
print(type(GoodFactory().create()).__name__)
```

运行输出：

```
EmailNotifier
SmsNotifier
```

---

## 9. 练习题

### 练习 1：实现"支付方式工厂"

用工厂方法实现三种支付方式（支付宝 / 微信 / 银行卡），并让"收银台"只依赖抽象工厂：

```python
# 答案：产品族 + 一一对应的工厂子类
import abc


class Payment(abc.ABC):
    """产品：支付方式"""

    @abc.abstractmethod
    def pay(self, amount: float) -> str:
        pass


class Alipay(Payment):
    def pay(self, amount: float) -> str:
        return f"支付宝支付 {amount} 元"


class WechatPay(Payment):
    def pay(self, amount: float) -> str:
        return f"微信支付 {amount} 元"


class BankCard(Payment):
    def pay(self, amount: float) -> str:
        return f"银行卡支付 {amount} 元"


class PaymentFactory(abc.ABC):
    """抽象工厂：决定用哪种支付方式"""

    @abc.abstractmethod
    def create_payment(self) -> Payment:
        pass


class AlipayFactory(PaymentFactory):
    def create_payment(self) -> Payment:
        return Alipay()


class WechatFactory(PaymentFactory):
    def create_payment(self) -> Payment:
        return WechatPay()


class BankCardFactory(PaymentFactory):
    def create_payment(self) -> Payment:
        return BankCard()


def checkout(factory: PaymentFactory, amount: float) -> str:
    """收银台：只认抽象工厂"""
    return factory.create_payment().pay(amount)


print(checkout(AlipayFactory(), 66.6))
print(checkout(WechatFactory(), 88.8))
print(checkout(BankCardFactory(), 100.0))
```

运行输出：

```
支付宝支付 66.6 元
微信支付 88.8 元
银行卡支付 100.0 元
```

### 练习 2：把简单工厂重构为工厂方法

下面的 `create_simple` 是简单工厂。请重构为工厂方法结构（抽象工厂 + 两个具体工厂）：

```python
# 答案：抽象工厂 + 每个类型一个工厂子类
import abc


class Logger(abc.ABC):
    @abc.abstractmethod
    def log(self, m):
        pass


class ConsoleLogger(Logger):
    def log(self, m):
        print(f"[控制台] {m}")


class FileLogger(Logger):
    def log(self, m):
        print(f"[文件] {m}")


class LoggerFactory(abc.ABC):
    @abc.abstractmethod
    def create(self) -> Logger:
        pass


class ConsoleFactory(LoggerFactory):
    def create(self) -> Logger:
        return ConsoleLogger()


class FileFactory(LoggerFactory):
    def create(self) -> Logger:
        return FileLogger()


for factory in (ConsoleFactory(), FileFactory()):
    factory.create().log("重构完成")
```

运行输出：

```
[控制台] 重构完成
[文件] 重构完成
```

### 练习 3：用 `classmethod` 实现"从 URL 创建数据库连接"

写一个 `DbConnection` 类，用 `classmethod` 工厂方法 `from_url` 解析形如 `mysql://127.0.0.1:3306/orders` 的地址并创建连接对象：

```python
# 答案：classmethod 工厂方法——把"如何解析配置"交给类自己
class DbConnection:
    def __init__(self, host: str, port: int, db: str):
        self.host, self.port, self.db = host, port, db

    @classmethod
    def from_url(cls, url: str) -> "DbConnection":
        """工厂方法：从 URL 解析出连接参数"""
        # 形如 mysql://127.0.0.1:3306/orders
        scheme, rest = url.split("://")
        host_port, db = rest.split("/")
        host, port = host_port.split(":")
        return cls(host, int(port), db)

    def __repr__(self):
        return f"<DbConnection {self.host}:{self.port}/{self.db}>"


conn = DbConnection.from_url("mysql://127.0.0.1:3306/orders")
print(conn)
```

运行输出：

```
<DbConnection 127.0.0.1:3306/orders>
```

---

## 10. 小结与口诀

> **口诀：创建逻辑不集中，子类各自造英雄；加个类型加对类，旧码稳坐钓鱼台。**

工厂方法模式是"把变化点推给子类"的经典示范：**创建谁，子类说了算；怎么用，客户端说了算。** 记住三条：

1. 产品类型频繁增加时，从简单工厂**升级**到工厂方法；
2. 返回值永远声明为**抽象类型**，替换才无感；
3. Python 里优先用 `classmethod` / 注册表等轻量玩法，别一上来就堆工厂类。

下一章，我们来看与工厂方法配合最默契的行为型模式——**模板方法**：流程骨架固定，步骤细节交给子类。

---

*本章金句：工厂方法把"选择产品"的权力下放给子类——父类定规则，子类定产品，加新产品不碰旧代码。*
