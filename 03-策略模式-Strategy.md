# 第 3 章 策略模式（Strategy）

> **一句话总结**：算法可插拔，运行时换。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 行为型 | ★★☆☆☆ | ★★★★★ |

---

## 1. 引子：先讲个故事

在外卖 App 下单，结账时你要选配送方式：普通快递三天到、同城急送一小时到、到店自提免运费。**同一个订单，换一种配送方式，整套"怎么送"的逻辑就全换了**——但下单流程本身一点不用变。出行也一样：同样从家到公司，公交、打车、骑车是三种完全不同的"到达算法"，你的目的地从来不变。

程序里最典型的"换算法"场景就是电商折扣。普通用户不打折、VIP 八折、SVIP 七折、新人九折——如果这些规则全堆在结账函数里，你会写出一段越来越长的 if-elif：

```python
# 引子：没有策略的世界——折扣逻辑全堆在结账函数里
def checkout(price: float, user_type: str) -> float:
    """结账：按用户类型算折扣"""
    if user_type == "vip":
        return price * 0.8
    elif user_type == "svip":
        return price * 0.7
    elif user_type == "new_user":
        return price * 0.9
    else:
        return price


print("普通用户：", checkout(100, "normal"))
print("VIP 用户：", checkout(100, "vip"))
print("SVIP 用户：", checkout(100, "svip"))
```

运行输出：

```
普通用户： 100
VIP 用户： 80.0
SVIP 用户： 70.0
```

这段代码的问题：**结账函数既管"流程"（收钱、算账、出单），又管"算法"（怎么打折）**。双十一要加"全场五折"，你得回来改 `checkout`；万一打折规则算错了，整个结账流程都要跟着排查。折扣规则越来越多，`checkout` 就越来越像一团乱麻。

**策略模式**就是把"算法"从"流程"里拆出来：每种算法一个独立单元，流程只负责"调用当前选中的算法"。想换算法？换一个单元就行，流程一行不改。

---

## 2. 模式登场

### 定义

> **策略模式（Strategy）**：定义一族算法，把每个算法封装成独立的"策略"，并使它们可以互相替换。上下文（Context）在运行时选择用哪个策略，算法的变化不影响使用算法的客户端。

### 三要素

| 要素 | 作用 |
|------|------|
| **上下文（Context）** | 持有一个策略对象，把工作委托给它；客户端通过它使用策略 |
| **策略接口（Strategy）** | 定义算法的公共约定（Python 里常常可以省略） |
| **具体策略（ConcreteStrategy）** | 算法的具体实现，一个策略就是"一种算法" |

### 解决的问题

1. **if-elif 地狱**：每种算法一个分支，加算法就要改业务代码；
2. **算法与业务耦合**：结账函数既管流程又管算法，违反单一职责；
3. **难以扩展**：新算法进不来，旧算法改不动。

### 结构

```
┌────────────────────┐           ┌────────────────────┐
│      Context       │   持有    │      Strategy      │
│    （上下文）        │──────────▶│    （策略接口）      │
├────────────────────┤           ├────────────────────┤
│ - strategy         │           │ + execute()        │
│ + set_strategy()   │           └─────────┬──────────┘
│ + do_action()      │                     │ 实现
└────────────────────┘        ┌────────────┼────────────┐
                              ▼            ▼            ▼
                    ┌────────────┐ ┌────────────┐ ┌────────────┐
                    │策略 A       │ │策略 B       │ │策略 C       │
                    └────────────┘ └────────────┘ └────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **上下文（Context）** | 持有策略，调用策略，提供换策略的入口 |
| **策略（Strategy）** | 算法的公共接口（Python 里经常就是"鸭子类型"，甚至直接传函数） |
| **具体策略** | 某个算法的实现 |
| **客户端（Client）** | 创建具体策略，设置给上下文 |

---

## 3. Python 实现

### 3.1 经典版：折扣策略（三要素齐全）

先写教科书版——不过 Python 里"策略接口"可有可无（鸭子类型说了算），这里直接上具体策略 + 上下文。注意 `set_strategy`——**运行时换算法**就靠它：

```python
class NormalDiscount:
    def discount(self, price: float) -> float:
        return price


