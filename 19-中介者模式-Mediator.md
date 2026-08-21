# 第 19 章 中介者模式（Mediator）

> **一句话总结**：别互相喊话，都通过中间人。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 行为型 | ★★★☆☆ | ★★☆☆☆ |

---

## 1. 引子：先讲个故事

机场里飞机起飞降落靠什么？靠**塔台**。几十架飞机在天上飞，如果每架都要跟其他所有飞机直接通话："A320 你让一下""B737 你往左偏点"——无线电频道早就吵成一锅粥了。有了塔台，所有飞机只跟塔台说话，塔台统一调度，秩序井然。

程序世界里也有"空中交通管制"：一个对话框里有输入框、列表框，二者互相影响——输入内容要同步到列表。如果组件直接持有彼此的引用，就会缠成一团：

```python
# 引子：没有中介者的界面——两个组件互相直接引用
class InputBox:
    def __init__(self):
        self.text = ""
        self.listbox = None

    def on_type(self, text):
        self.text = text
        self.listbox.add_item(text)


class ListBox:
    def __init__(self):
        self.items = []
        self.input = None

    def add_item(self, text):
        self.items.append(text)
        self.input.text = ""


inp = InputBox()
lst = ListBox()
inp.listbox = lst
lst.input = inp

inp.on_type("买牛奶")
print("列表条目：", lst.items)
print("输入框内容：", repr(inp.text))
```

运行输出：

```
列表条目： ['买牛奶']
输入框内容： ''
```

这才两个组件就互相"私通"了：输入框往列表里塞东西，列表又回头把输入框清空。等输入框、列表框、删除按钮、状态栏全上场，每加一个组件要改其他所有组件——这就是**多对多**的依赖地狱。**中介者模式**就是把这张"蜘蛛网"收拢成"星形结构"：所有组件只跟中介者说话，由它统一协调。

---

## 2. 模式登场

### 定义

> **中介者模式**：用一个中介对象封装一组对象之间的交互，让对象之间不再互相直接引用，而是通过中介者通信。

### 解决的问题

1. **多对多依赖**：N 个对象互相直接引用，关系数是 N×(N-1)/2，改一处动全身；
2. **复用困难**：组件绑得太死，想单独复用其中一个都难；
3. **逻辑分散**：协调规则散落在各个组件里，没人看得清全局。

### 结构

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Colleague A  │     │  Colleague B  │     │  Colleague C  │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │   只和中介者通信    │                     │
       ▼                   ▼                     ▼
┌──────────────────────────────────────────────────────┐
│                      Mediator                          │
│  持有所有同事的引用，负责转发消息、协调行为               │
└──────────────────────────────────────────────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **Mediator（中介者）** | 定义同事间通信的接口 |
| **ConcreteMediator（具体中介者）** | 持有所有同事的引用，实现协调逻辑（塔台、聊天室） |
| **Colleague（同事）** | 参与交互的对象，只认识中介者，不认识其他同事 |
| **客户端** | 创建中介者和同事，把同事注册进中介者 |

---

## 3. Python 实现

### 3.1 经典版：聊天室

聊天室就是最标准的中介者：用户（同事）之间不直接发消息，全部通过聊天室（中介者）转发：

```python
class ChatRoom:
    """中介者：聊天室，负责在用户之间转发消息"""
    def __init__(self):
        self.users = []
    def join(self, user):
        self.users.append(user)
        user.room = self
        for other in self.users:
            if other is not user:
                other.receive("系统", f"{user.name} 加入了群聊")
    def broadcast(self, sender, message):
        for user in self.users:
            if user is not sender:
                user.receive(sender.name, message)


class User:
    """同事：用户不直接找别人说话，都通过聊天室"""
    def __init__(self, name):
        self.name = name
        self.room = None
    def send(self, message):
        print(f"[{self.name} 发言] {message}")
        self.room.broadcast(self, message)
    def receive(self, sender, message):
        print(f"{self.name} 收到来自 {sender} 的消息：{message}")


room = ChatRoom()
alice = User("爱丽丝")
bob = User("鲍勃")
carol = User("卡罗尔")
for u in (alice, bob, carol):
    room.join(u)
alice.send("今晚吃火锅？")
bob.send("走起！")
```

运行输出：

```
爱丽丝 收到来自 系统 的消息：鲍勃 加入了群聊
爱丽丝 收到来自 系统 的消息：卡罗尔 加入了群聊
鲍勃 收到来自 系统 的消息：卡罗尔 加入了群聊
[爱丽丝 发言] 今晚吃火锅？
鲍勃 收到来自 爱丽丝 的消息：今晚吃火锅？
卡罗尔 收到来自 爱丽丝 的消息：今晚吃火锅？
[鲍勃 发言] 走起！
爱丽丝 收到来自 鲍勃 的消息：走起！
卡罗尔 收到来自 鲍勃 的消息：走起！
```

