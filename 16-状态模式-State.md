# 第 16 章 状态模式（State）

> **一句话总结**：状态变了，行为就变；状态自己管自己的行为。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 行为型 | ★★★☆☆ | ★★★☆☆ |

---

## 1. 引子：先讲个故事

打游戏时，你的角色有三种状态：正常、狂暴、眩晕。同一个"攻击键"，三种状态下按下去，效果完全不同——正常打 10 点血，狂暴打 50 点，眩晕时按键直接没反应。再想想红绿灯 🚦：同一个路口，红灯停、绿灯行、黄灯等一等。**同一个动作（按键、通过路口），因为当前状态不同，行为完全不同。**

程序里最常见的写法是"一个状态字段 + 一堆 if/elif"。状态少的时候还行，状态一多，每个方法里都要挂一长串判断，改一个状态就得翻遍所有方法——这就是**状态机地狱**：

```python
# 引子：没有状态模式的世界——if/elif 状态机地狱
class MediaPlayer:
    def __init__(self):
        self.state = "stopped"      # stopped / playing / paused

    def play(self):
        if self.state == "stopped":
            self.state = "playing"
            print("开始播放")
        elif self.state == "playing":
            print("已经在播放了，忽略")
        elif self.state == "paused":
            self.state = "playing"
            print("从暂停恢复播放")

    def pause(self):
        if self.state == "playing":
            self.state = "paused"
            print("暂停")
        else:
            print("当前状态不能暂停")

    def stop(self):
        if self.state == "playing" or self.state == "paused":
            self.state = "stopped"
            print("停止")
        else:
            print("已经停止了")


player = MediaPlayer()
player.play()
player.pause()
player.play()
player.stop()
player.stop()
```

运行输出：

```
开始播放
暂停
从暂停恢复播放
停止
已经停止了
```

这段代码有三个毛病：

1. **加状态 = 改所有方法**：再加一个"缓冲中"状态，`play`、`pause`、`stop` 每个方法都要加分支；
2. **行为碎片化**："播放中"的行为散落在三个方法里，你想知道"播放中到底能干什么"，得把三个方法拼起来看；
3. **转移规则不透明**：谁允许转到谁，藏在各个 if 里，没法一眼看全。

**状态模式**的思路是：把"每个状态下的行为"集中到一个类里，让**状态自己管自己的行为**——"播放中"该干嘛、能转移到哪，全部由 `PlayingState` 一个类说了算。

---

## 2. 模式登场

### 定义

> **状态模式**：允许对象在其内部状态改变时改变它的行为，看起来就像对象换了一个类。

### 解决的问题

1. **消灭状态机地狱**：把每个状态下的行为封装成独立类，消灭大段 if/elif；
2. **行为随状态内聚**：一个状态的行为集中在一个类里，改状态不改别的；
3. **转移规则清晰**：每个状态知道"自己能转移到哪"。

### 结构

```
        ┌─────────────────────────┐
        │         Context          │
        │ （上下文：播放器/订单/角色） │
        ├─────────────────────────┤
        │ - _state: State         │
        │ + play() / pause()      │
        │ + stop()                │
        │ + set_state(s)          │
        └────────────┬────────────┘
                     │ 持有当前状态，把请求转发给它
                     ▼
        ┌─────────────────────────┐
        │       State（状态接口）    │
        ├─────────────────────────┤
        │ + play(ctx)             │
        │ + pause(ctx)            │
        │ + stop(ctx)             │
        └────────────┬────────────┘
                     │ 实现
        ┌────────────┴────────────┐
        │  StoppedState 等具体状态  │──▶ 每个状态自己定义：
        └─────────────────────────┘    行为 + 转移到哪个状态
```

### 角色

| 角色 | 说明 |
|------|------|
| **Context（上下文）** | 持有当前状态对象，把请求转发给它，并提供换状态的入口 |
| **State（状态接口）** | 声明"该状态下对每个动作的响应" |
| **ConcreteState（具体状态）** | 实现某个状态的行为，并决定"下一个状态"是谁 |