class VipDiscount:
    def discount(self, price: float) -> float:
        return price * 0.8


class NewUserDiscount:
    def discount(self, price: float) -> float:
        return price * 0.9


class CheckoutContext:
    """上下文：持有一个策略，负责调用它"""

    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy) -> None:
        """运行时换策略"""
        self._strategy = strategy

    def settle(self, price: float) -> float:
        return self._strategy.discount(price)


cart = CheckoutContext(NormalDiscount())
print("普通用户：", cart.settle(100))

cart.set_strategy(VipDiscount())          # 运行时换算法
print("VIP 用户：", cart.settle(100))

cart.set_strategy(NewUserDiscount())
print("新用户：", cart.settle(100))
```

运行输出：

```
普通用户： 100
VIP 用户： 80.0
新用户： 90.0
```

对比引子的代码：`CheckoutContext` 里**没有任何 if-elif**——加一种折扣，写个新策略类、客户端换一个对象就行，上下文一行不改。这就是**开闭原则**的教科书体现。

### 3.2 运费策略：同一次下单，换计费规则

把"算运费"做成策略——按重量、按距离、包邮，三种算法互不干扰：

```python
class WeightFee:
    def calculate(self, weight: float, distance: float) -> float:
        return weight * 2.0          # 每公斤 2 元


class DistanceFee:
    def calculate(self, weight: float, distance: float) -> float:
        return distance * 0.5        # 每公里 0.5 元


class FreeFee:
    def calculate(self, weight: float, distance: float) -> float:
        return 0.0                   # 包邮


def show_fee(name: str, fee):
    print(f"{name}：{fee.calculate(weight=5, distance=10)} 元")


show_fee("按重量计费", WeightFee())
show_fee("按距离计费", DistanceFee())
show_fee("全场包邮", FreeFee())
```

运行输出：

```
按重量计费：10.0 元
按距离计费：5.0 元
全场包邮：0.0 元
```

`show_fee` 只负责"拿着策略算结果"，具体怎么算它完全不关心——5 公斤、10 公里的同一个包裹，换一种策略，运费就从 10 元变成 5 元、0 元。

### 3.3 排序策略：同一个商品列表，换算法就换顺序

商品排序也适合策略化：价格升序、价格降序、评分优先，每种排序一个策略：

```python
class PriceAsc:
    def sort(self, items: list):
        return sorted(items, key=lambda p: p["price"])


class PriceDesc:
    def sort(self, items: list):
        return sorted(items, key=lambda p: p["price"], reverse=True)


class RatingDesc:
    def sort(self, items: list):
        return sorted(items, key=lambda p: p["rating"], reverse=True)


def show(name: str, items: list):
    print(name + "：", [p["name"] for p in items])


products = [
    {"name": "键盘", "price": 199, "rating": 4.5},
    {"name": "鼠标", "price": 89, "rating": 4.8},
    {"name": "显示器", "price": 1299, "rating": 4.2},
]

show("价格从低到高", PriceAsc().sort(products))
show("价格从高到低", PriceDesc().sort(products))
show("评分从高到低", RatingDesc().sort(products))
```

运行输出：

```
价格从低到高： ['鼠标', '键盘', '显示器']
价格从高到低： ['显示器', '键盘', '鼠标']
评分从高到低： ['鼠标', '键盘', '显示器']
```

---

## 4. Python 特有玩法

### 4.1 函数直接当策略：Python 里"策略"就是一个函数

Java 里实现策略必须写接口、写类；Python 里**一个函数就是策略**——因为函数是一等公民。上下文退化成一行：

```python
def discount_normal(price: float) -> float:
    return price


def discount_vip(price: float) -> float:
    return price * 0.8


def discount_festival(price: float) -> float:
    """双十一全场五折"""
    return price * 0.5


def checkout(price: float, discount_fn) -> float:
    """上下文退化成一行：调用传入的策略函数"""
    return discount_fn(price)


