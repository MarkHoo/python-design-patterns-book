# 第 21 章 桥接模式（Bridge）

> **一句话总结**：两个维度各自演化，组合出全部可能。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 结构型 | ★★★★☆ | ★★☆☆☆ |

---

## 1. 引子：先讲个故事

你家的遥控器能控制电视，但你换了一台新电视后，旧遥控器还能用吗？**能**——因为遥控器和你家的电视是"标准化"的：只要电视支持红外/蓝牙协议，任何遥控器都能配任何电视。遥控器和电视是**两个独立演化的维度**：电视厂商可以出新的电视型号（不用等遥控器厂商），遥控器厂商也可以出新的遥控器（不用等电视厂商），两边各自发展，用的时候任意组合。

现在想象一个反例：如果"遥控器"和"电视"必须绑定——索尼遥控器只能配索尼电视，三星遥控器只能配三星电视，那么市场上 10 个电视品牌 × 10 个遥控器型号就要造 **100 个"电视-遥控器"组合产品**。这就是**继承爆炸**。

程序世界里同样的故事天天上演。先看坏味道：

```python
# 引子：继承爆炸——消息发送 × 紧急程度，两两组合出 6 个类！
class Message:
    def send(self) -> None: ...


class NormalSMS(Message):
    def send(self) -> None:
        print("发送普通短信")


class UrgentSMS(Message):
    def send(self) -> None:
        print("发送加急短信：!!!")


class NormalEmail(Message):
    def send(self) -> None:
        print("发送普通邮件")


class UrgentEmail(Message):
    def send(self) -> None:
        print("发送加急邮件：!!!")


class NormalAppPush(Message):
    def send(self) -> None:
        print("发送普通 App 推送")


class UrgentAppPush(Message):
    def send(self) -> None:
        print("发送加急 App 推送：!!!")


for cls in (NormalSMS, UrgentSMS, NormalEmail, UrgentEmail, NormalAppPush, UrgentAppPush):
    cls().send()
```

运行输出：

```
发送普通短信
发送加急短信：!!!
发送普通邮件
发送加急邮件：!!!
发送普通 App 推送
发送加急 App 推送：!!!
```

才 3 种渠道 × 2 种紧急度就要 6 个类；如果再加一种渠道（钉钉）就是 8 个，再加一种紧急度（特急）就是 9 个——**类数量 = 维度 A × 维度 B × 维度 C……** 指数爆炸。

**桥接模式**就是治这个病的：把"渠道"和"紧急度"拆成两个独立的维度，用**组合**代替继承。

---

## 2. 模式登场

### 定义

> **桥接模式**：将抽象部分与实现部分分离，使它们都可以独立地变化。

"抽象部分"和"实现部分"容易误解，先翻译成人话：当一个事物有两个（或更多）**独立变化的维度**时，把每个维度做成一棵自己的类层次，再用"组合"把它们桥接起来。

### 解决的问题

1. **继承爆炸**：多维度组合用继承 = 笛卡尔积爆炸（2×3 变 6，3×4 变 12……）；
2. **耦合**：两个维度绑死在同一个类里，改一个维度动另一个；
3. **扩展难**：加新维度或新成员都要动一大片。

### 结构

```
         ┌────────────────────────┐
         │   Abstraction（抽象）    │
         │  - impl: Implementor   │─── 桥接：持有实现维度的引用 ───┐
         └───────────┬────────────┘                              │
                     │                                           ▼
        ┌────────────┴───────────┐                 ┌──────────────────────┐
        ▼                        ▼                 │  Implementor（实现）   │
┌───────────────┐      ┌───────────────┐           └───────────┬──────────┘
│ RefinedAbstraction │    │ RefinedAbstraction │                 │
│ （普通消息）         │    │ （加急消息）         │                 ▼
└───────────────┘      └───────────────┘        ┌──────────────────────┐
                                                │ ConcreteImplementor   │
                                                │ （短信/邮件/App 推送）   │
                                                └──────────────────────┘
```

### 角色

| 角色 | 说明 | 例子 |
|------|------|------|
| **Abstraction（抽象）** | 高层的控制逻辑，持有实现引用 | 消息（普通/加急） |
| **Implementor（实现）** | 底层的能力接口 | 发送渠道（短信/邮件/推送） |
| **RefinedAbstraction** | 抽象维度的具体变体 | 加急消息 |
| **ConcreteImplementor** | 实现维度的具体变体 | EmailSender |

