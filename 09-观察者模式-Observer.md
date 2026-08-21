# 第 9 章 观察者模式（Observer）

> **一句话总结**：有事广播，订阅者自知，互不认识。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 行为型 | ★★☆☆☆ | ★★★★☆ |

---

## 1. 引子：先讲个故事

你关注了一个公众号。博主每次发文，你都会收到推送；你取关了，推送就停了。注意一个细节：**博主根本不知道你是谁**，他只需要维护一份"粉丝列表"，发文时挨个发一遍——至于哪个粉丝是程序员、哪个是学生，他一概不关心。粉丝之间也互不认识：张三收到推送不会通知李四。

这种"**一个发布者，很多订阅者，发布者不认识订阅者**"的协作方式，就是观察者模式的灵魂。反过来说，如果博主每次发文都要手动挨个打电话通知粉丝，那公众号就完蛋了——而很多程序就是这么写的：

```python
# 引子：订单类里写死通知渠道——加一个渠道就要改订单类
class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.status = "待支付"

    def update_status(self, new_status):
        self.status = new_status
        print(f"订单 {self.order_id} 状态变更为：{new_status}")
        # ↓ 写死的通知逻辑：改订单状态还得顺带管通知
        self._send_email()
        self._send_sms()

    def _send_email(self):
        print(f"  [邮件] 订单 {self.order_id} 状态更新：{self.status}")

    def _send_sms(self):
        print(f"  [短信] 订单 {self.order_id} 状态更新：{self.status}")


order = Order("A001")
order.update_status("已支付")
order.update_status("已发货")
```

运行输出：

```
订单 A001 状态变更为：已支付
  [邮件] 订单 A001 状态更新：已支付
  [短信] 订单 A001 状态更新：已支付
订单 A001 状态变更为：已发货
  [邮件] 订单 A001 状态更新：已发货
  [短信] 订单 A001 状态更新：已发货
```

痛点在哪儿？**订单类被通知逻辑绑架了**。明天要加 App 推送？改 `Order` 类！后天要"发货后通知物流公司"？再改 `Order` 类！订单类变成了"改谁都疼"的万能膏药，违反了**开闭原则**和**单一职责原则**。

**观察者模式**就是来解耦的：订单只负责"状态变了"，至于谁关心、怎么通知，交给订阅者自己。

---

## 2. 模式登场

### 定义

> **观察者模式**：定义对象间一对多的依赖关系。当一个对象（被观察者 Subject）状态改变时，所有依赖它的对象（观察者 Observer）都会收到通知并自动更新。

### 解决的问题

1. **解耦**：Subject 不认识 Observer 的具体类型，只认识"它们有 update 方法"；
2. **一对多广播**：一个变化同时通知所有关心它的对象；
3. **动态增减**：观察者可以随时注册（订阅）、注销（取关），Subject 不用改代码。

### 结构

```
        ┌────────────────────────────┐
        │       Subject（主题）         │
        ├────────────────────────────┤
        │ + attach(observer)         │
        │ + detach(observer)         │
        │ + notify()                 │
        └──────────────┬─────────────┘
                       │ 通知所有观察者
                       ▼
        ┌────────────────────────────┐
        │       Observer（观察者）      │
        ├────────────────────────────┤
        │ + update(event)            │
        └──────────────┬─────────────┘
                       ▲
          ┌────────────┴────────────┐
          ▼                         ▼
┌───────────────────┐   ┌───────────────────┐
│ ConcreteObserverA │   │ ConcreteObserverB │
└───────────────────┘   └───────────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **Subject（被观察者/主题）** | 维护观察者列表，状态变化时广播通知 |
| **Observer（观察者）** | 定义接收通知的接口（`update`） |
| **ConcreteSubject（具体主题）** | 真正的状态持有者 |
| **ConcreteObserver（具体观察者）** | 收到通知后做出自己的反应 |

> 核心一句话：**Subject 只认"观察者长什么样"（有 update 方法），不认"观察者是谁"。**

---

## 3. Python 实现

### 3.1 经典版：股票行情推送

股票交易所的行情一变，手机 App、交易所大屏都要跟着更新——正是典型的"一对多广播"：

```python
import abc