print("普通：", checkout(100, discount_normal))
print("VIP：", checkout(100, discount_vip))
print("双十一：", checkout(100, discount_festival))
print("临时九折：", checkout(100, lambda p: p * 0.9))
```

运行输出：

```
普通： 100
VIP： 80.0
双十一： 50.0
临时九折： 90.0
```

看到最后一行了吗？连 `lambda` 都能当策略——**策略可以是任何可调用对象**，这是 Python 让策略模式"减肥"的最好例子。

### 4.2 字典注册策略表：一个 dict 装下所有算法

算法多了，用字典把"策略名 → 策略函数"注册成一张表，客户端按名字取：

```python
def fee_wechat(amount: float) -> float:
    return amount * 0.006   # 微信费率 0.6%


def fee_alipay(amount: float) -> float:
    return amount * 0.006


def fee_unionpay(amount: float) -> float:
    return amount * 0.008


FEE_STRATEGIES = {
    "wechat": fee_wechat,
    "alipay": fee_alipay,
    "unionpay": fee_unionpay,
}


def pay(amount: float, channel: str) -> float:
    """上下文：查表拿到算法并执行"""
    return amount + FEE_STRATEGIES[channel](amount)


for ch in FEE_STRATEGIES:
    print(f"{ch} 付 1000 元，实付 {pay(1000, ch):.2f}")
```

运行输出：

```
wechat 付 1000 元，实付 1006.00
alipay 付 1000 元，实付 1006.00
unionpay 付 1000 元，实付 1008.00
```

加一种支付渠道 = 写一个费率函数 + 表里加一行。查表比 if-elif 清晰，这正是"注册表式策略"在真实项目里最常见的形态。

### 4.3 对比：`functools.singledispatch`——按类型分派的内建机制

标准库还提供了一个"表亲"：`singledispatch` 按**参数类型**自动选实现。注意它的定位和策略不同——策略是"算法可替换"，分派是"同名单分类型"：

```python
from functools import singledispatch


@singledispatch
def format_data(data):
    return f"未知类型：{type(data).__name__}"


@format_data.register
def _(data: str):
    return f"字符串：{data}"


@format_data.register
def _(data: int):
    return f"整数：{data}"


@format_data.register
def _(data: list):
    return f"列表（{len(data)} 项）：{data}"


print(format_data("你好"))
print(format_data(42))
print(format_data([1, 2, 3]))
print(format_data(3.14))
```

运行输出：

```
字符串：你好
整数：42
列表（3 项）：[1, 2, 3]
未知类型：float
```

---

## 5. 真实世界中的它

### `sorted(key=...)`：内置的"策略注入点"

Python 最常用的排序函数 `sorted` 天生支持策略——**`key` 参数就是策略**：同一个 `sorted`，换一个 `key` 函数就换一种排序规则：

```python
students = [
    {"name": "小明", "score": 88},
    {"name": "小红", "score": 95},
    {"name": "小刚", "score": 72},
]

by_name = sorted(students, key=lambda s: s["name"])
by_score = sorted(students, key=lambda s: s["score"])
by_score_desc = sorted(students, key=lambda s: s["score"], reverse=True)