---

## 3. Python 实现

### 3.1 订单状态流转：状态对象里转移

先看最经典的写法——订单的状态机：待支付 → 已支付 → 已发货 → 已完成。这里采用"**状态对象里转移**"的风格：状态方法直接改上下文的 `state`，状态自己决定"下一步是谁"：

```python
class PendingState:
    """待支付：只能支付或取消"""

    def pay(self, order) -> None:
        print("待支付 → 已支付")
        order.state = PaidState()

    def cancel(self, order) -> None:
        print("待支付 → 已取消")
        order.state = CancelledState()


class PaidState:
    """已支付：只能发货"""

    def ship(self, order) -> None:
        print("已支付 → 已发货")
        order.state = ShippedState()


class ShippedState:
    """已发货：只能确认完成"""

    def complete(self, order) -> None:
        print("已发货 → 已完成")
        order.state = DoneState()


class DoneState:
    """已完成：终态，什么都不许做"""

    def pay(self, order) -> None:
        print("订单已完成，不能再支付")

    def ship(self, order) -> None:
        print("订单已完成，不能发货")

    def complete(self, order) -> None:
        print("订单已经完成了")


class CancelledState:
    """已取消：终态"""

    def pay(self, order) -> None:
        print("订单已取消，无法支付")


class Order:
    """上下文：只管转发请求 + 持有当前状态"""

    def __init__(self, order_id: str):
        self.order_id = order_id
        self.state = PendingState()

    def pay(self) -> None:
        self.state.pay(self)

    def ship(self) -> None:
        self.state.ship(self)

    def complete(self) -> None:
        self.state.complete(self)


order = Order("A1001")
order.pay()
order.ship()
order.complete()
order.pay()          # 已完成订单想再支付？状态类直接拒绝
```

运行输出：

```
待支付 → 已支付
已支付 → 已发货
已发货 → 已完成
订单已完成，不能再支付
```

注意体会：`Order` 类里**一个 if 都没有**。加一个"退款中"状态？写一个新类，再在相关状态里加一条转移——老代码基本不动。

### 3.2 播放器：上下文里转移（另一种风格）

也可以换一种风格：状态方法**不碰上下文**，只返回"下一个状态"，由上下文自己切换。两种风格的取舍，代码跑完再说：

```python
class StoppedState:
    def play(self):
        print("开始播放")
        return PlayingState()

    def pause(self):
        print("已经停止了，无法暂停")
        return self

    def stop(self):
        print("已经停止了")
        return self


class PlayingState:
    def play(self):
        print("正在播放中")
        return self

    def pause(self):
        print("暂停")
        return PausedState()

    def stop(self):
        print("停止")
        return StoppedState()


class PausedState:
    def play(self):
        print("恢复播放")
        return PlayingState()

    def pause(self):
        print("已经暂停了")
        return self

    def stop(self):
        print("停止")
        return StoppedState()


class Player:
    """上下文：只负责'换状态'，不负责'怎么换'"""

    def __init__(self):
        self.state = StoppedState()

    def play(self):
        self.state = self.state.play()

    def pause(self):
        self.state = self.state.pause()

    def stop(self):
        self.state = self.state.stop()


player = Player()
player.play()
player.pause()
player.play()
player.stop()
```

运行输出：

```
开始播放
暂停
恢复播放
停止
```

> **两种风格怎么选？**
> - **状态对象里转移**（3.1）：状态掌握完整决策权，职责内聚；但状态需要拿到上下文（`order`）才能改状态，耦合稍重。
> - **上下文里转移**（3.2）：状态不依赖上下文，返回值驱动转移，更好测试；但状态方法里要写 `return self` 表示"不转移"，略啰嗦。
>
> 小项目随便选，大项目建议**全项目统一一种**，别混着来。

### 3.3 游戏角色：同一按键，三种行为

回到开头游戏的例子：正常 / 狂暴 / 眩晕，同一个"攻击键"，行为完全不同；而且状态还会**自己迁移**（怒气攒够了自动狂暴）：