> 注意：这里的"抽象/实现"不是"抽象类/实现类"的意思！"抽象"指**面向用户的控制层**（消息长什么样、怎么包装），"实现"指**底层能力**（怎么把字节送出去）。用 GoF 原书的例子理解最顺：**遥控器是抽象，电视机是实现**。

---

## 3. Python 实现

### 3.1 经典版：消息发送（渠道 × 紧急度）

```python
class Sender:
    """实现维度：发送渠道"""

    def send(self, content: str) -> None: ...


class SMSSender(Sender):
    def send(self, content: str) -> None:
        print(f"[短信] {content}")


class EmailSender(Sender):
    def send(self, content: str) -> None:
        print(f"[邮件] {content}")


class AppPushSender(Sender):
    def send(self, content: str) -> None:
        print(f"[App推送] {content}")


class Message:
    """抽象维度：消息（控制层），持有渠道引用"""

    def __init__(self, sender: Sender):
        self._sender = sender

    def send(self, content: str) -> None:
        self._sender.send(content)          # 把活交给渠道


class UrgentMessage(Message):
    """抽象维度的变体：加急消息"""

    def send(self, content: str) -> None:
        self._sender.send("【加急】" + content + "！！！")


# 组合：3 种渠道 × 2 种紧急度 = 6 种用法，只用了 5 个类
msgs = [
    Message(SMSSender()),
    Message(EmailSender()),
    UrgentMessage(SMSSender()),
    UrgentMessage(AppPushSender()),
]
for m in msgs:
    m.send("项目上线了")
```

运行输出：

```
[短信] 项目上线了
[邮件] 项目上线了
[短信] 【加急】项目上线了！！！
[App推送] 【加急】项目上线了！！！
```

**魔法就在这**：要加新渠道（钉钉），只需加一个 `DingTalkSender`，**一个类**搞定，普通/加急消息自动都能用；要加新紧急度（特急），加一个 `CriticalMessage`。新增量从"笛卡尔积"降为"线性"。

### 3.2 图形版：形状 × 渲染方式

```python
class Renderer:
    """实现维度：渲染引擎"""

    def draw_line(self, x1, y1, x2, y2) -> str: ...
    def draw_circle(self, cx, cy, r) -> str: ...


class AsciiRenderer(Renderer):
    """字符画渲染"""

    def draw_line(self, x1, y1, x2, y2) -> str:
        return f"ASCII 画线 ({x1},{y1})-({x2},{y2})"

    def draw_circle(self, cx, cy, r) -> str:
        return f"ASCII 画圆 圆心({cx},{cy}) 半径{r}"


class SvgRenderer(Renderer):
    """矢量渲染"""

    def draw_line(self, x1, y1, x2, y2) -> str:
        return f"<line x1={x1} y1={y1} x2={x2} y2={y2} />"

    def draw_circle(self, cx, cy, r) -> str:
        return f"<circle cx={cx} cy={cy} r={r} />"


class Shape:
    """抽象维度：形状"""

    def __init__(self, renderer: Renderer):
        self._renderer = renderer

    def render(self) -> None: ...


class Line(Shape):
    def __init__(self, renderer: Renderer, x1, y1, x2, y2):
        super().__init__(renderer)
        self._points = (x1, y1, x2, y2)

    def render(self) -> None:
        print(self._renderer.draw_line(*self._points))


class Circle(Shape):
    def __init__(self, renderer: Renderer, cx, cy, r):
        super().__init__(renderer)
        self._circle = (cx, cy, r)

    def render(self) -> None:
        print(self._renderer.draw_circle(*self._circle))


# 2 种形状 × 2 种渲染 = 4 种组合，只有 4 个类（没有桥接要 4 个类，但加维度就爆炸）
for shape in (Line(AsciiRenderer(), 0, 0, 10, 10),
              Circle(AsciiRenderer(), 5, 5, 3),
              Line(SvgRenderer(), 0, 0, 10, 10),
              Circle(SvgRenderer(), 5, 5, 3)):
    shape.render()
```

运行输出：