print("按名字排：", [s["name"] for s in by_name])
print("按分数排：", [s["name"] for s in by_score])
print("按分数倒序：", [s["name"] for s in by_score_desc])
print("最高分：", max(students, key=lambda s: s["score"])["name"])
print("最低分：", min(students, key=lambda s: s["score"])["name"])
```

运行输出：

```
按名字排： ['小刚', '小明', '小红']
按分数排： ['小刚', '小明', '小红']
按分数倒序： ['小红', '小明', '小刚']
最高分： 小红
最低分： 小刚
```

`max` / `min` 的 `key` 参数同理——**"比较策略"由调用方注入**，排序算法本身一行不改。你在不知不觉中用了十几年策略模式。### Django 的认证后端（文字提及）

Django 的 `AUTHENTICATION_BACKENDS` 就是策略模式：一个后端类列表，每个后端实现"如何验证用户"。换认证方式（数据库、LDAP、第三方登录）不用改框架核心——**往列表里加一个类就行**。框架的"认证流程"是上下文，每个后端是一个策略。

### `logging` 的 Handler（文字提及）

`logging` 里 `StreamHandler`、`FileHandler`、`RotatingFileHandler` 各是一种"日志输出策略"——`addHandler(...)` 就是在运行时给日志器换输出算法。

---

## 6. 优缺点与适用场景

### 优点

- **开闭原则的教科书体现**：加算法不用改上下文和客户端；
- **消灭 if-elif 地狱**：分支被"查表/换对象"取代；
- **算法独立**：每种算法可单独测试、单独复用、单独替换；
- **运行时切换**：`set_strategy` 让算法可以在程序运行中更换。

### 缺点

- **类数量增加**：每个算法一个类/函数，小项目会觉得"杀鸡用牛刀"（Python 用函数当策略可以缓解）；
- **客户端要知道有哪些策略**：选择权交给了客户端，客户端得先认识所有策略；
- **策略之间共享状态麻烦**：策略应尽量无状态，否则要小心管理。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 同一行为有多个算法/规则 | 只有一两个分支（过度设计） |
| 算法需要运行时切换 | 算法从不更换、写死就行的场景 |
| 想消除大段 if-elif | 策略选择逻辑复杂到需要另一个模式来管理 |
| 同系列规则经常新增（促销、费率、校验） | 业务代码本身就很简单，加一层反而绕 |

---

## 7. 与其他模式的关系

- **策略 vs 状态**：状态是"行为随**内部状态**自动切换"（订单自动从已支付变已发货），策略是"客户端**主动**换算法"——状态"身不由己"，策略"我选择"。
- **策略 vs 模板方法**：模板方法用**继承**固定骨架、子类填步骤（第 8 章）；策略用**组合**整体换算法——"组合优于继承"的体现。
- **策略 vs 命令**：命令把"请求"封装成对象，可排队、可撤销（第 15 章）；策略封装的是"算法"。
- **策略 + 简单工厂**：经典搭档——工厂负责创建策略对象，客户端不用自己 new 策略（第 2 章）。

---

## 8. 常见误区

### 误区 1：把策略当成状态模式

很多人分不清两者。看代码：状态模式里，**对象自己切换自己的状态**，客户端只是触发；策略模式里，**客户端负责换策略**：

```python
# 误区 1：策略 ≠ 状态。下面演示状态模式的"自动切换"：
class PaidState:
    def next(self, order):
        order.state = ShippedState()
        return "已支付 → 已发货"


class ShippedState:
    def next(self, order):
        order.state = DoneState()
        return "已发货 → 已完成"


class DoneState:
    def next(self, order):
        return "订单已完成，不能继续流转"


class Order:
    def __init__(self):
        self.state = PaidState()

    def advance(self):
        return self.state.next(self)


order = Order()
for _ in range(3):
    print(order.advance())   # 状态自己变，不用客户端操心
```

运行输出：

```
已支付 → 已发货
已发货 → 已完成
订单已完成，不能继续流转
```

区别在于**谁来换**：状态模式的状态在对象内部流转（`order.state = ...` 发生在状态类自己身上）；策略模式的策略由客户端换（`cart.set_strategy(...)`）。如果你发现"策略"在内部自己跳来跳去，那其实是在写状态模式。

### 误区 2：过度设计——俩分支也上策略

策略模式不是万能药。就两种税率、永不变更，直接 if 反而更清晰：

```python
# 误区 2：过度设计——只有一两个分支也硬上策略模式
def tax(income: float, is_tech: bool) -> float:
    """只有两种税率，直接 if 就够清晰了"""
    rate = 0.10 if is_tech else 0.20
    return income * rate


print("科技公司：", tax(10000, True))
print("普通公司：", tax(10000, False))
print("（等算法种类多了、需要运行时切换时，再升级成策略模式）")
```

运行输出：

```
科技公司： 1000.0
普通公司： 2000.0
（等算法种类多了、需要运行时切换时，再升级成策略模式）
```

判断标准：**算法会不会变多？会不会运行时切换？** 两个都"否"，就别上策略——"提前抽象"和"过度设计"往往只有一线之隔。

### 误区 3：把"选策略"的判断又写回业务代码

有人用了策略模式，却在调用处又写一遍 if-elif 选策略——if-elif 只是换了个地方，一点没少：

```python
# 误区 3：选择策略的判断又写回业务代码——if-elif 只是搬了家
def settle_bad(price: float, user_type: str) -> float:
    if user_type == "vip":
        return price * 0.8
    elif user_type == "new":
        return price * 0.9
    return price