```python
class NormalState:
    """正常：普通攻击，怒气够了自动狂暴"""

    def attack(self, hero) -> None:
        print("普通攻击，伤害 10")
        if hero.rage >= 80:
            hero.state = RageState()
            print("怒气爆发！进入狂暴状态")


class RageState:
    """狂暴：攻击力翻五倍"""

    def attack(self, hero) -> None:
        print("狂暴攻击，伤害 50！")


class DizzyState:
    """眩晕：按键无效"""

    def attack(self, hero) -> None:
        print("角色还在眩晕，攻击键没反应……")


class Hero:
    """上下文：角色"""

    def __init__(self):
        self.rage = 0
        self.state = NormalState()

    def attack(self) -> None:
        self.state.attack(self)

    def gain_rage(self, amount: int) -> None:
        self.rage += amount


hero = Hero()
hero.gain_rage(30)
hero.attack()            # 正常攻击
hero.gain_rage(60)       # 怒气 90 了
hero.attack()            # 这次攻击后触发狂暴
hero.attack()            # 已经是狂暴攻击
hero.state = DizzyState()   # 被 BOSS 打晕
hero.attack()            # 眩晕中，按键无效
```

运行输出：

```
普通攻击，伤害 10
普通攻击，伤害 10
怒气爆发！进入狂暴状态
狂暴攻击，伤害 50！
角色还在眩晕，攻击键没反应……
```

角色从头到尾是同一个对象，只是 `state` 在变——**看起来像换了一个类**，这正是状态模式的定义。

---

## 4. Python 特有玩法

### 4.1 状态表：dict 映射 (状态, 动作) → 下一状态

如果状态很多、转移规则很规整，用"状态表"最清晰——一张字典就是整张状态机图纸，配合 `enum` 定义状态：

```python
from enum import Enum


class Light(Enum):
    RED = "红"
    GREEN = "绿"
    YELLOW = "黄"


# 状态表：(当前状态, 动作) → 下一状态
TRANSITIONS = {
    (Light.RED, "timeout"): Light.GREEN,
    (Light.GREEN, "timeout"): Light.YELLOW,
    (Light.YELLOW, "timeout"): Light.RED,
}


def next_state(current: Light, action: str) -> Light:
    key = (current, action)
    if key not in TRANSITIONS:
        raise ValueError(f"非法转移：{current.name} + {action}")
    return TRANSITIONS[key]


state = Light.RED
for i in range(4):
    print(f"第 {i + 1} 轮：{state.value}灯亮，车辆{'通行' if state is Light.GREEN else '停止'}")
    state = next_state(state, "timeout")
```

运行输出：

```
第 1 轮：红灯亮，车辆停止
第 2 轮：绿灯亮，车辆通行
第 3 轮：黄灯亮，车辆停止
第 4 轮：红灯亮，车辆停止
```

状态表的杀手锏：**全局视角**。想知道"谁能转移到谁"，扫一眼字典就行——这正好治"转移逻辑分散"的病（见常见误区 3）。

### 4.2 dataclass 状态元数据 + 转移表

`dataclass` 适合描述"状态附带的信息"（允许哪些动作、显示什么文案），和状态表搭配起来非常顺手：