class Observer(abc.ABC):
    """观察者接口：所有想被通知的对象都实现 update"""

    @abc.abstractmethod
    def update(self, symbol: str, price: float) -> None:
        pass


class StockMarket:
    """被观察者（主题）：维护观察者列表，行情一变就广播"""

    def __init__(self):
        self._observers = []
        self._prices = {}

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def set_price(self, symbol: str, price: float) -> None:
        self._prices[symbol] = price
        print(f"【行情】{symbol} 最新价 {price}")
        self._notify(symbol, price)

    def _notify(self, symbol: str, price: float) -> None:
        for observer in self._observers:
            observer.update(symbol, price)


class AppClient(Observer):
    """手机 App 客户端"""

    def update(self, symbol: str, price: float) -> None:
        print(f"  [App] {symbol} 价格变动提醒：{price}")


class BigScreen(Observer):
    """交易所大屏"""

    def update(self, symbol: str, price: float) -> None:
        print(f"  [大屏] 滚动显示 {symbol}：{price}")


market = StockMarket()
app = AppClient()
screen = BigScreen()
market.attach(app)
market.attach(screen)

market.set_price("AAPL", 188.5)
market.detach(app)          # 注销：App 不再接收通知
market.set_price("AAPL", 190.2)
```

运行输出：

```
【行情】AAPL 最新价 188.5
  [App] AAPL 价格变动提醒：188.5
  [大屏] 滚动显示 AAPL：188.5
【行情】AAPL 最新价 190.2
  [大屏] 滚动显示 AAPL：190.2
```

`StockMarket` 完全不认识 `AppClient` 和 `BigScreen`——它只遍历"观察者列表"挨个喊一声。**加一个新的客户端？写个类实现 update，attach 一下，完事。**

### 3.2 订单状态通知：邮件 + 短信 + App

回到引子的场景，用观察者重写：订单只管状态，通知渠道各自订阅：

```python
import abc


class OrderNotifier(abc.ABC):
    """观察者：订单通知渠道"""

    @abc.abstractmethod
    def notify(self, order_id: str, status: str) -> None:
        pass


class EmailNotifier(OrderNotifier):
    def notify(self, order_id, status):
        print(f"  [邮件] 订单 {order_id} 状态：{status}")


class SmsNotifier(OrderNotifier):
    def notify(self, order_id, status):
        print(f"  [短信] 订单 {order_id} 状态：{status}")


class AppPushNotifier(OrderNotifier):
    def notify(self, order_id, status):
        print(f"  [App推送] 订单 {order_id} 状态：{status}")


class Order:
    """被观察者：订单状态变化时通知所有订阅渠道"""

    def __init__(self, order_id: str):
        self.order_id = order_id
        self.status = "待支付"
        self._channels = []

    def subscribe(self, channel: OrderNotifier) -> None:
        self._channels.append(channel)

    def unsubscribe(self, channel: OrderNotifier) -> None:
        self._channels.remove(channel)

    def update_status(self, new_status: str) -> None:
        self.status = new_status
        print(f"订单 {self.order_id} → {new_status}")
        for channel in self._channels:
            channel.notify(self.order_id, self.status)


order = Order("A001")
email, sms, app = EmailNotifier(), SmsNotifier(), AppPushNotifier()
order.subscribe(email)
order.subscribe(sms)

print("--- 只订了邮件和短信 ---")
order.update_status("已支付")

print("--- 用户又订了 App 推送 ---")
order.subscribe(app)
order.update_status("已发货")

print("--- 用户退订短信 ---")
order.unsubscribe(sms)
order.update_status("已签收")
```

运行输出：

```
--- 只订了邮件和短信 ---
订单 A001 → 已支付
  [邮件] 订单 A001 状态：已支付
  [短信] 订单 A001 状态：已支付
