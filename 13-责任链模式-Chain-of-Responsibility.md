# 第 13 章 责任链模式（Chain of Responsibility）

> **一句话总结**：层层审批，传到为止；谁接得住谁处理。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 行为型 | ★★★☆☆ | ★★★★☆ |

---

## 1. 引子：先讲个故事

公司报销流程：300 元组长批，3000 元经理批，5 万总监批，再往上董事会。你提交一张 3 万的发票，它不会直接飞到董事会桌上，而是从组长开始一路"传"上去，直到有人能拍板。**每一级都看一眼金额：自己能批就批，不能批就传给上一级。**

如果把这个流程写成代码，新手第一反应是 if-elif 一路写下去：

```python
# 引子：报销审批用 if-elif 硬编码，加一级审批就要改函数
def approve(amount):
    if amount <= 500:
        return "组长审批通过"
    elif amount <= 5000:
        return "经理审批通过"
    elif amount <= 50000:
        return "总监审批通过"
    else:
        return "需要董事会审批"

print(approve(300))
print(approve(3000))
print(approve(30000))
print(approve(300000))
```

运行输出：

```
组长审批通过
经理审批通过
总监审批通过
需要董事会审批
```

问题在哪？审批规则和金额判断**焊死在一个函数里**：明天加个"副总裁"审批级别，要改这个函数；不同部门审批额度不一样，又要改；审批动作不只是返回一句话，还要记录、通知、留痕……函数会越来越臃肿。**责任链模式**把"每一级审批"拆成独立的处理者，手拉手串成链，请求从链头开始传递，谁接得住谁处理。

---

## 2. 模式登场

### 定义

> **责任链模式**：将请求的发送者和接收者解耦，让多个对象都有机会处理请求，把这些对象连成一条链，并沿着链传递请求，直到有对象处理它为止。

### 解决的问题

1. **请求的处理者不确定**：运行时才知道谁该处理（金额多少、日志级别多少）；
2. **处理者可以动态组合**：加一级审批、换一个过滤器，不用改业务代码（**开闭原则**）；
3. **发送者与处理者解耦**：提交报销的人不需要知道审批链有多长。

### 结构

```
┌─────────────────────────────┐
│        Handler（处理者）       │
├─────────────────────────────┤
│ - next: Handler             │  ← 后继引用：下一个处理者
├─────────────────────────────┤
│ + set_next(h): Handler      │  ← 把处理者串起来
│ + handle(request)           │  ← 能处理就处理，不能就传给 next
└──────────────┬──────────────┘
               │ 后继
               ▼
┌─────────────────────────────┐
│   ConcreteHandler（具体处理者） │
├─────────────────────────────┤
│ + handle(request)           │  ← 多个具体处理者手拉手成链
└─────────────────────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **处理者 Handler** | 定义处理接口，并持有"下一个处理者"的引用 |
| **具体处理者 ConcreteHandler** | 判断自己能不能处理：能则处理，不能则传给后继 |
| **客户端 Client** | 把处理者串成链，把请求丢给链头，不关心谁最终处理 |

### 两种传递方式

- **遇能处理者即停**：审批链、异常捕获——谁接得住谁处理，处理完就停，不再往下传；
- **全部经过**：过滤链、中间件——每个节点都处理一遍，再传给下一个（处理可以修改请求，也可以提前短路）。

---

## 3. Python 实现

### 3.1 经典版：手拉手构建审批链（遇能处理者即停）

每个处理者都持有一个后继引用，处理不了就 `super().handle()` 往下传：

```python
class Handler:
    """责任链节点：处理不了就传给下一个"""

    def __init__(self):
        self._next = None

    def set_next(self, handler):
        """把下一个处理者接在自己后面（返回它以便继续链式）"""
        self._next = handler
        return handler

    def handle(self, amount):
        if self._next:
            return self._next.handle(amount)
        return "无人能批，需要董事会"

class TeamLeader(Handler):
    """组长：500 以内自己批"""

    def handle(self, amount):
        if amount <= 500:
            return f"组长批了 {amount} 元"
        return super().handle(amount)

class Manager(Handler):
    """经理：5000 以内自己批"""

    def handle(self, amount):
        if amount <= 5000:
            return f"经理批了 {amount} 元"
        return super().handle(amount)

class Director(Handler):
    """总监：50000 以内自己批"""

    def handle(self, amount):
        if amount <= 50000:
            return f"总监批了 {amount} 元"
        return super().handle(amount)