```python
from dataclasses import dataclass
from enum import Enum


class OrderStatus(Enum):
    PENDING = "待支付"
    PAID = "已支付"
    SHIPPED = "已发货"
    DONE = "已完成"
    CANCELLED = "已取消"


@dataclass(frozen=True)
class StatusInfo:
    """状态元数据：这个状态下允许哪些动作"""
    label: str
    allowed_actions: tuple


STATUS_INFO = {
    OrderStatus.PENDING: StatusInfo("待支付", ("pay", "cancel")),
    OrderStatus.PAID: StatusInfo("已支付", ("ship",)),
    OrderStatus.SHIPPED: StatusInfo("已发货", ("complete",)),
    OrderStatus.DONE: StatusInfo("已完成", ()),
    OrderStatus.CANCELLED: StatusInfo("已取消", ()),
}

# 状态转移表：(状态, 动作) → 下一状态
TRANSITIONS = {
    (OrderStatus.PENDING, "pay"): OrderStatus.PAID,
    (OrderStatus.PENDING, "cancel"): OrderStatus.CANCELLED,
    (OrderStatus.PAID, "ship"): OrderStatus.SHIPPED,
    (OrderStatus.SHIPPED, "complete"): OrderStatus.DONE,
}


class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.status = OrderStatus.PENDING

    def do(self, action: str) -> None:
        info = STATUS_INFO[self.status]
        if action not in info.allowed_actions:
            raise ValueError(f"订单 {self.order_id} 当前是「{info.label}」，不能执行 {action}")
        self.status = TRANSITIONS[(self.status, action)]
        print(f"订单 {self.order_id} 执行 {action} → {STATUS_INFO[self.status].label}")


order = Order("A2001")
order.do("pay")
order.do("ship")
order.do("complete")
try:
    order.do("pay")        # 已完成订单不能再支付
except ValueError as e:
    print("非法操作被拦截:", e)
```

运行输出：

```
订单 A2001 执行 pay → 已支付
订单 A2001 执行 ship → 已发货
订单 A2001 执行 complete → 已完成
非法操作被拦截: 订单 A2001 当前是「已完成」，不能执行 pay
```

### 4.3 无状态状态对象：全局共享也不串

状态对象**不带实例数据**时（行为只由"我是哪个状态"决定），可以做成模块级单例全局共享——多个上下文用同一批状态对象，谁也不会串（呼应第 1 章的单例）：

```python
class StoppedState:
    def play(self, player) -> None:
        player.state = PLAYING
        print("停止 → 播放")

    def pause(self, player) -> None:
        print("已经停止了，无法暂停")

    def stop(self, player) -> None:
        print("已经停止了")


class PlayingState:
    def play(self, player) -> None:
        print("正在播放中")

    def pause(self, player) -> None:
        player.state = PAUSED
        print("播放 → 暂停")

    def stop(self, player) -> None:
        player.state = STOPPED
        print("播放 → 停止")


class PausedState:
    def play(self, player) -> None:
        player.state = PLAYING
        print("暂停 → 播放")

    def pause(self, player) -> None:
        print("已经暂停了")

    def stop(self, player) -> None:
        player.state = STOPPED
        print("暂停 → 停止")


# 无状态的状态对象：全局共享一份，谁用都不串
STOPPED = StoppedState()
PLAYING = PlayingState()
PAUSED = PausedState()


class Player:
    """上下文：持有当前状态，把请求转发给状态对象"""

    def __init__(self):
        self.state = STOPPED

    def play(self) -> None:
        self.state.play(self)

    def pause(self) -> None:
        self.state.pause(self)

    def stop(self) -> None:
        self.state.stop(self)


p1 = Player()
p2 = Player()          # 两个播放器共享同一批状态对象
p1.play()
p1.pause()
p2.play()              # p2 还是 stopped，直接进入播放
print("p1 状态:", type(p1.state).__name__)
print("p2 状态:", type(p2.state).__name__)
```

运行输出：

```
停止 → 播放
播放 → 暂停
停止 → 播放
p1 状态: PausedState
p2 状态: PlayingState
```

p1 暂停、p2 播放，互不干扰——因为"谁在播放"这个信息存在各自的 `Player`（上下文）里，状态对象只管行为不管数据。

---

## 5. 真实世界中的它

### 标准库：`asyncio.Future` 的内部状态机

`asyncio` 的 `Future`/`Task` 内部就是一台状态机：`PENDING`（等待中）→ `FINISHED`（完成）或 `CANCELLED`（取消）。很多行为（能不能拿结果、会不会抛异常）都取决于当前状态：