--- 用户又订了 App 推送 ---
订单 A001 → 已发货
  [邮件] 订单 A001 状态：已发货
  [短信] 订单 A001 状态：已发货
  [App推送] 订单 A001 状态：已发货
--- 用户退订短信 ---
订单 A001 → 已签收
  [邮件] 订单 A001 状态：已签收
  [App推送] 订单 A001 状态：已签收
```

看到区别了吗？**`Order` 类从此再也不用改**。加 App 推送？写个 `AppPushNotifier` 订阅一下。用户退订？`unsubscribe` 一下。订单类和通知渠道彻底解耦——这就是观察者模式的价值。

### 3.3 事件系统变体：按事件名订阅

真实系统里，"通知"往往按**事件类型**分发：订单创建、订单支付、订单退款……不同事件有不同订阅者。于是观察者模式演化出"事件总线"形态：

```python
class EventBus:
    """迷你事件总线：按事件名订阅，一对多广播"""

    def __init__(self):
        self._handlers = {}

    def on(self, event: str, handler) -> None:
        """订阅：给某类事件注册处理器"""
        self._handlers.setdefault(event, []).append(handler)

    def off(self, event: str, handler) -> None:
        self._handlers[event].remove(handler)

    def emit(self, event: str, payload) -> None:
        """发布：触发某类事件的所有处理器"""
        print(f"触发事件：{event}")
        for handler in self._handlers.get(event, []):
            handler(payload)


def log_order(payload):
    print(f"  [日志] 记录订单 {payload}")


def send_coupon(payload):
    print(f"  [营销] 给订单 {payload} 发优惠券")


bus = EventBus()
bus.on("order.created", log_order)
bus.on("order.created", send_coupon)
bus.on("order.paid", log_order)

bus.emit("order.created", "A001")
bus.emit("order.paid", "A001")
```

运行输出：

```
触发事件：order.created
  [日志] 记录订单 A001
  [营销] 给订单 A001 发优惠券
触发事件：order.paid
  [日志] 记录订单 A001
```

同一个事件可以有多个订阅者，同一段逻辑可以订阅多个事件——事件总线是观察者模式在生产环境最常见的形态（后面 5.2 的 Django signals 就是它的"完全体"）。

---

## 4. Python 特有玩法

### 4.1 观察者就是函数：回调列表

GoF 时代，观察者必须是个类。Python 里函数是一等公民，**观察者直接就是普通函数**，Subject 里存一个回调列表就行：

```python
class WechatOfficialAccount:
    """公众号：观察者就是普通函数"""

    def __init__(self, name: str):
        self.name = name
        self._followers = []          # 列表里存的是函数

    def follow(self, callback) -> None:
        """关注：传入一个函数作为观察者"""
        self._followers.append(callback)

    def unfollow(self, callback) -> None:
        self._followers.remove(callback)

    def publish(self, article: str) -> None:
        print(f"📢 {self.name} 发布：《{article}》")
        for callback in self._followers:
            callback(self.name, article)


def fan_zhang(account, article):
    print(f"  张三收到推送：{account} 更新了《{article}》")


def fan_li(account, article):
    print(f"  李四点赞：《{article}》")


account = WechatOfficialAccount("Python 设计模式")
account.follow(fan_zhang)
account.follow(fan_li)
account.publish("观察者模式入门")
account.unfollow(fan_zhang)
account.publish("工厂方法入门")
```

运行输出：

```
📢 Python 设计模式 发布：《观察者模式入门》
  张三收到推送：Python 设计模式 更新了《观察者模式入门》
  李四点赞：《观察者模式入门》
📢 Python 设计模式 发布：《工厂方法入门》
  李四点赞：《工厂方法入门》