```
ASCII 画线 (0,0)-(10,10)
ASCII 画圆 圆心(5,5) 半径3
<line x1=0 y1=0 x2=10 y2=10 />
<circle cx=5 cy=5 r=3 />
```

### 3.3 设备版：遥控器 × 设备

回到开头的故事——遥控器与电视，GoF 原书风格的经典桥接：

```python
class Device:
    """实现维度：可遥控的设备"""

    def power_on(self) -> None: ...
    def power_off(self) -> None: ...
    def set_volume(self, level: int) -> None: ...


class TV(Device):
    def __init__(self):
        self._on = False
        self._volume = 10

    def power_on(self) -> None:
        self._on = True
        print("电视：开机")

    def power_off(self) -> None:
        self._on = False
        print("电视：关机")

    def set_volume(self, level: int) -> None:
        self._volume = max(0, min(100, level))
        print(f"电视：音量调到 {self._volume}")


class Radio(Device):
    def __init__(self):
        self._on = False
        self._volume = 20

    def power_on(self) -> None:
        self._on = True
        print("收音机：开机")

    def power_off(self) -> None:
        self._on = False
        print("收音机：关机")

    def set_volume(self, level: int) -> None:
        self._volume = max(0, min(100, level))
        print(f"收音机：音量调到 {self._volume}")


class RemoteControl:
    """抽象维度：遥控器"""

    def __init__(self, device: Device):
        self._device = device

    def toggle_power(self) -> None:
        print("按下电源键：", end="")
        self._device.power_on()      # 简化：演示只开机

    def volume_up(self) -> None:
        self._device.set_volume(self._current_volume() + 5)

    def _current_volume(self) -> int:
        # 演示用：假设当前音量是 10
        return 10


class AdvancedRemote(RemoteControl):
    """抽象维度变体：高级遥控器（带静音）"""

    def mute(self) -> None:
        print("按下静音键：", end="")
        self._device.set_volume(0)


tv_remote = RemoteControl(TV())
tv_remote.toggle_power()
tv_remote.volume_up()

radio_remote = AdvancedRemote(Radio())
radio_remote.toggle_power()
radio_remote.mute()
```

运行输出：

```
按下电源键：电视：开机
电视：音量调到 15
按下电源键：收音机：开机
按下静音键：收音机：音量调到 0
```

**任何遥控器都能配任何设备**——这就是桥接给我们的自由：设备维度加投影仪、遥控器维度加"语音遥控器"，互不干扰。

---

## 4. Python 特有玩法

### 4.1 用协议（Protocol）代替抽象基类

Python 的鸭子类型让"实现维度"连继承都不用——只要长得像就行：

```python
from typing import Protocol


class Sender(Protocol):
    """实现维度：协议（结构性子类型，无需继承）"""

    def send(self, content: str) -> None: ...


class WeChatSender:
    """微信渠道：没继承任何类，只是长得像 Sender"""
    def send(self, content: str) -> None:
        print(f"[微信] {content}")


class Notice:
    """抽象维度：通知"""

    def __init__(self, sender: Sender):
        self._sender = sender

    def push(self, content: str) -> None:
        self._sender.send(content)


Notice(WeChatSender()).push("今晚 8 点上线评审")
```

运行输出：

```
[微信] 今晚 8 点上线评审
```

### 4.2 函数即实现维度

如果"实现维度"只有一两个方法，它甚至不需要是类——**一个函数就是最小的实现**：

```python
class Alarm:
    """抽象维度：闹钟"""

    def __init__(self, notifier):
        self._notifier = notifier      # 函数注入

    def fire(self, reason: str) -> None:
        self._notifier(f"【告警】{reason}")


def email_notify(text: str) -> None:
    print(f"[邮件] {text}")


def sms_notify(text: str) -> None:
    print(f"[短信] {text}")


Alarm(email_notify).fire("CPU 温度过高")
Alarm(sms_notify).fire("磁盘空间不足")
```

运行输出：

```
[邮件] 【告警】CPU 温度过高
[短信] 【告警】磁盘空间不足
```

**加一种通知方式 = 加一个函数**，Alarm 一行不改。这正是 Python 里桥接的"轻量版"——当维度足够简单时，函数就是最好的 Implementor。

---

## 5. 真实世界中的它

### 标准库：`logging` 的 Handler × Formatter