# 正确姿势：策略表收拢选择逻辑，业务代码只认策略名
STRATEGIES = {
    "vip": lambda p: p * 0.8,
    "new": lambda p: p * 0.9,
    "normal": lambda p: p,
}


def settle(price: float, user_type: str) -> float:
    return STRATEGIES[user_type](price)


print("坏味道：", settle_bad(100, "vip"))
print("正确姿势：", settle(100, "vip"))
```

运行输出：

```
坏味道： 80.0
正确姿势： 80.0
```

策略模式要消灭的是"散落的 if-elif"——用注册表（4.2）或工厂（第 2 章）把"选哪个策略"收拢到一处，而不是换个地方继续堆分支。

---

## 9. 练习题

### 练习 1：用函数实现三种"问候策略"

写三个问候函数（中文/英文/颜文字），再写一个 `greet` 上下文调用它们：

```python
def greet_cn(name: str) -> str:
    return f"你好，{name}！"


def greet_en(name: str) -> str:
    return f"Hello, {name}!"


def greet_fun(name: str) -> str:
    return f"嗨嗨～{name}～(*´▽`*)"


def greet(name: str, strategy) -> str:
    """上下文：调用传入的策略"""
    return strategy(name)


print(greet("小明", greet_cn))
print(greet("小明", greet_en))
print(greet("小明", greet_fun))
```

运行输出：

```
你好，小明！
Hello, 小明!
嗨嗨～小明～(*´▽`*)
```

### 练习 2：补全一个能换策略的 `Sorter`

让 `Sorter` 支持运行时切换排序策略（升序/降序）：

```python
class Sorter:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy(data)


def asc(data):
    return sorted(data)


def desc(data):
    return sorted(data, reverse=True)

sorter = Sorter(asc)
print("升序：", sorter.sort([3, 1, 2]))
sorter.set_strategy(desc)
print("降序：", sorter.sort([3, 1, 2]))
```

运行输出：

```
升序： [1, 2, 3]
降序： [3, 2, 1]
```

### 练习 3：用"字典注册策略表"实现会员积分

普通日 1 元 1 分、双倍积分日 2 分、生日 3 分，用一个字典装下三种规则：

```python
def points_normal(amount: float) -> int:
    return int(amount)          # 1 元 1 分


def points_double(amount: float) -> int:
    return int(amount) * 2      # 双倍积分日


def points_birthday(amount: float) -> int:
    return int(amount) * 3      # 生日三倍


POINTS_RULES = {
    "normal": points_normal,
    "double": points_double,
    "birthday": points_birthday,
}


def earn_points(amount: float, rule: str) -> int:
    return POINTS_RULES[rule](amount)


print("普通日购物 100 元：", earn_points(100, "normal"), "分")
print("双倍日购物 100 元：", earn_points(100, "double"), "分")
print("生日购物 100 元：", earn_points(100, "birthday"), "分")
```

运行输出：

```
普通日购物 100 元： 100 分
双倍日购物 100 元： 200 分
生日购物 100 元： 300 分
```

---

## 10. 小结与口诀

> **口诀：算法可插拔，运行时换；函数即策略，字典当表格。**

策略模式是行为型里最"讲道理"的一个：它把"算法"从"流程"中剥离，让两者各自演化、互不拖累。记住三条：**三要素**——上下文管调用、策略定约定、具体策略管算法；**Python 里策略常常就是函数或 lambda**，别硬写一堆类；算法多了用**注册表**收拢，别让 if-elif 换个地方继续长。

下一章，我们来看一个你天天在用、却可能从没意识到它是模式的东西——**迭代器模式**：Python 早就替你实现了。

---

*本章金句：策略模式解决的不是"怎么写算法"，而是"怎么让算法可以随便换"——流程归流程，算法归算法。*