# 手拉手构建责任链：组长 → 经理 → 总监
leader = TeamLeader()
leader.set_next(Manager()).set_next(Director())

for amount in (300, 3000, 30000, 300000):
    print(f"报销 {amount} 元 → {leader.handle(amount)}")
```

运行输出：

```
报销 300 元 → 组长批了 300 元
报销 3000 元 → 经理批了 3000 元
报销 30000 元 → 总监批了 30000 元
报销 300000 元 → 无人能批，需要董事会
```

现在加一个"副总裁"审批级别？新写一个 `VicePresident` 类，链上多接一环，**其他代码一行不用改**。

### 3.2 全部经过型：评论过滤链（每个节点都处理）

日志过滤、敏感词过滤这类场景正好相反：**每个节点都要处理**，处理完再传给下一个，链尾返回最终结果：

```python
class Filter:
    def __init__(self):
        self._next = None

    def set_next(self, f):
        self._next = f
        return f

    def process(self, text):
        if self._next:
            return self._next.process(text)
        return text

class SensitiveFilter(Filter):
    """敏感词过滤：处理完继续传给下一个"""

    def process(self, text):
        text = text.replace("垃圾", "**").replace("混蛋", "**")
        return super().process(text)

class AdFilter(Filter):
    """广告过滤：含"加微信"就标记"""

    def process(self, text):
        if "加微信" in text:
            text = text + "（疑似广告）"
        return super().process(text)

class LengthFilter(Filter):
    """长度过滤：超过 30 字截断"""

    def process(self, text):
        if len(text) > 30:
            text = text[:30] + "……"
        return super().process(text)

chain = SensitiveFilter()
chain.set_next(AdFilter()).set_next(LengthFilter())

msg1 = "这个混蛋又在发广告，加微信领券"
msg2 = "这是一条很长的正常评论，讲了整整五十个字的故事，从早讲到晚，非常啰嗦，请务必看完哦"

print("原始：", msg1)
print("过滤后：", chain.process(msg1))
print()
print("原始：", msg2)
print("过滤后：", chain.process(msg2))
```

运行输出：

```
原始： 这个混蛋又在发广告，加微信领券
过滤后： 这个**又在发广告，加微信领券（疑似广告）

原始： 这是一条很长的正常评论，讲了整整五十个字的故事，从早讲到晚，非常啰嗦，请务必看完哦
过滤后： 这是一条很长的正常评论，讲了整整五十个字的故事，从早讲到晚，……
```

敏感词被替换、广告被标记、超长被截断——三道过滤器依次经过，互不干扰。

### 3.3 简化版：用列表构建责任链

"手拉手"适合处理者逻辑差异大的场景；如果每个处理者只是"判断+返回"，一个**列表 + 循环**就能表达同样的链，代码更短：

```python
class Handler:
    """一个很薄的处理者：只有名字和上限"""

    def __init__(self, name, limit):
        self.name = name
        self.limit = limit

    def can_handle(self, amount):
        return amount <= self.limit

# 用列表构建责任链
handlers = [
    Handler("组长", 500),
    Handler("经理", 5000),
    Handler("总监", 50000),
]

def handle(amount):
    for h in handlers:                 # 从头到尾遍历，找第一个能处理的
        if h.can_handle(amount):
            return f"{h.name}批了 {amount} 元"
    return "无人能批，需要董事会"

for amount in (300, 3000, 30000, 300000):
    print(f"报销 {amount} 元 → {handle(amount)}")
```

运行输出：

```
报销 300 元 → 组长批了 300 元
报销 3000 元 → 经理批了 3000 元
报销 30000 元 → 总监批了 30000 元
报销 300000 元 → 无人能批，需要董事会
```

列表版的好处：加一级审批 = 往列表里加一个元素；调整顺序 = 挪一下位置。它和手拉手版在概念上完全等价——**链的本质是"有序的一组候选者"**。

---

## 4. Python 特有玩法

### 4.1 用"列表 + 循环"模拟中间件（Web 中间件的本质）

Web 框架的中间件就是责任链：请求依次穿过每个中间件（日志、鉴权、路由……），每个中间件要么处理掉，要么放行给下一个。用"列表 + 循环"就能把这条链看得明明白白：

```python
# 中间件的本质：一个"处理函数"的列表，请求依次穿过
def log_middleware(request):
    print(f"[日志] 收到请求：{request.get('path')}")
    return None                  # 放行：返回 None 表示继续下一个