`logging` 模块是桥接思想的典范：**输出渠道（Handler：控制台/文件/网络）** 和 **消息格式（Formatter）** 是两个独立维度，自由组合：

```python
import logging
import sys

# 维度一：Handler（输出渠道）
console = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("app.log", encoding="utf-8")

# 维度二：Formatter（消息格式）——同一个渠道可以换不同格式
fmt_simple = logging.Formatter("%(message)s")
fmt_detail = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

console.setFormatter(fmt_simple)        # 控制台：简单格式
file_handler.setFormatter(fmt_detail)   # 文件：详细格式

logger = logging.getLogger("bridge_demo")
logger.setLevel(logging.INFO)
logger.addHandler(console)
logger.addHandler(file_handler)

logger.info("这是一条测试日志")
```

运行输出：

```
这是一条测试日志
```

> 运行后目录下会生成 `app.log`，里面是带时间戳的详细格式；控制台则是简洁格式。Handler 和 Formatter 各自演化、任意组合——**这就是桥接**。（本示例的工作目录是隔离的临时目录，日志文件不会污染书目录。）

### 框架：SQLAlchemy 的 Dialect

SQLAlchemy 把"SQL 生成/方言"（Dialect：MySQL、PostgreSQL、SQLite……）与"数据库连接/驱动"（DBAPI）分离成独立维度：你的业务代码只依赖抽象层（`Engine`），换数据库时只换 Dialect，业务代码一行不改。

### GUI 工具包：样式 × 控件

Qt 的 QStyle 与控件体系、Tk 的 theme 与 widget——"外观主题"和"控件结构"也是桥接式的两个维度。

---

## 6. 优缺点与适用场景

### 优点

- **告别继承爆炸**：多维度组合从"乘法"变"加法"；
- **开闭原则**：新增维度成员只加一个类，不动其他维度；
- **独立演化**：两个维度可以分别测试、分别升级。

### 缺点

- **结构变复杂**：多了一层间接调用，小场景下显得"过度设计"；
- **维度划分要准确**：分错维度（把不是独立变化的维度拆开）反而更乱；
- **调试多一跳**：调用链变长（消息 → 渠道 → 底层）。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 两个维度都**独立变化**且组合数爆炸 | 只有一两个变体（直接 if 就够） |
| 跨平台/多渠道/多格式类需求 | 维度之间强耦合、不会单独变化 |
| 需要"自由组合"的产品线 | 简单场景（YAGNI：你可能不需要它） |

> **判断口诀**：问自己"这个类的两个变化方向，会不会各自独立地变？"——会，才用桥接。

---

## 7. 与其他模式的关系

- **桥接 vs 适配器**：适配器是"事后补救"——接口不兼容了，加个转换层；桥接是"事前设计"——一开始就把两个维度拆开。适配器让"已有的"能一起工作，桥接让"未来的"能各自演化；
- **桥接 + 抽象工厂**：桥接的两个维度常常由抽象工厂来创建（第 14 章），组合使用很常见；
- **桥接 vs 策略**：策略是"一个维度换算法"；桥接是"两个维度自由组合"——桥接的实现维度内部可以再用策略；
- **桥接 vs 装饰器**：装饰器是单链包装（一条线），桥接是双维度交叉（一张网）。

---

## 8. 常见误区

### 误区 1：把桥接当成"依赖注入"就完事了

依赖注入（构造函数传对象）是手段，**桥接的关键是"两个维度都要能独立扩展"**。只注入不拆维度，等于只做了一半。

```python
# 误区：只有一个维度，却硬套桥接
class Report:
    def __init__(self, writer):     # writer 只是依赖注入
        self._writer = writer

    def generate(self) -> None:
        self._writer.write("报表内容")
```

这不算桥接——因为 Report 只有一个变化维度。桥接需要**至少两个交叉维度**。

### 误区 2：维度划分错误

把"短信渠道"和"加急消息"拆成两个维度没问题；但如果"加急"逻辑强依赖"短信"的特殊能力（比如短信有签名、邮件没有），说明它们不是独立维度，强行拆开会得到"跨维度耦合"的桥。

### 误区 3：用桥接解决"组合爆炸"，但维度其实不会变

如果一个维度永远只有一个实现（比如公司只用一种消息渠道），桥接就是纯纯的过度设计。**先让代码跑起来，等第二个维度变体出现时再桥接**（YAGNI 原则）。