```python
import asyncio


async def demo() -> None:
    future = asyncio.Future()
    print("创建后的状态:", future._state)          # PENDING
    future.set_result(42)
    print("set_result 后的状态:", future._state)  # FINISHED
    print("拿到结果:", future.result())

    cancelled = asyncio.Future()
    cancelled.cancel()
    print("取消后的状态:", cancelled._state)       # CANCELLED


asyncio.run(demo())
```

运行输出：

```
创建后的状态: PENDING
set_result 后的状态: FINISHED
拿到结果: 42
取消后的状态: CANCELLED
```

> `_state` 是内部属性（前面带下划线），正常开发不要直接碰它——这里只是用它演示状态机的存在。

### 框架：Django 与状态机

Django 本身**没有内置状态机**，但这是社区最常用的组合拳：用 `enum` 定义状态常量，用 `choices` 字段存数据库，再用 `django-fsm`、`django-transitions` 这类第三方库提供状态转移表（自动校验非法转移、支持状态变更钩子）。原理就是我们 4.2 的状态表——只不过把"查表 + 校验"做成了现成工具。

### 其他：`http.server` 的协议状态

标准库 `http.server` 处理 HTTP 请求时，内部也是按协议状态一步步走的（读请求行 → 读请求头 → 读请求体 → 发响应），每一步的状态决定了下一步做什么、出错怎么收场。凡是"协议解析"类代码，几乎都是隐式的状态机。

---

## 6. 优缺点与适用场景

### 优点

- **消灭 if/elif 地狱**：每个状态的行为独立成类，代码结构清晰；
- **开闭原则友好**：新增状态 = 新增类 + 在相关状态里加转移，旧状态类基本不动；
- **行为内聚**：一个状态的行为集中一处，改"狂暴攻击"只动一个类；
- **转移规则显式**：谁到谁，写在状态类或状态表里，肉眼可查。

### 缺点

- **类数量膨胀**：一个状态一个类，状态多时类很多（可用状态表缓解）；
- **转移逻辑可能分散**：每个状态类各写各的转移，全局视图要靠状态表补；
- **小状态机杀鸡用牛刀**：两三个状态、行为又简单，直接 if 反而更短。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 订单、播放器、工作流等状态多、行为随状态变化大的系统 | 只有两三个状态且行为简单 |
| 状态会持续增加的业务 | 状态之间几乎没有转移逻辑 |
| 同一动作在不同状态下行为差异明显 | 一次性脚本、临时判断 |

---

## 7. 与其他模式的关系

- **与策略**：这是最容易混的一对。**策略不迁移**——角色换武器（剑→弓），角色还是那个角色，只是算法换了；**状态会迁移**——角色从正常变狂暴，是角色自己变了。区别一句话：策略是"换一种做法"，状态是"换一种身份"。代码对比见常见误区 1。
- **与观察者**：状态变化时常常要通知别人——订单状态变了要通知用户、播放器暂停了要更新 UI。状态模式管"怎么变"，观察者管"变了告诉谁"（第 9 章）。
- **与单例**：无状态的状态对象适合做成单例全局共享（见 4.3），省内存、免重复创建。
- **与命令**：编辑器的撤销/重做系统里，命令记录"做了什么"，状态机记录"当前处于什么阶段"，两者经常一起出现（第 15 章）。

---

## 8. 常见误区

### 误区 1：状态模式与策略模式混淆

同一个"角色攻击"场景，两种写法对比一下，区别立刻清楚。先看**策略**：武器是"可替换的算法"，换武器不改变角色本身：

```python
class SwordAttack:
    def attack(self) -> str:
        return "挥剑攻击，伤害 30"


class BowAttack:
    def attack(self) -> str:
        return "拉弓射击，伤害 20"


class Hero:
    def __init__(self, weapon):
        self.weapon = weapon          # 策略：随时可换

    def set_weapon(self, weapon) -> None:
        self.weapon = weapon

    def attack(self) -> str:
        return self.weapon.attack()


hero = Hero(SwordAttack())
print("用剑:", hero.attack())
hero.set_weapon(BowAttack())
print("换弓:", hero.attack())
print("换成弓之后，角色还是原来的角色（状态没变）")
```