```

没有 `Observer` 抽象类、没有 `update` 方法——**函数本身就是观察者**。这是 Python 里最轻量的观察者写法。

### 4.2 用 `weakref` 弱引用，避免"观察者泄漏在主题里"

观察者模式有个经典坑：**忘了注销的观察者会被主题强引用，永远无法回收**。Python 的 `weakref` 弱引用是治它的良药——主题只"弱弱地"握着观察者，观察者被别处删掉后，弱引用自动失效，通知时自动跳过：

```python
import gc
import weakref


class Subject:
    """主题：用弱引用保存观察者，避免泄漏"""

    def __init__(self):
        self._observers = []

    def attach(self, observer) -> None:
        # 存的是弱引用，不增加对象的"存活负担"
        self._observers.append(weakref.ref(observer))

    def notify(self, message: str) -> None:
        alive = []
        for ref in self._observers:
            observer = ref()
            if observer is not None:
                observer.update(message)
                alive.append(ref)
            # observer 已被回收？弱引用取到 None，自动清掉
        self._observers = alive


class Widget:
    def __init__(self, name: str):
        self.name = name

    def update(self, message: str) -> None:
        print(f"  [{self.name}] 收到：{message}")


subject = Subject()
w1 = Widget("窗口A")
w2 = Widget("窗口B")
subject.attach(w1)
subject.attach(w2)

print("--- 两个观察者都在 ---")
subject.notify("刷新列表")

# w1 被销毁了，但没人记得调用 detach
del w1
gc.collect()

print("--- w1 已被回收，通知不再报错 ---")
subject.notify("再次刷新")
print("剩余观察者数量：", len(subject._observers))
```

运行输出：

```
--- 两个观察者都在 ---
  [窗口A] 收到：刷新列表
  [窗口B] 收到：刷新列表
--- w1 已被回收，通知不再报错 ---
  [窗口B] 收到：再次刷新
剩余观察者数量： 1
```

`w1` 被 `del` 之后，弱引用自动失效，下一次 `notify` 把它从列表里清掉——**不用手动 detach，也不会泄漏**。

### 4.3 `@dataclass` 事件对象

通知不能只传一个状态字符串——真实事件带着一堆上下文（订单号、金额、备注……）。用 `dataclass` 定义事件对象，观察者的 `update` 收到的是一个结构清晰的对象：

```python
from dataclasses import dataclass


@dataclass
class OrderEvent:
    """事件对象：携带完整上下文，比裸参数更清晰"""
    order_id: str
    status: str
    amount: float = 0.0
    note: str = ""


class OrderTracker:
    """被观察者：发布 OrderEvent 事件对象"""

    def __init__(self):
        self._handlers = []

    def on_change(self, handler) -> None:
        self._handlers.append(handler)

    def change(self, event: OrderEvent) -> None:
        print(f"状态变更：{event.order_id} → {event.status}")
        for handler in self._handlers:
            handler(event)


def audit_log(event: OrderEvent) -> None:
    print(f"  [审计] {event.order_id} {event.status} 金额={event.amount} 备注={event.note}")


def notify_user(event: OrderEvent) -> None:
    if event.status == "已退款":
        print(f"  [通知] 您的订单 {event.order_id} 已退款 {event.amount} 元")


tracker = OrderTracker()
tracker.on_change(audit_log)
tracker.on_change(notify_user)

tracker.change(OrderEvent(order_id="A001", status="已支付", amount=199.0))
tracker.change(OrderEvent(order_id="A001", status="已退款", amount=199.0, note="七天无理由"))
```

运行输出：

```
状态变更：A001 → 已支付
  [审计] A001 已支付 金额=199.0 备注=
状态变更：A001 → 已退款
  [审计] A001 已退款 金额=199.0 备注=七天无理由
  [通知] 您的订单 A001 已退款 199.0 元
```

观察者收到的是"完整的事件"，而不是一堆散参数——`dataclass` 让事件的构造和读取都赏心悦目。

---

## 5. 真实世界中的它

### 标准库：`asyncio.Future.add_done_callback`

`asyncio` 的 `Future` / `Task` 就是被观察者：任务完成时，所有通过 `add_done_callback` 注册的回调都会被调用——这正是观察者模式（回调就是观察者）：

```python
import asyncio