`User` 的世界里只有 `self.room`，没有"认识其他用户"的代码——加用户、改规则，都只动聊天室。

### 3.2 表单联动版：选城市 → 更新区县

下单页最常见的交互：选省 → 市列表跟着变；选市 → 区列表跟着变。三个下拉框互不直接引用，全由 `FormMediator` 协调：

```python
class FormMediator:
    """表单中介者：协调省/市/区三个下拉框联动"""
    def __init__(self):
        self.province = None
        self.city = None
        self.district = None
        self.data = {
            "广东省": {"广州市": ["天河区", "越秀区"], "深圳市": ["南山区", "福田区"]},
            "浙江省": {"杭州市": ["西湖区", "滨江区"], "宁波市": ["海曙区", "鄞州区"]},
        }
    def on_province_changed(self, province):
        cities = list(self.data.get(province, {}).keys())
        self.city.select(cities[0] if cities else None)
        self.on_city_changed(cities[0] if cities else None)
    def on_city_changed(self, city):
        districts = []
        for cities in self.data.values():
            if city in cities:
                districts = cities[city]
                break
        self.district.select(districts[0] if districts else None)


class SelectBox:
    """同事：下拉框，不直接认识其他下拉框"""
    def __init__(self, name, mediator):
        self.name = name
        self.mediator = mediator
    def select(self, value):
        print(f"{self.name} 选中：{value}")
    def user_select(self, value):
        """用户手动选择：通知中介者协调其他框"""
        self.select(value)
        if self.name == "省":
            self.mediator.on_province_changed(value)
        elif self.name == "市":
            self.mediator.on_city_changed(value)


mediator = FormMediator()
province = SelectBox("省", mediator)
city = SelectBox("市", mediator)
district = SelectBox("区", mediator)
mediator.province, mediator.city, mediator.district = province, city, district

province.user_select("广东省")
print("---")
city.user_select("深圳市")
```

运行输出：

```
省 选中：广东省
市 选中：广州市
区 选中：天河区
---
市 选中：深圳市
区 选中：南山区
```

三个下拉框彼此零依赖，联动规则全集中在 `FormMediator`——**同事不认识，规则全在中介者**。

### 3.3 机场塔台：多架飞机排队降落

塔台统一调度，跑道一次只服务一架飞机：

```python
class ControlTower:
    """中介者：机场塔台，统一调度飞机起降"""
    def __init__(self):
        self.planes = []
        self.runway_busy = False
    def register(self, plane):
        self.planes.append(plane)
        plane.tower = self
        print(f"塔台：{plane.name} 已登记")
    def request_landing(self, plane):
        if self.runway_busy:
            print(f"塔台：{plane.name}，跑道繁忙，请在空中盘旋等待")
            return False
        self.runway_busy = True
        print(f"塔台：{plane.name}，跑道已清空，允许降落")
        return True
    def finish_landing(self, plane):
        self.runway_busy = False
        print(f"塔台：{plane.name} 已落地，跑道空闲")


class Plane:
    """同事：飞机不直接跟其他飞机通话，都找塔台"""
    def __init__(self, name):
        self.name = name
        self.tower = None
    def land(self):
        print(f"{self.name}：请求降落")
        if self.tower.request_landing(self):
            self.tower.finish_landing(self)


tower = ControlTower()
p1 = Plane("A320")
p2 = Plane("B737")
tower.register(p1)
tower.register(p2)
p1.land()
p2.land()
```

运行输出：

```
塔台：A320 已登记
塔台：B737 已登记
A320：请求降落
塔台：A320，跑道已清空，允许降落
塔台：A320 已落地，跑道空闲
B737：请求降落
塔台：B737，跑道已清空，允许降落
塔台：B737 已落地，跑道空闲
```

---

## 4. Python 特有玩法

### 4.1 事件回调注册表：中介者就是一张"事件 → 回调"表

Python 函数是一等公民，"中介者"常可退化成一张**事件注册表**：内部维护 `{事件名: [回调函数]}`，发布事件时按表分发——这正是第 9 章观察者的"发布-订阅"结构，中介者与观察者天生合体：