运行输出：

```
用剑: 挥剑攻击，伤害 30
换弓: 拉弓射击，伤害 20
换成弓之后，角色还是原来的角色（状态没变）
```

再看**状态**：同样叫"攻击"，行为随状态变，而且状态会自己迁移：

```python
class NormalState:
    def attack(self, hero) -> None:
        print("普通攻击，伤害 10")
        if hero.rage >= 80:
            hero.state = RageState()
            print("怒气爆发！进入狂暴状态")


class RageState:
    def attack(self, hero) -> None:
        print("狂暴攻击，伤害 50！")


class Hero:
    def __init__(self):
        self.rage = 0
        self.state = NormalState()

    def attack(self) -> None:
        self.state.attack(self)

    def gain_rage(self, amount: int) -> None:
        self.rage += amount


hero = Hero()
hero.gain_rage(30)
hero.attack()
hero.gain_rage(60)
hero.attack()        # 这次攻击后怒气 90，触发狂暴
hero.attack()        # 已经是狂暴攻击
print("当前状态:", type(hero.state).__name__)
```

运行输出：

```
普通攻击，伤害 10
普通攻击，伤害 10
怒气爆发！进入狂暴状态
狂暴攻击，伤害 50！
当前状态: RageState
```

**判断口诀**：问自己"换掉这个对象，对象本身变不变？"——不变是策略，变了是状态。

### 误区 2：有状态的状态对象被共享 → 串状态

状态对象如果私藏了数据，还被多个上下文共享，就会互相污染：

```python
# 反面教材：状态对象带着自己的数据，还被全局共享 → 串状态
class PlayingState:
    def __init__(self):
        self.started_at = "未知"      # 状态对象私藏数据

    def play(self, player) -> None:
        self.started_at = f"{player.name} 开始播放的时间"
        print(f"{player.name} 开始播放")

    def describe(self) -> str:
        return self.started_at


PLAYING = PlayingState()      # 全局共享同一个状态对象


class Player:
    def __init__(self, name: str):
        self.name = name
        self.state = PLAYING


p1 = Player("播放器A")
p2 = Player("播放器B")
p1.state.play(p1)
p2.state.play(p2)             # B 覆盖了 A 的记录
print("A 的播放记录被污染:", p1.state.describe())
```

运行输出：

```
播放器A 开始播放
播放器B 开始播放
A 的播放记录被污染: 播放器B 开始播放的时间
```

> 修正两条路：要么状态对象**保持无状态**（数据放上下文，见 4.3）；要么每个上下文**各自 new 状态实例**。共享有数据的状态对象 = 埋雷。

### 误区 3：转移逻辑分散各处，难追踪

状态对象里转移的风格，每个状态类各写各的转移——状态多了，想画一张全局转移图得翻遍所有类。**状态表**是解药：转移规则集中在一张字典里，缺了哪条一目了然：

```python
# 状态表集中管理：缺转移当场报错，不会静默出错
TRANSITIONS = {
    ("待支付", "支付"): "已支付",
    ("已支付", "发货"): "已发货",
    # 忘了写：已支付 → 已完成 这条转移
}


def transit(current: str, action: str) -> str:
    key = (current, action)
    if key not in TRANSITIONS:
        raise ValueError(f"没有定义转移：{current} + {action}")
    return TRANSITIONS[key]


try:
    transit("已支付", "完成")
except ValueError as e:
    print("缺转移被当场抓住:", e)
```

运行输出：

```
缺转移被当场抓住: 没有定义转移：已支付 + 完成
```

---

## 9. 练习题

### 练习 1：状态表版电梯

用 `enum` + 状态表实现电梯：静止 →(按电梯)→ 运行中 →(到达)→ 门开着 →(关门)→ 静止：