def on_done(task) -> None:
    """观察者回调：任务完成时被调用"""
    print("回调收到任务结果：", task.result())


async def download() -> str:
    await asyncio.sleep(0.05)
    return "下载完成，共 1.2MB"


async def main() -> None:
    task = asyncio.create_task(download())   # 被观察者：任务
    task.add_done_callback(on_done)          # 注册观察者：完成回调
    await task                               # 等任务完成
    print("主流程继续：任务已结束")


asyncio.run(main())
```

运行输出：

```
回调收到任务结果： 下载完成，共 1.2MB
主流程继续：任务已结束
```

你注册回调，却不需要轮询任务状态——任务完成时框架"打电话"给你。观察者模式让异步代码不用 `while True` 干等。

### 框架：Django 的 signals

Django 的 `signal`（`post_save`、`pre_delete` 等）是观察者模式的框架级实现：模型保存时触发 `post_save`，所有 `connect` 过的 receiver 都会被调用。receiver 之间互不认识，只管处理自己关心的信号——日志、缓存失效、发送通知，全靠它串联，模型类本身一行通知代码都不用写。

### 框架：tkinter 的 `bind`

GUI 编程也是观察者的天下：`widget.bind("<Button-1>", handler)` 就是"我关心点击事件，请在我被点击时调用我"。控件是主题，事件是通知，handler 是观察者。

---

## 6. 优缺点与适用场景

### 优点

- **彻底解耦**：Subject 不认识 Observer 的具体类型，加新观察者不用改 Subject；
- **一对多广播**：一次变化，所有订阅者自动更新；
- **动态订阅**：运行时随时注册、注销，开闭原则的模范生。

### 缺点

- **通知顺序不可控**：观察者的执行顺序依赖注册顺序，谁先谁后容易埋雷；
- **回调异常会传染**：一个观察者抛异常，可能中断整个通知链（见误区 1）；
- **过度通知**：观察者多了，一次变化引发连锁反应，出问题难排查；
- **内存泄漏隐患**：忘注销的观察者被主题强引用，回收不掉（见误区 2）。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 一个变化要通知多个对象（行情、订单、消息） | 只有一对一调用 |
| 观察者数量会动态变化 | 通知链又长又深（考虑事件总线/队列） |
| 需要解耦事件源与事件处理 | 观察者之间有强依赖关系 |
| 事件驱动架构、GUI、异步回调 | 简单场景（直接函数调用更直白） |

> **Python 圈的共识**：Python 里观察者常常就是"回调函数列表"；需要按事件分类时，升级成事件总线（dict 存回调列表）。

---

## 7. 与其他模式的关系

- **观察者 vs 发布-订阅**：观察者模式里 Subject **直接**调用 Observer；发布-订阅（Pub/Sub）中间隔着**消息代理**（channel/topic），发布者和订阅者完全不知道对方存在。3.3 的 `EventBus` 就是"半个发布-订阅"——按事件名分发，但还没有独立的中间人；
- **观察者 vs 中介者**：观察者是一对多**单向**广播；中介者（第 19 章）是多对多**双向**协调——观察者解决"一个变了通知一群"，中介者解决"一群互相乱打电话"；
- **观察者 + 状态**：状态模式（第 16 章）里状态一变化，常常就触发观察者通知——两者经常成对出现；
- **观察者 + 单例**：事件总线/主题对象常常做成单例（第 1 章），全程序共享一个"广播台"。

---

## 8. 常见误区

### 误区 1：回调抛异常导致通知中断

一个观察者处理逻辑炸了，异常直接冒泡，后面的观察者全都收不到通知——**一个人的锅，全队买单**：

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, fn):
        self._observers.append(fn)

    def notify_bad(self, msg):     # 反面：一个观察者炸了，后面的全收不到
        for fn in self._observers:
            fn(msg)

    def notify_good(self, msg):    # 正确：每个通知都包一层 try/except
        for fn in self._observers:
            try:
                fn(msg)
            except Exception as e:
                print(f"  观察者 {fn.__name__} 出错，已隔离：{e}")


def observer_a(msg):
    print(f"  [A] 收到 {msg}")


def observer_b(msg):
    raise ValueError("B 的处理逻辑炸了")


def observer_c(msg):
    print(f"  [C] 收到 {msg}")


s = Subject()
s.attach(observer_a)
s.attach(observer_b)
s.attach(observer_c)

print("--- 反面：通知中断 ---")
try:
    s.notify_bad("事件1")
except ValueError as e:
    print("  异常冒泡上来，C 永远收不到：", e)

print("--- 正确：异常隔离 ---")
s.notify_good("事件2")
```