### 误区 4：桥接和策略分不清

两者都靠"组合 + 注入"，但关注点不同：策略解决"同一个维度怎么换算法"（换一种折扣），桥接解决"多个维度怎么自由组合"（渠道 × 紧急度）。桥接的实现维度内部可以用策略，但桥接解决的是**维度之间的解耦**。

---

## 9. 练习题

### 练习 1：用桥接重构"日志系统"

现有需求：输出渠道（控制台/文件）× 日志级别过滤（INFO/ERROR 全收 or 只收 ERROR）。用桥接实现：

```python
class Sink:
    """实现维度：输出目标"""

    def write(self, line: str) -> None: ...


class ConsoleSink(Sink):
    def write(self, line: str) -> None:
        print(f"[控制台] {line}")


class FileSink(Sink):
    def write(self, line: str) -> None:
        print(f"[文件] {line}")     # 演示用：真实场景应写入文件


class Logger:
    """抽象维度：日志器（含级别过滤）"""

    def __init__(self, sink: Sink, level: str = "INFO"):
        self._sink = sink
        self._level = level

    def _allowed(self, level: str) -> bool:
        order = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
        return order[level] >= order[self._level]

    def log(self, level: str, msg: str) -> None:
        if self._allowed(level):
            self._sink.write(f"[{level}] {msg}")


console_logger = Logger(ConsoleSink(), level="INFO")
error_file_logger = Logger(FileSink(), level="ERROR")

console_logger.log("INFO", "用户登录成功")
console_logger.log("ERROR", "数据库连接失败")
error_file_logger.log("INFO", "这行不该出现")
error_file_logger.log("ERROR", "磁盘写入失败")
```

运行输出：

```
[控制台] [INFO] 用户登录成功
[控制台] [ERROR] 数据库连接失败
[文件] [ERROR] 磁盘写入失败
```

### 练习 2：给图形版加第三个维度——"边框样式"

在 3.2 的基础上，说出加"边框样式（无/虚线/双线）"维度后，桥接方案要加几个类？（答案：3 个——每个样式一个类，或 1 个类 + 参数；对比继承方案要 形状×渲染×边框 = 2×2×3 = 12 个类）

```python
# 答案思路：边框样式属于"渲染"维度的扩展——给 Renderer 加一个 draw_border 方法
class Renderer:
    def draw_border(self, style: str) -> str:
        return f"绘制{style}边框"


class AsciiRenderer(Renderer):
    def draw_border(self, style: str) -> str:
        return f"ASCII 绘制{style}边框"


class SvgRenderer(Renderer):
    def draw_border(self, style: str) -> str:
        return f"<rect stroke-dasharray={style!r} />"


for r in (AsciiRenderer(), SvgRenderer()):
    print(r.draw_border("虚线"))
```

运行输出：

```
ASCII 绘制虚线边框
<rect stroke-dasharray='虚线' />
```

### 练习 3：函数即实现维度

把 3.1 的 Sender 改成函数式写法——渠道用函数，消息类不变：

```python
class Message:
    """抽象维度：消息（渠道改为函数注入）"""

    def __init__(self, send_func):
        self._send = send_func

    def send(self, content: str) -> None:
        self._send(content)


def sms(content: str) -> None:
    print(f"[短信] {content}")


def dingtalk(content: str) -> None:
    print(f"[钉钉] {content}")


Message(sms).send("开会了")
Message(dingtalk).send("代码评审 2 点开始")
```

运行输出：

```
[短信] 开会了
[钉钉] 代码评审 2 点开始
```

---

## 10. 小结与口诀

> **口诀：两个维度各自变，组合靠桥不靠继；乘法变加法，类不再爆炸。**

桥接模式是"组合优于继承"最纯粹的教科书：把"遥控器"和"电视"拆开，各自演化，用时自由组合。它是本书结构型模式的收尾之作，也是难度较高的一个——**难点不在实现，而在判断"这俩是不是真的独立维度"**。

下一章，我们进入行为型模式的压轴戏——**访问者**：数据结构不动，操作随便加。

---

*本章金句：桥接说：别让两个维度互相绑架——遥控器归遥控器，电视归电视，用时再牵手。*