```python
class EventMediator:
    """事件注册表式中介者：内部就是一张 {事件名: [回调函数]} 的表"""
    def __init__(self):
        self._handlers = {}
    def on(self, event, handler):
        self._handlers.setdefault(event, []).append(handler)
    def emit(self, event, *args):
        for handler in self._handlers.get(event, []):
            handler(*args)


def refresh_list(data):
    print(f"列表框刷新：{data}")


def update_status(data):
    print(f"状态栏更新：收到 {len(data)} 条数据")


def notify_admin(data):
    print(f"管理员收到通知：{data}")


mediator = EventMediator()
for h in (refresh_list, update_status, notify_admin):
    mediator.on("data_loaded", h)

mediator.emit("data_loaded", ["苹果", "香蕉", "橙子"])
print("---")
mediator.emit("data_loaded", ["只有一条"])
```

运行输出：

```
列表框刷新：['苹果', '香蕉', '橙子']
状态栏更新：收到 3 条数据
管理员收到通知：['苹果', '香蕉', '橙子']
---
列表框刷新：['只有一条']
状态栏更新：收到 1 条数据
管理员收到通知：['只有一条']
```

### 4.2 `weakref` 防止泄漏

中介者持有同事的**强引用**，会让"已经没用"的同事无法被垃圾回收，内存悄悄泄漏。解决思路是用 `weakref`（弱引用）持有订阅者：`self._subscribers.append((weakref.ref(obj), method_name))`；发布事件时 `ref()` 取回对象，取不回来就说明对象已死，直接跳过并顺手清理。这里有个经典坑：**别对"绑定方法"直接弱引用**——`weakref.ref(win.on_click)` 存的绑定方法每次访问都是新对象，弱引用会立刻失效；正确做法是存 `(weakref.ref(对象), 方法名字符串)`，广播时再 `getattr(obj, method_name)()`。tkinter、Qt 等框架的事件系统里，"弱引用订阅"就是防泄漏的标配。

### 4.3 `dataclass` 消息对象

同事之间传递的消息用 `dataclass` 定义最清晰；再加 `frozen=True`，消息发出去就不能被中途篡改：

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    """不可变消息：发出去就不能被篡改"""
    sender: str
    content: str


# 中介者投递消息：frozen 保证消息在传递途中不会被改
def deliver(room, msg):
    print(f"[{room}] {msg.sender} 说：{msg.content}")


deliver("吃货群", Message("爱丽丝", "今晚吃火锅？"))
try:
    Message("爱丽丝", "今晚吃火锅？").content = "被篡改"
except Exception as e:
    print("消息不可变，篡改失败：", e)