def auth_middleware(request):
    if not request.get("user"):
        return "401 未登录"      # 拦截：直接返回响应
    return None                  # 放行

def route_middleware(request):
    if request.get("path") == "/":
        return "首页"
    return None

def final_handler(request):
    return f"404：{request.get('path')} 不存在"

middlewares = [log_middleware, auth_middleware, route_middleware]   # 责任链 = 有序列表

def handle_request(request):
    for mw in middlewares:       # 列表 + 循环：请求依次穿过
        response = mw(request)
        if response is not None:
            return response      # 有中间件拦截了
    return final_handler(request)  # 全部放行 → 兜底处理

print(handle_request({"path": "/", "user": "小明"}))
print(handle_request({"path": "/admin", "user": None}))
print(handle_request({"path": "/unknown", "user": "小明"}))
```

运行输出：

```
[日志] 收到请求：/
首页
[日志] 收到请求：/admin
401 未登录
[日志] 收到请求：/unknown
404：/unknown 不存在
```

注意 `auth_middleware` 里的"短路"：没登录直接返回 401，不再往下传——这就是中间件能"拦截请求"的原理。

### 4.2 装饰器链：Python 原生的"责任链"

装饰器的嵌套本身就是一条链：越靠上的装饰器越"外层"，请求从外到内穿过每个装饰器，再返回时从内到外。它天然适合"全部经过"型链条：

```python
def sensitive(func):
    """装饰器 1：敏感词过滤"""
    def wrapper(text):
        text = text.replace("垃圾", "**")
        return func(text)
    return wrapper

def ad_filter(func):
    """装饰器 2：广告标记"""
    def wrapper(text):
        if "加微信" in text:
            text += "（疑似广告）"
        return func(text)
    return wrapper

@sensitive
@ad_filter
def echo(text):
    return text

print(echo("这个垃圾又在加微信卖课"))
```

运行输出：

```
这个**又在加微信卖课（疑似广告）
```

`sensitive` 在最外层先执行，然后是 `ad_filter`，最后才是 `echo` 本体——和 3.2 的过滤链是同一个套路，只是语法糖帮你把链串好了。

---

## 5. 真实世界中的它

### 标准库：`logging` 的 logger 层级与传播

`logging` 是责任链的隐藏大户：logger 按名字分层（`app` → `app.service` → `app.service.db`），**子 logger 不配 handler 时，日志会沿着层级向上"冒泡"，直到某个父级 logger 的 handler 接住它**——这就是一条责任链：

```python
import logging
import sys

# 根 logger：所有 logger 的"兜底"
root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(name)s -> %(message)s"))
root.addHandler(handler)

# 子 logger：不配 handler，日志会"冒泡"到父 logger 的 handler
child = logging.getLogger("app.service")
child.info("子 logger 的日志，父 logger 帮忙输出")