运行输出：

```
--- 反面：通知中断 ---
  [A] 收到 事件1
  异常冒泡上来，C 永远收不到： B 的处理逻辑炸了
--- 正确：异常隔离 ---
  [A] 收到 事件2
  观察者 observer_b 出错，已隔离：B 的处理逻辑炸了
  [C] 收到 事件2
```

**生产环境的标准做法**：`notify` 里给每个观察者包 `try/except`，一个挂了不连累别人，还要记日志方便排查。

### 误区 2：忘记注销观察者，内存泄漏

观察者被删了，但忘了 `detach`——主题还强引用着它，垃圾回收拿它没办法，内存悄悄涨：

```python
import gc


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, o):
        self._observers.append(o)


class BigWidget:
    def __init__(self, name):
        self.name = name

    def update(self, msg):
        pass


s = Subject()
w = BigWidget("大窗口")
s.attach(w)
print("删除前，主题持有观察者数量：", len(s._observers))

del w            # 窗口关了，但忘了 detach
gc.collect()

count = sum(1 for obj in gc.get_objects() if type(obj).__name__ == "BigWidget")
print("删除后，BigWidget 实例仍存活：", count, "（被主题强引用，无法回收——泄漏！）")
```

运行输出：

```
删除前，主题持有观察者数量： 1
删除后，BigWidget 实例仍存活： 1 （被主题强引用，无法回收——泄漏！）
```

**解决办法**：要么保证成对调用 `attach`/`detach`，要么直接用 4.2 的 `weakref` 弱引用，让"忘了注销"也没事。

### 误区 3：依赖通知顺序

观察者的执行顺序就是注册顺序——**谁先注册谁先收到**。如果业务逻辑依赖"A 必须在 B 之前执行"，换个注册顺序结果就变了，这是定时炸弹：

```python
# 反面：观察者 A 假设自己一定在 B 之前被通知
class Order:
    def __init__(self):
        self._observers = []

    def attach(self, fn, name):
        self._observers.append((name, fn))

    def notify(self):
        for name, fn in self._observers:
            fn(name)


def first(name):
    print(f"{name} 先执行：扣库存")


def second(name):
    print(f"{name} 后执行：发货")


o = Order()
o.attach(first, "A")
o.attach(second, "B")
o.notify()

print("--- 换个注册顺序，结果就变了 ---")
o2 = Order()
o2.attach(second, "B")
o2.attach(first, "A")
o2.notify()
```

运行输出：

```
A 先执行：扣库存
B 后执行：发货
--- 换个注册顺序，结果就变了 ---
B 后执行：发货
A 先执行：扣库存
```

**正确姿势**：观察者应该互相独立、无先后依赖；真有先后关系，就把它们合并成一个观察者，或者引入显式优先级。

---

## 9. 练习题

### 练习 1：温度传感器 + 多个显示器

写一个 `Thermostat`（温度传感器）作为被观察者，`PhoneDisplay` 和 `WallDisplay` 两个观察者，温度一变都更新：