```

运行输出：

```
[吃货群] 爱丽丝 说：今晚吃火锅？
消息不可变，篡改失败： cannot assign to field 'content'
```

---

## 5. 真实世界中的它

### Qt 的信号槽机制

Qt 把中介者思想发扬光大：**信号（signal）与槽（slot）**。任何控件可发出信号，任何对象可用 `connect` 声明"我关心这个信号"。发送者不知道接收者是谁，连接关系全部由外部（相当于中介者）管理——你写 `button.clicked.connect(handler)`，就是在说"让中介者把点击事件转达给 handler"。

### tkinter 的 `StringVar` 联动

tkinter 的 `StringVar` 也是迷你中介者：多个控件（输入框、标签、列表）**绑定同一个 `StringVar`**，任何一个修改它，其他控件自动刷新——控件互不引用，全靠这个"值对象"中转。

### asyncio 的消息传递

`asyncio.Queue` 是协程世界里的中介者：生产者和消费者互不认识，一个往队列里放、一个从队列里取，由队列完成消息转交——相比"直接传引用"，天然支持异步解耦，是事件驱动框架最常见的协作方式。

---

## 6. 优缺点与适用场景

### 优点

- **彻底解耦同事**：多对多的蜘蛛网变成多对一的星形结构，同事之间零依赖；
- **逻辑集中、便于扩展**：协调规则集中一处，改规则只改一个类；加同事只注册进中介者（开闭原则）；
- **同事可复用**：组件不再绑定其他组件，单独拎出来就能用。

### 缺点

- **中介者可能膨胀**：交互规则全塞进来，容易变成"上帝对象"（见误区 1）；
- **单点故障**：中介者挂了，整个协作系统瘫痪；
- **间接通信、过度抽象**：消息要绕道转发，直连能一行写完的要写两处；只有两三个对象交互时纯属画蛇添足。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 多个对象交互复杂、互相依赖严重 | 只有两三个对象、交互简单直接 |
| 交互规则经常变化（改一处即可） | 交互逻辑与对象本身强绑定 |
| 想复用个别组件（解耦后随便拎） | 消息有严格的性能要求（绕道有开销） |
| GUI 组件联动、聊天室、游戏房间 | 只需要一个对象通知另一个（观察者就够） |

> **一句话权衡**：交互"乱成一锅粥"时用中介者收拢；交互本来就简单，别硬造"中间商"。

---

## 7. 与其他模式的关系

- **与外观**：方向相反——外观**单向**（对外简化接口，内部对象之间不协调，第 6 章），中介者**双向**（消息经它转发、主动协调各方）。外观是"前台接待"，中介者是"内部调度员"。
- **与观察者**：中介者内部常用观察者实现（4.1 的"事件→回调"表就是发布-订阅）；观察者是一对多"广播"，中介者是对象间"协调"；只是"通知"时，观察者就够了。
- **与责任链**：责任链是"请求沿链条传递，谁接住谁处理"（第 13 章）；中介者是"请求收拢到一点再分发"，两者可结合。
- **与单例**：中介者（聊天室、事件总线）常被实现成单例——全系统一个调度中心，呼应第 1 章。
- **与命令**：中介者可配合命令模式（第 15 章）实现"点按钮 → 生成命令 → 中介者执行"，天然支持撤销、排队。

---

## 8. 常见误区

### 误区 1：中介者变成"上帝对象"

中介者负责"协调"，但**业务逻辑**（校验、存储、通知）不该塞给它——每加一条业务规则就要改一次中介者，违反单一职责原则：

```python
# 反面教材：上帝中介者——什么逻辑都往里塞
class GodMediator:
    """中介者包揽一切：校验、存储、通知、日志……越写越长"""
    def on_login_click(self, username, password):
        if len(username) < 3:
            print("用户名太短")
            return
        if password != "123456":
            print("密码错误")
            return
        self._save_to_db(username)
        self._send_welcome(username)
        self._write_log(username)
    def _save_to_db(self, username):
        print(f"保存 {username} 到数据库")
    def _send_welcome(self, username):
        print(f"给 {username} 发欢迎邮件")
    def _write_log(self, username):
        print(f"记录日志：{username} 登录")


GodMediator().on_login_click("王小明", "123456")
```

运行输出：

```
保存 王小明 到数据库
给 王小明 发欢迎邮件
记录日志：王小明 登录
```

**正确姿势**：中介者只管"转达和协调"，校验、存储、通知交给同事或服务层——别当"什么都干"的居委会大妈。

### 误区 2：与外观模式混淆

两者都"收拢"，但本质不同：外观是**单向简化**——客户端以前调 5 个类的方法，现在只调外观 1 个，但这 5 个类之间**不需要互相通信**；中介者是**双向协调**——同事之间本来就要频繁通信，中介者是"话务总机"。一句话：外观是"前台"，中介者是"调度中心"。

### 误区 3：同事之间偷偷直接引用

中介者的前提是"同事只认识中介者"。若同事偷偷保存了其他同事的引用、私下通信，中介者就形同虚设——消息不被记录、不被审计、规则被绕过：

```python
# 反面教材：同事之间"私通"——绕过中介者直接引用
class User:
    def __init__(self, name, room):
        self.name = name
        self.room = room
        self.secret_friend = None
    def send(self, message):
        self.room.broadcast(self.name, message)
    def send_secret(self, message):
        # 绕过中介者直接私聊——中介者再也管不到这条消息
        self.secret_friend.receive(self.name, message)
    def receive(self, sender, message):
        print(f"{self.name} 收到 {sender}：{message}")


class Room:
    def __init__(self):
        self.users = []
    def join(self, user):
        self.users.append(user)
    def broadcast(self, sender, message):
        for u in self.users:
            if u.name != sender:
                u.receive(sender, message)


room = Room()
a = User("阿伟", room)
b = User("小明", room)
room.join(a)
room.join(b)
a.secret_friend = b
a.send_secret("别告诉别人")
print("问题：这种消息没人记录、没人审计，中介者形同虚设")
```

运行输出：

```
小明 收到 阿伟：别告诉别人
问题：这种消息没人记录、没人审计，中介者形同虚设
```

**纪律**：一旦决定用中介者，同事间通信必须走中介者——"偷偷私聊"会瞬间毁掉整个架构。

---

## 9. 练习题

### 练习 1：给聊天室加"私聊"

请扩展 `ChatRoom` 支持 `whisper` 私聊——**私聊也要走中介者**，由聊天室转发并判断对方是否在线：

```python
class ChatRoom:
    def __init__(self):
        self.users = {}
    def join(self, user):
        self.users[user.name] = user
        user.room = self
    def broadcast(self, sender, message):
        for name, user in self.users.items():
            if name != sender.name:
                user.receive(sender.name, message)
    def whisper(self, sender, target_name, message):
        target = self.users.get(target_name)
        if target:
            target.receive(f"{sender.name}(私聊)", message)
        else:
            print(f"{sender.name}：{target_name} 不在线，消息发送失败")