# 孙子 logger：继续向上冒泡
grand = logging.getLogger("app.service.db")
grand.warning("孙子 logger 的警告也冒泡了")
```

运行输出：

```
app.service -> 子 logger 的日志，父 logger 帮忙输出
app.service.db -> 孙子 logger 的警告也冒泡了
```

`child` 自己没有任何 handler，但日志照样输出了——因为链上传到根 logger 的 handler 接住了。这也是为什么你只在入口配一次 `basicConfig`，全项目的日志就都能打印。

### 框架：Django 中间件

Django 的中间件是教科书级责任链：`MIDDLEWARE` 配置列表里每个中间件实现 `__call__(request, get_response)`，`get_response` 就是"链上下一个节点"。请求从列表头穿到列表尾，响应再从尾穿回头——你可以在任意一环拦截（返回响应不调用 `get_response`）或加工（修改 request/response）。加一个中间件 = 配置列表加一行，业务代码零改动。

### 标准：WSGI 中间件

WSGI（Python Web 的底层接口标准）的中间件同样是责任链：`app(environ, start_response)` 一层包一层，最外层中间件把请求转给内层应用。Flask、Django 的所有扩展（压缩、会话、安全头）本质上都是这条链上的环节。

---

## 6. 优缺点与适用场景

### 优点

- **解耦**：发送者不知道也不关心谁处理请求，只认链头；
- **灵活**：加处理者、调顺序、改链长，都不动业务代码（**开闭原则**）；
- **职责单一**：每个处理者只关心自己那一档（**单一职责原则**）；
- **可控**：可以动态决定"这次请求要不要经过某一环"。

### 缺点

- **调试困难**：请求在链上"漂流"，出问题时不知道卡在哪一环；
- **性能**：链很长时，每个请求都要穿过多层判断；
- **易出错**：忘了传给下一个 → 请求"消失"；顺序搭错 → 结果不对；
- **可能过度设计**：3 个固定分支用 if-elif 更直白。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 处理者数量/组合可能变化（审批流、过滤链） | 分支固定且很少（两三个 if 就够） |
| 请求的接收者事先不确定 | 每个请求都必须由特定对象处理 |
| 需要"短路"或"中途拦截"（中间件、权限链） | 性能极度敏感、链会非常长 |

---

## 7. 与其他模式的关系

- **责任链 vs 命令**：命令模式把"动作"封装成对象（小票），责任链把"动作"在链上**传递**（审批单传下去）；
- **责任链 vs 观察者**：观察者是**一对多广播**（发布者通知所有订阅者），责任链是**一对一传递**（请求只沿着链走，只有一个处理者接住）；
- **责任链 vs 装饰器**：装饰器是**固定的静态链**（写代码时就确定了嵌套顺序），责任链是**动态的链**（运行时可以加节点、改顺序）；
- **责任链 + 组合**：链的每个节点内部还可以是子树，形成更复杂的处理结构。

---

## 8. 常见误区

### 误区 1：忘了传递，请求"消失"（没有兜底）

链上每个节点处理不了时都必须 `super().handle()` 传给下一个；链尾还应该有个**兜底节点**，否则请求会静默消失：

```python
class Handler:
    def __init__(self):
        self._next = None

    def set_next(self, h):
        self._next = h
        return h

    def handle(self, amount):
        if self._next:
            return self._next.handle(amount)
        return None   # 兜底：无人处理返回 None

class Leader(Handler):
    def handle(self, amount):
        if amount <= 500:
            return "组长批了"
        return super().handle(amount)

class Manager(Handler):
    def handle(self, amount):
        if amount <= 5000:
            return "经理批了"
        return super().handle(amount)

# 反面教材：忘了加兜底节点，超大金额直接"消失"
chain = Leader()
chain.set_next(Manager())

result = chain.handle(99999)
if result is None:
    print("危险：99999 元的报销没有任何人处理，静默消失了！")
else:
    print(result)
```

运行输出：

```
危险：99999 元的报销没有任何人处理，静默消失了！
```

线上环境里"请求消失"比"报错"可怕得多——报错至少有人看见。**责任链的链尾永远要有一个兜底**（拒绝、默认值、或者明确抛异常）。

### 误区 2：链过长，难调试

一条链二十个节点，请求从哪一环开始"变质"很难定位。对策：给每个节点加日志（或调试模式下打印经过的节点），并控制链的长度。**链是给"变化"用的，不是给"凑数"用的**——固定不变的处理步骤直接写成一个函数，别拆成链。

### 误区 3：处理顺序依赖

"全部经过"型链条里，节点顺序可能改变结果——先签名再截断和先截断再签名，结果完全不同：

```python
def add_signature(text):
    return text + " —— 来自系统"

def truncate(text, n=10):
    return text[:n]

msg = "这是一条很长很长的消息内容"
print("A：", truncate(add_signature(msg)))   # 先签名再截断：签名被截掉
print("B：", add_signature(truncate(msg)))   # 先截断再签名：签名保留
```

运行输出：

```
A： 这是一条很长很长的消
B： 这是一条很长很长的消 —— 来自系统
```

所以链条的顺序必须**显式管理**（配置列表、文档注明），并写测试锁定顺序，防止有人"顺手"调换。

### 误区 4：把责任链当万能，简单 if-elif 就够时硬上链

三个固定分支、处理者永远不会变——那就老老实实写 if-elif，责任链只会增加阅读负担：

```python
# 就 3 种固定情况，if-elif 最直白，别上责任链
def grade(score):
    if score >= 90:
        return "优秀"
    elif score >= 60:
        return "及格"
    return "不及格"

for s in (95, 70, 40):
    print(f"{s} 分 → {grade(s)}")