```python
# 答案：经典的"一个主题 + 多个观察者"
import abc


class Display(abc.ABC):
    @abc.abstractmethod
    def show(self, temp: float) -> None:
        pass


class Thermostat:
    """温度传感器：被观察者"""

    def __init__(self):
        self._displays = []

    def attach(self, d: Display):
        self._displays.append(d)

    def set_temp(self, temp: float):
        print(f"温度变化：{temp}℃")
        for d in self._displays:
            d.show(temp)


class PhoneDisplay(Display):
    def show(self, temp):
        print(f"  [手机] 当前室温 {temp}℃")


class WallDisplay(Display):
    def show(self, temp):
        print(f"  [挂墙屏] 室温 {temp}℃，建议开空调")


t = Thermostat()
t.attach(PhoneDisplay())
t.attach(WallDisplay())
t.set_temp(26.0)
t.set_temp(31.5)
```

运行输出：

```
温度变化：26.0℃
  [手机] 当前室温 26.0℃
  [挂墙屏] 室温 26.0℃，建议开空调
温度变化：31.5℃
  [手机] 当前室温 31.5℃
  [挂墙屏] 室温 31.5℃，建议开空调
```

### 练习 2：用"函数观察者"实现任务完成提醒

任务中心完成一个任务时，要同时通知领导和写日志。要求观察者是普通函数：

```python
# 答案：观察者就是函数，主题存回调列表
class TaskCenter:
    """任务中心：任务完成时广播"""

    def __init__(self):
        self._watchers = []

    def watch(self, fn):
        self._watchers.append(fn)

    def complete(self, task_name, cost):
        print(f"任务完成：{task_name}（耗时 {cost} 秒）")
        for fn in self._watchers:
            fn(task_name, cost)


def notify_leader(task, cost):
    print(f"  [领导] {task} 完成，耗时 {cost}s")


def save_log(task, cost):
    print(f"  [日志] 记录 {task} 耗时 {cost}s")


center = TaskCenter()
center.watch(notify_leader)
center.watch(save_log)
center.complete("数据清洗", 12)
```

运行输出：

```
任务完成：数据清洗（耗时 12 秒）
  [领导] 数据清洗 完成，耗时 12s
  [日志] 记录 数据清洗 耗时 12s
```

### 练习 3：用 `weakref` 修复"忘了注销"的泄漏

主题用强引用保存观察者，观察者被删除后仍被主题拽着不放。请用 `weakref` 修复：

```python
# 答案：弱引用保存观察者，对象回收后自动失效
import gc
import weakref


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, o):
        self._observers.append(weakref.ref(o))

    def notify(self, msg):
        alive = []
        for ref in self._observers:
            o = ref()
            if o is not None:
                o.update(msg)
                alive.append(ref)
        self._observers = alive


class Listener:
    def __init__(self, name):
        self.name = name

    def update(self, msg):
        print(f"  [{self.name}] {msg}")


s = Subject()
a = Listener("甲")
b = Listener("乙")
s.attach(a)
s.attach(b)

del a          # 甲被销毁，但忘了注销
gc.collect()

s.notify("你好")
print("剩余观察者：", len(s._observers))
```

运行输出：

```
  [乙] 你好
剩余观察者： 1
```

---

## 10. 小结与口诀

> **口诀：有事广播，订阅者自知；注册注销随心意，互不认识最干净。**

观察者模式是"解耦广播"的利器：**Subject 只管喊，Observer 只管应，两边谁也不认识谁。** 记住三条：

1. **回调要隔离异常**，一个观察者炸了不能连累整条通知链；
2. **忘注销会泄漏**——用 `weakref` 或保证成对注册/注销；
3. Python 里观察者**常常就是函数**，别一上来就写抽象类。

下一章，我们来看结构型家族里的"翻译官"——**适配器模式**：换个插头，接上旧设备。

---

*本章金句：观察者模式是"解耦广播"的艺术——主题只管喊一嗓子，谁在听、听几遍，它一概不知。*