```python
# 答案：状态表驱动电梯——(状态, 动作) → 下一状态
from enum import Enum


class ElevatorState(Enum):
    IDLE = "静止"
    MOVING = "运行中"
    DOOR_OPEN = "门开着"


TRANSITIONS = {
    (ElevatorState.IDLE, "press"): ElevatorState.MOVING,
    (ElevatorState.MOVING, "arrive"): ElevatorState.DOOR_OPEN,
    (ElevatorState.DOOR_OPEN, "close"): ElevatorState.IDLE,
    (ElevatorState.DOOR_OPEN, "press"): ElevatorState.MOVING,
}


class Elevator:
    def __init__(self):
        self.state = ElevatorState.IDLE

    def trigger(self, event: str) -> None:
        key = (self.state, event)
        if key not in TRANSITIONS:
            raise ValueError(f"非法事件：{self.state.value} + {event}")
        self.state = TRANSITIONS[key]
        print(f"事件[{event}] → 现在是「{self.state.value}」")


elevator = Elevator()
elevator.trigger("press")
elevator.trigger("arrive")
elevator.trigger("close")
elevator.trigger("press")
```

运行输出：

```
事件[press] → 现在是「运行中」
事件[arrive] → 现在是「门开着」
事件[close] → 现在是「静止」
事件[press] → 现在是「运行中」
```

### 练习 2：状态类版订单（状态对象里转移）

用状态类实现订单流转，要求"已完成"后再支付会被拒绝：

```python
# 答案：每个状态类知道"下一个状态是谁"
class PendingState:
    def pay(self, order) -> None:
        print("待支付 → 已支付")
        order.state = PaidState()

    def cancel(self, order) -> None:
        print("待支付 → 已取消")
        order.state = CancelledState()


class PaidState:
    def ship(self, order) -> None:
        print("已支付 → 已发货")
        order.state = ShippedState()


class ShippedState:
    def complete(self, order) -> None:
        print("已发货 → 已完成")
        order.state = DoneState()


class DoneState:
    def pay(self, order) -> None:
        print("订单已完成，不能再支付")


class CancelledState:
    def pay(self, order) -> None:
        print("订单已取消，无法支付")


class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.state = PendingState()

    def pay(self) -> None:
        self.state.pay(self)

    def ship(self) -> None:
        self.state.ship(self)

    def complete(self) -> None:
        self.state.complete(self)


order = Order("A2002")
order.pay()
order.ship()
order.complete()
order.pay()
```

运行输出：

```
待支付 → 已支付
已支付 → 已发货
已发货 → 已完成
订单已完成，不能再支付
```

### 练习 3：把 if/elif 播放器改成状态模式

用无状态单例状态对象重写引子里的 `MediaPlayer`：

```python
# 答案：状态模式重写播放器（无状态单例状态对象）
class Stopped:
    def play(self, p) -> None:
        p.state = Playing()
        print("停止 → 播放")

    def stop(self, p) -> None:
        print("已经停止了")


class Playing:
    def play(self, p) -> None:
        print("正在播放中")

    def stop(self, p) -> None:
        p.state = Stopped()
        print("播放 → 停止")


class Player:
    def __init__(self):
        self.state = Stopped()

    def play(self) -> None:
        self.state.play(self)

    def stop(self) -> None:
        self.state.stop(self)


p = Player()
p.play()
p.stop()
p.stop()
```

运行输出：

```
停止 → 播放
播放 → 停止
已经停止了
```

---

## 10. 小结与口诀

> **口诀：状态自己管行为，一态一类不打架；状态表里看全局，别让 if 叠成山。**

状态模式把"状态判断"从散落的 if/elif 里捞出来，装进一个个状态类：行为内聚、转移显式、加状态不动老代码。三个记忆点：

1. **状态即行为**：一个状态一个类，行为跟着状态走；
2. **转移两种写法**：状态对象里转移（内聚）或上下文里转移（解耦），全项目统一一种；
3. **无状态优先**：状态对象不带数据，才能放心全局共享。

下一章，我们来看一个专门对付"树形结构"的模式——**组合模式**：树形结构，叶子与容器一视同仁。

---

*本章金句：状态模式说：行为不是写死的代码，而是状态"活"出来的表情。*