class User:
    def __init__(self, name):
        self.name = name
        self.room = None
    def send(self, message):
        self.room.broadcast(self, message)
    def whisper(self, target, message):
        self.room.whisper(self, target, message)
    def receive(self, sender, message):
        print(f"{self.name} 收到 {sender}：{message}")


room = ChatRoom()
a = User("爱丽丝")
b = User("鲍勃")
room.join(a)
room.join(b)
a.send("大家好")
a.whisper("鲍勃", "晚上一起吃饭吗？")
a.whisper("查尔斯", "在吗？")
```

运行输出：

```
鲍勃 收到 爱丽丝：大家好
鲍勃 收到 爱丽丝(私聊)：晚上一起吃饭吗？
爱丽丝：查尔斯 不在线，消息发送失败
```

### 练习 2：用事件注册表实现"输入 → 列表 + 状态栏"

用 4.1 的写法实现：输入框每敲一行字，列表新增一条，状态栏显示总条数：

```python
# 练习 2 答案：事件注册表版中介者实现表单联动
class Mediator:
    def __init__(self):
        self._handlers = {}
    def on(self, event, handler):
        self._handlers.setdefault(event, []).append(handler)
    def emit(self, event, *args):
        for h in self._handlers.get(event, []):
            h(*args)


mediator = Mediator()
items = []


def add_to_list(text):
    items.append(text)
    print(f"列表新增：{text}")


def update_status(text):
    print(f"状态栏：当前共 {len(items)} 条")


mediator.on("input", add_to_list)
mediator.on("input", update_status)

for text in ["买牛奶", "交房租", "约牙医"]:
    mediator.emit("input", text)
```

运行输出：

```
列表新增：买牛奶
状态栏：当前共 1 条
列表新增：交房租
状态栏：当前共 2 条
列表新增：约牙医
状态栏：当前共 3 条
```

### 练习 3：塔台排队调度

三架飞机几乎同时请求降落，跑道一次只能服务一架。请让飞机按请求顺序依次降落：

```python
# 练习 3 答案：塔台按请求顺序排队放行，跑道一次只服务一架
class Tower:
    def __init__(self):
        self._queue = []
        self._busy = False
    def register(self, plane):
        plane.tower = self
    def request_landing(self, plane):
        self._queue.append(plane)
        self._serve()
    def _serve(self):
        if self._busy or not self._queue:
            return
        self._busy = True
        plane = self._queue.pop(0)
        print(f"塔台：允许 {plane.name} 降落")
        print(f"{plane.name}：正在降落……")
        print(f"塔台：{plane.name} 已落地，跑道空闲")
        self._busy = False
        self._serve()   # 继续处理下一架


class Plane:
    def __init__(self, name):
        self.name = name
        self.tower = None
    def land(self):
        print(f"{self.name}：请求降落")
        self.tower.request_landing(self)


tower = Tower()
planes = [Plane(n) for n in ("A320", "B737", "C919")]
for p in planes:
    tower.register(p)

for p in planes:
    p.land()
```

运行输出：

```
A320：请求降落
塔台：允许 A320 降落
A320：正在降落……
塔台：A320 已落地，跑道空闲
B737：请求降落
塔台：允许 B737 降落
B737：正在降落……
塔台：B737 已落地，跑道空闲
C919：请求降落
塔台：允许 C919 降落
C919：正在降落……
塔台：C919 已落地，跑道空闲
```

---

## 10. 小结与口诀

> **口诀：多对多，变多对一；都找中间人，谁也不认识谁；协调逻辑集中放，别让中介成上帝。**

中介者的价值在于**把交互的"关系网"变成"星形结构"**：同事零依赖、规则集中、加人只动中介者。它常与观察者合体（事件注册表）、易与外观混淆（外观单向、中介者双向）。

但记住代价：中介者天生会膨胀成"上帝对象"，**只放协调逻辑，别放业务逻辑**；交互简单时，别硬造中间商。下一章，我们来看"随时存档、随时回档"的**备忘录**模式：游戏存档，随时保存，随时读档重来。

---

*本章金句：中介者把"千丝万缕"捋成"众星拱月"——协作的复杂度，由中间人一人承担。*