```

运行输出：

```
95 分 → 优秀
70 分 → 及格
40 分 → 不及格
```

判断标准：**处理者会不会变、请求会不会由不同的人处理**。会变 → 责任链；永不变 → if-elif。

---

## 9. 练习题

### 练习 1：写一个客服工单转接链

工单按难度升级：一线客服（难度 ≤2）→ 组长（≤4）→ 经理（≤6），都接不住就升级到最高层。用责任链实现：

```python
# 答案：经典责任链
class SupportHandler:
    def __init__(self, name, max_difficulty):
        self.name = name
        self.max_difficulty = max_difficulty
        self._next = None

    def set_next(self, h):
        self._next = h
        return h

    def handle(self, ticket):
        if ticket <= self.max_difficulty:
            return f"{self.name}解决了难度 {ticket} 的工单"
        if self._next:
            return self._next.handle(ticket)
        return "工单升级到最高层处理"

chain = SupportHandler("一线客服", 2)
chain.set_next(SupportHandler("组长", 4)).set_next(SupportHandler("经理", 6))

for difficulty in (1, 3, 5, 9):
    print(chain.handle(difficulty))
```

运行输出：

```
一线客服解决了难度 1 的工单
组长解决了难度 3 的工单
经理解决了难度 5 的工单
工单升级到最高层处理
```

### 练习 2：用"列表 + 循环"实现用户名校验链

依次做长度校验、黑名单校验、格式校验，第一个报错就返回错误信息：

```python
# 答案：列表 + 循环（校验链）
def check_length(text):
    if len(text) < 4:
        return "太短，至少 4 个字符"
    return None

def check_blacklist(text):
    if text in {"admin", "root"}:
        return "该用户名被禁止"
    return None

def check_format(text):
    if not text.isalnum():
        return "只能包含字母和数字"
    return None

checks = [check_length, check_blacklist, check_format]

def validate(username):
    for check in checks:
        error = check(username)
        if error:
            return f"用户名 {username!r}：{error}"
    return f"用户名 {username!r} 校验通过"

for name in ("ab", "admin", "hello!", "python123"):
    print(validate(name))
```

运行输出：

```
用户名 'ab'：太短，至少 4 个字符
用户名 'admin'：该用户名被禁止
用户名 'hello!'：只能包含字母和数字
用户名 'python123' 校验通过
```

### 练习 3：给权限链加上兜底

下面的链没有兜底，合法请求通过后返回 `None`，请加一个兜底节点修复：

```python
# 答案：链尾加兜底放行节点
class Node:
    def __init__(self, name):
        self.name = name
        self._next = None

    def set_next(self, n):
        self._next = n
        return n

    def handle(self, req):
        if self._next:
            return self._next.handle(req)
        return None

class AuthNode(Node):
    def handle(self, req):
        if not req.get("token"):
            return "拒绝访问：未登录"
        return super().handle(req)

class RateNode(Node):
    def handle(self, req):
        if req.get("path") == "/api/vip":
            return "拒绝访问：需要会员"
        return super().handle(req)

class FallbackNode(Node):
    """兜底：走到这里说明全部检查通过"""

    def handle(self, req):
        return "放行：请求已通过全部检查"

chain = AuthNode("登录检查")
chain.set_next(RateNode("限流检查")).set_next(FallbackNode("兜底放行"))

print(chain.handle({"path": "/api/vip", "token": "abc"}))
print(chain.handle({"path": "/api/free", "token": "abc"}))
print(chain.handle({"path": "/api/free"}))
```

运行输出：

```
拒绝访问：需要会员
放行：请求已通过全部检查
拒绝访问：未登录
```

---

## 10. 小结与口诀

> **口诀：层层审批传到为止，谁接得住谁处理；全经型要挨个过，链尾兜底别忘记。**

责任链模式把"一堆 if-elif"拆成"一串处理者"：请求从链头开始传递，要么被接住，要么穿过所有节点。记住三条：

1. 两种传递方式：**遇能处理者即停**（审批）vs **全部经过**（过滤/中间件），别混用；
2. 链尾**必须有兜底**，否则请求会静默消失；
3. 处理者会变才上链，固定分支用 if-elif 更香。

下一章，我们进入创建型模式的"全家桶"——**抽象工厂**：一套产品，成套生产，换就换一整套。

---

*本章金句：责任链是"接力棒"的艺术——每个人只负责自己该管的一段，管不了就交给下一位。*
