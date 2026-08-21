# 第 6 章 外观模式（Facade）

> **一句话总结**：一个前台，搞定一切；内部多复杂，外面多简单。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 结构型 | ★★☆☆☆ | ★★★★☆ |

---

## 1. 引子：先讲个故事

你走进一家餐厅，对服务员说："一份宫保鸡丁，一碗米饭。"然后刷手机等菜。你完全不知道后厨怎么运转——谁洗菜、谁切鸡丁、谁颠勺、谁装盘，你统统不关心。**服务员就是你和后厨之间的门面**：你把需求告诉他，他把成品端给你，复杂的流程被挡在墙后面。

如果餐厅不设服务员，让你直接进后厨点菜，你得认识每一个厨师，还得记住流程："先找切菜工说一声，再跟掌勺的打个招呼，最后让装盘的小工拿碗……"——菜没点完，你先累趴了。

程序世界里的"后厨"就是那些**各司其职的子系统**：库存、支付、物流。没有门面时，每个调用方都得亲自把整套流程抄一遍：

```python
# 引子：没有外观的世界——下单流程散落在每个调用方里
def buy_online(sku, qty, amount, address):
    """调用方 A：自己要操心"查库存→扣库存→支付→发货"全套流程"""
    print(f"  库存：检查 {sku} x{qty} 是否有货")
    if qty > 10:
        print("库存不足，下单失败")
        return
    print(f"  库存：扣减 {sku} x{qty}")
    order_id = f"ORD-{sku}-{qty}"
    print(f"  支付：{order_id} 收款 {amount} 元")
    print(f"  物流：{order_id} 发往 {address}")
    print("下单成功！")


def buy_in_store(sku, qty, amount, address):
    """调用方 B：同样的流程，再抄一遍——复制粘贴的臭味"""
    print(f"  库存：检查 {sku} x{qty} 是否有货")
    if qty > 10:
        print("库存不足，下单失败")
        return
    print(f"  库存：扣减 {sku} x{qty}")
    order_id = f"ORD-{sku}-{qty}"
    print(f"  支付：{order_id} 收款 {amount} 元")
    print(f"  物流：{order_id} 发往 {address}")
    print("下单成功！")


buy_online("P001", 2, 199.0, "上海市浦东新区")
buy_in_store("P002", 1, 59.0, "北京市朝阳区")
```

运行输出：

```
  库存：检查 P001 x2 是否有货
  库存：扣减 P001 x2
  支付：ORD-P001-2 收款 199.0 元
  物流：ORD-P001-2 发往 上海市浦东新区
下单成功！
  库存：检查 P002 x1 是否有货
  库存：扣减 P002 x1
  支付：ORD-P002-1 收款 59.0 元
  物流：ORD-P002-1 发往 北京市朝阳区
下单成功！
```

痛点在哪儿？**每个调用方都得把这段流程重写一遍**。今天下单要四步，明天加一个"开发票"步骤，所有调用方都得跟着改；更别提哪天库存系统的接口改名，全项目大扫除。

**外观模式**就是来当这个"服务员"的：把后厨（子系统）的复杂性藏起来，对外只露出一个简单的门面。

---

## 2. 模式登场

### 定义

> **外观模式**：为子系统中的一组接口提供一个统一的、更简单的入口。调用方只跟外观打交道，不直接面对各个子系统。

### 解决的问题

1. **调用方太累**：一个业务操作往往要串起多个子系统，调用方被迫知道所有细节；
2. **耦合太紧**：调用方直接依赖每个子系统的类，子系统一改，调用方全崩；
3. **重复代码**：同样的"串流程"代码在多个调用方之间复制粘贴。

### 结构

```
        ┌──────────────────────────────┐
        │          客户端 Client         │
        └──────────────┬───────────────┘
                       │ 只调用一个方法
                       ▼
        ┌──────────────────────────────┐
        │       OrderFacade（外观）       │
        ├──────────────────────────────┤
        │ + place_order()              │  ← 把流程串起来
        └───────┬──────────┬───────────┘
                │          │
                ▼          ▼
       ┌────────────┐ ┌───────────┐ ┌───────────┐
       │  Inventory  │ │  Payment  │ │ Logistics │
       │  库存子系统   │ │  支付子系统 │ │  物流子系统  │
       └────────────┘ └───────────┘ └───────────┘
```

外观和子系统之间是**组合**关系（外观"拥有"子系统），不是继承。

### 角色

| 角色 | 说明 |
|------|------|
| **外观（Facade）** | 知道各子系统的职责和调用顺序，对外提供简单接口 |
| **子系统（Subsystem）** | 各自完成独立的功能，对外观一无所知 |
| **客户端（Client）** | 只依赖外观，不直接触碰子系统 |

> 注意：子系统**不知道外观的存在**——外观是"单相思"，子系统根本不在乎谁来调用它。

---

## 3. Python 实现

### 3.1 经典版：下单系统一条龙

把引子里的三个子系统单独成类，外面包一层 `OrderFacade`，调用方从"抄流程"变成"一句话下单"：

```python
class Inventory:
    """库存子系统"""

    def check(self, sku: str, qty: int) -> bool:
        print(f"  库存：检查 {sku} x{qty}")
        return qty <= 10

    def reduce(self, sku: str, qty: int) -> None:
        print(f"  库存：扣减 {sku} x{qty}")


class Payment:
    """支付子系统"""

    def pay(self, order_id: str, amount: float) -> bool:
        print(f"  支付：订单 {order_id} 收款 {amount} 元")
        return True


class Logistics:
    """物流子系统"""

    def ship(self, order_id: str, address: str) -> None:
        print(f"  物流：订单 {order_id} 发往 {address}")


class OrderFacade:
    """外观：把三个子系统串成一条龙服务"""

    def __init__(self):
        self._inventory = Inventory()
        self._payment = Payment()
        self._logistics = Logistics()

    def place_order(self, sku: str, qty: int, amount: float, address: str) -> str:
        """对外只暴露一个方法：下单"""
        if not self._inventory.check(sku, qty):
            raise ValueError(f"{sku} 库存不足")
        self._inventory.reduce(sku, qty)
        order_id = f"ORD-{sku}-{qty}"
        if not self._payment.pay(order_id, amount):
            raise RuntimeError("支付失败")
        self._logistics.ship(order_id, address)
        return f"下单成功，订单号 {order_id}"


facade = OrderFacade()
print(facade.place_order("P001", 2, 199.0, "上海市浦东新区"))

# 库存不足的情况：外观负责把"流程中断"翻译成清晰的错误
try:
    facade.place_order("P999", 99, 1.0, "火星基地")
except ValueError as e:
    print("下单被拒：", e)
```

运行输出：

```
  库存：检查 P001 x2
  库存：扣减 P001 x2
  支付：订单 ORD-P001-2 收款 199.0 元
  物流：订单 ORD-P001-2 发往 上海市浦东新区
下单成功，订单号 ORD-P001-2
  库存：检查 P999 x99
下单被拒： P999 库存不足
```

对比引子：调用方从"亲自指挥三个子系统、记住四步流程"变成"一句话下单"。以后要加"开发票"步骤，只改 `OrderFacade` 一处，调用方一行不用动——这就是对**开闭原则**的践行：扩展功能时只改外观，不惊动客户端。

> **关键点**：外观里串流程时，把"中途失败"翻译成清晰的异常或返回值，调用方才不会被一堆半成品状态搞懵。

### 3.2 家庭影院：一键观影

再看一个经典场景。家庭影院的设备各有各的脾气：投影仪要开机、要切模式，窗帘要拉上，音响要开、音量要调，灯光要调暗。每次看电影都手动操作五样设备，仪式感会变成负担。上个外观，把"开机仪式"封装成一键：

```python
class Projector:
    """投影仪"""

    def on(self) -> None:
        print("投影仪：开机")

    def set_mode(self, mode: str) -> None:
        print(f"投影仪：切换到{mode}模式")


class Curtain:
    """窗帘"""

    def close(self) -> None:
        print("窗帘：缓缓拉上")

    def open(self) -> None:
        print("窗帘：拉开")


class SoundSystem:
    """音响"""

    def on(self) -> None:
        print("音响：开机")

    def set_volume(self, level: int) -> None:
        print(f"音响：音量调到 {level}")


class Light:
    """灯光"""

    def dim(self, percent: int) -> None:
        print(f"灯光：调暗到 {percent}%")


class HomeTheaterFacade:
    """家庭影院外观：一键观影、一键散场"""

    def __init__(self):
        self._projector = Projector()
        self._curtain = Curtain()
        self._sound = SoundSystem()
        self._light = Light()

    def watch_movie(self, movie: str) -> None:
        """一键观影：调暗灯光 → 拉窗帘 → 开投影 → 开音响"""
        print(f"===== 开始观影《{movie}》 =====")
        self._light.dim(10)
        self._curtain.close()
        self._projector.on()
        self._projector.set_mode("影院")
        self._sound.on()
        self._sound.set_volume(30)

    def end_movie(self) -> None:
        """一键散场：关音响 → 投影待机 → 拉开窗帘 → 开灯"""
        print("===== 观影结束 =====")
        self._sound.set_volume(0)
        self._projector.set_mode("待机")
        self._curtain.open()
        self._light.dim(100)


theater = HomeTheaterFacade()
theater.watch_movie("流浪地球3")
theater.end_movie()
```

运行输出：

```
===== 开始观影《流浪地球3》 =====
灯光：调暗到 10%
窗帘：缓缓拉上
投影仪：开机
投影仪：切换到影院模式
音响：开机
音响：音量调到 30
===== 观影结束 =====
音响：音量调到 0
投影仪：切换到待机模式
窗帘：拉开
灯光：调暗到 100%
```

"开始观影"和"结束观影"各是一条命令，中间的设备协调全被外观吃掉了。家里来客人，你不用现场教学"先按这个再按那个"，直接说一句"看个电影"就行。

### 3.3 外观不锁死"高级用户"

外观是"方便之门"，**不是"唯一的门"**。子系统仍然对外可见、可直接调用——想绕过外观玩点高级操作的用户，永远有这个自由：

```python
class Projector:
    def on(self) -> None:
        print("投影仪：开机")


class Curtain:
    def close(self) -> None:
        print("窗帘：拉上")


class Light:
    def dim(self, percent: int) -> None:
        print(f"灯光：{percent}%")


class HomeTheaterFacade:
    """外观：一键观影"""

    def __init__(self):
        self.projector = Projector()
        self.curtain = Curtain()
        self.light = Light()

    def watch_movie(self, movie: str) -> None:
        print(f"===== 观影《{movie}》 =====")
        self.light.dim(10)
        self.curtain.close()
        self.projector.on()


# 普通用户：走外观，一条命令搞定
HomeTheaterFacade().watch_movie("功夫熊猫")

# 高级用户：不买外观的账，直接操作子系统——外观从不阻止你
print("——下午只想拉窗帘、不开投影——")
Curtain().close()
Light().dim(60)
```

运行输出：

```
===== 观影《功夫熊猫》 =====
灯光：10%
窗帘：拉上
投影仪：开机
——下午只想拉窗帘、不开投影——
窗帘：拉上
灯光：60%
```

两种方式并行不悖：**想省事，走外观；想精细控制，直接碰子系统。** 这就是外观与"把子系统藏起来"的本质区别——它做的是"简化"，不是"封锁"。

---

## 4. Python 特有玩法

### 4.1 模块即外观

Python 里最天然的外观，就是一个**组织良好的模块**：内部可以有一堆"脏活累活"的私有函数（下划线开头），对外只暴露一两个简洁的公共函数。调用方 `import` 之后，看到的是一张干净的脸：

```python
# ===== 模拟一个组织良好的模块：config_loader.py =====
import os
import tempfile


# 模块内部：三个"脏活累活"的私有函数（下划线 = 对外不可见）
def _read_raw(path: str) -> str:
    print("  底层：读取配置文件")
    with open(path, encoding="utf-8") as f:
        return f.read()


def _parse(text: str) -> dict:
    print("  底层：解析 INI 格式")
    result = {}
    for line in text.splitlines():
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            result[key.strip()] = value.strip()
    return result


def _validate(config: dict) -> dict:
    print("  底层：校验必填字段")
    if "name" not in config:
        raise ValueError("缺少 name 字段")
    return config


# 模块对外：只暴露这一个"外观函数"
def load_config(path: str) -> dict:
    """读配置：读取 → 解析 → 校验，调用方一行搞定"""
    return _validate(_parse(_read_raw(path)))


# ===== 调用方：完全不知道模块内部有三个函数 =====
with tempfile.NamedTemporaryFile("w", suffix=".ini", delete=False, encoding="utf-8") as f:
    f.write("# 我的配置\nname=小明\nlevel=3\n")
    tmp_path = f.name

try:
    config = load_config(tmp_path)
    print("调用方拿到的配置：", config)
finally:
    os.unlink(tmp_path)
```

运行输出：

```
  底层：读取配置文件
  底层：解析 INI 格式
  底层：校验必填字段
调用方拿到的配置： {'name': '小明', 'level': '3'}
```

调用方眼里只有 `load_config` 这一个名字，模块内部的 `_read_raw`、`_parse`、`_validate` 它一概不知。**一个模块的公共 API 就是它的外观**——写模块的时候，你其实就在设计一个外观。

### 4.2 `*args` / `**kwargs` 转发

Python 的 `*args` / `**kwargs` 让外观的"传话"能力极其灵活：外观不需要列出子系统的每一个参数，原样转发即可：

```python
class CoffeeMachine:
    """咖啡机子系统：一堆可选项"""

    def make(self, beans="阿拉比卡", grind=3, milk="全脂", sugar=0, size="中杯"):
        parts = [f"{size}咖啡", beans, f"研磨度{grind}"]
        if milk:
            parts.append(f"{milk}奶")   # milk 传"全脂"→"全脂奶"，传"燕麦"→"燕麦奶"
        if sugar:
            parts.append(f"{sugar}块糖")
        print("制作：", "、".join(parts))


class BaristaFacade:
    """咖啡师外观：顾客点什么，就原样转达给机器"""

    def __init__(self):
        self._machine = CoffeeMachine()

    def order(self, *args, **kwargs):
        """外观不拆解参数，原样转发给子系统"""
        self._machine.make(*args, **kwargs)


barista = BaristaFacade()
barista.order()                                    # 什么都不说：默认一杯
barista.order(beans="云南小粒", size="大杯")        # 只改部分参数
barista.order("瑰夏", 5, milk="燕麦", sugar=1)      # 位置参数 + 关键字参数混用
```

运行输出：

```
制作： 中杯咖啡、阿拉比卡、研磨度3、全脂奶
制作： 大杯咖啡、云南小粒、研磨度3、全脂奶
制作： 中杯咖啡、瑰夏、研磨度5、燕麦奶、1块糖
```

外观既提供了"一句话下单"的便捷，又保留了子系统的全部灵活性——参数照单全收、原样转发，这就是 Python 动态特性给外观模式送的见面礼。

---

## 5. 真实世界中的它

### 5.1 `requests`：把 HTTP 的"后厨"整个藏起来

用过 Python 的人都爱 `requests`：一行 `requests.get(url)` 拿到响应。背后呢？`requests` 封装了 `urllib3`（连接池、重试、证书校验），`urllib3` 又封装了标准库 `http.client`（最底层的 HTTP 协议操作）。**`requests` 就是一个典型的外观**：底层再复杂，对外永远是一张干净的脸。

标准库自带的 `http.client` 有多繁琐？我们起一个本地微型接口服务，先体验"没有 requests 的世界"：

```python
import http.client
import http.server
import json
import threading
import urllib.parse


class ApiHandler(http.server.BaseHTTPRequestHandler):
    """本地测试用微型接口服务"""

    def do_GET(self):
        # ensure_ascii=False：让中文以原文输出（否则会变成 \u5c0f\u660e 转义）
        body = json.dumps({"code": 0, "data": {"name": "小明", "level": 3}}, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass  # 屏蔽请求日志，保持输出干净


server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), ApiHandler)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()

# 方式一：直接用 http.client——拼请求、读响应、解析 JSON 全要自己来
conn = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
conn.request("GET", "/api/user/1")
resp = conn.getresponse()
raw = resp.read().decode("utf-8")
print("http.client 手写：", raw)
conn.close()

# 方式二：一个迷你 requests——把上面那堆步骤都藏进外观
class MiniRequests:
    """外观：仿 requests 的极简版，只封装 http.client"""

    def get(self, url: str) -> dict:
        parts = urllib.parse.urlsplit(url)
        conn = http.client.HTTPConnection(parts.hostname, parts.port, timeout=3)
        conn.request("GET", parts.path)
        resp = conn.getresponse()
        data = json.loads(resp.read().decode("utf-8"))
        conn.close()
        return data


data = MiniRequests().get(f"http://127.0.0.1:{port}/api/user/1")
print("MiniRequests 一行：", data)

server.shutdown()
thread.join()
```

运行输出：

```
http.client 手写： {"code": 0, "data": {"name": "小明", "level": 3}}
MiniRequests 一行： {'code': 0, 'data': {'name': '小明', 'level': 3}}
```

同样的请求，`http.client` 要四五行，包一层外观后一行搞定。真实的 `requests` 还多了连接池、超时、重试、Session、Cookie 管理等一整套"后厨设备"，但对外依然是 `get` / `post` 几个动词——**把复杂留给内部，把简单留给世界**。

### 5.2 `shutil`：文件操作的"一站式服务"

标准库的 `shutil` 模块也是外观的化身：`shutil.copyfile`、`shutil.move`、`shutil.rmtree` 背后，是一堆 `os` 层级的底层操作。复制一个文件，用 `os` 得自己开文件、读字节、写字节、关文件；用 `shutil` 一行完事：

```python
import os
import shutil

# 在当前目录创建两个"假图片"文件（本示例的工作目录是隔离的临时目录）
src = "photo.jpg"
dst = "backup.jpg"
with open(src, "wb") as f:
    f.write(b"\xff\xd8" + b"0" * 1024)   # 伪造一张 1026 字节的"图片"

# 方式一：手动复制（模拟 os 层面的繁琐）
with open(src, "rb") as f_in, open(dst, "wb") as f_out:
    f_out.write(f_in.read())
print("手动复制完成，大小：", os.path.getsize(dst), "字节")

# 方式二：shutil.copyfile——一行搞定
shutil.copyfile(src, dst)
print("shutil 复制完成，大小：", os.path.getsize(dst), "字节")

# 清理临时文件
os.remove(src)
os.remove(dst)
```

运行输出：

```
手动复制完成，大小： 1026 字节
shutil 复制完成，大小： 1026 字节
```

`shutil` 内部帮你处理了"打开、读、写、关闭、处理错误"这些琐事，你只需要说"复制这个文件"——一个教科书级的外观。

---

## 6. 优缺点与适用场景

### 优点

- **调用方省心**：一个简单接口代替一堆子系统调用，学习成本骤降；
- **解耦**：调用方只依赖外观，子系统怎么换都不惊动客户端（开闭原则）；
- **集中管理**：流程编排、失败处理都收在外部一处，不再散落各调用方；
- **不设门槛**：外观是简化，不是封锁，高级用户仍可直接访问子系统。

### 缺点

- **多一层间接**：过度封装会让调用方失去对细节的控制力；
- **外观可能膨胀**：如果什么都往外观里塞，外观本身会变成"上帝类"（见常见误区）；
- **掩盖问题**：外观能藏住复杂性，也能藏住糟糕的设计——子系统烂，外观只是块遮羞布。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 复杂的子系统组合（下单、报表、多媒体） | 只有一个类、调用也简单的场景 |
| 想让第三方/新手用得轻松的库 API | 调用方需要精细控制每个子系统时 |
| 分层架构中给"上层"提供入口 | 用外观掩盖子系统本身的混乱 |
| 重构遗留系统（先包一层，再逐步替换内部） | 外观自身职责已经失控的场景 |

> **Python 圈的共识**：外观模式在 Python 里常常"退化"成一个组织良好的模块或几个顶层函数——先想清楚公共 API 长什么样，再想类的事。

---

## 7. 与其他模式的关系

- **外观 vs 适配器**：适配器是**转换**——把旧接口翻译成新接口，让不兼容的东西能用；外观是**简化**——把一堆接口整理成一个更简单的入口。适配器只有一个"翻译对象"，外观管着一群子系统；
- **外观 vs 中介者**：外观是**单向**的——客户端 → 外观 → 子系统，子系统之间不通过外观互相通信；中介者是**双向**的——所有对象都通过中介者传话，避免网状耦合（第 19 章）；
- **外观 + 单例**：一个系统通常只需要一个门面，所以外观经常和单例搭配（第 1 章）——共享一个前台；
- **外观 + 工厂**：外观内部创建子系统时，可以用工厂方法（第 7 章）来决定"具体用哪个子系统实现"。

---

## 8. 常见误区

### 误区 1：把外观做成"上帝类"

外观的职责是"简化子系统的使用"，不是"包揽所有业务"。有人写着写着，就把退款、开发票、改密码、发短信全塞进同一个外观——它变成了一个什么都管、改谁都疼的垃圾场，违背了**单一职责原则**：

```python
# 反面教材：上帝外观——什么都往里塞
class GodFacade:
    """下单、退款、发票、密码、短信……全包了"""

    def place_order(self):
        print("下单")

    def refund(self):
        print("退款")

    def invoice(self):
        print("开发票")

    def reset_password(self):
        print("重置密码")   # ← 这跟下单系统有什么关系？

    def send_sms(self):
        print("发短信")     # ← 又一个八竿子打不着的

    def calculate_shipping(self):
        print("算运费")

    # ……还在继续膨胀


facade = GodFacade()
facade.place_order()
facade.reset_password()   # 外观变成了杂物间
```

运行输出：

```
下单
重置密码
```

**正确的做法**：按业务域拆成多个小外观——订单域一个、财务域一个、账号域一个。每个外观只聚合"同一件事"的子系统。

### 误区 2：把外观和适配器、中介者混为一谈

三者长得有点像，但动机完全不同。适配器是"**接口转换**"，外观是"**接口简化**"，中介者是"**对象间的传话人**"：

```python
# 适配器：把"旧接口"翻译成"新接口"——转换
class OldSocket:
    def plug(self) -> str:
        return "老式插头"


class UsbCAdapter:
    """适配器：让老插头能插进新插座"""

    def __init__(self, old: OldSocket):
        self._old = old

    def usb_c(self) -> str:
        return f"{self._old.plug()} → 转成 USB-C"


# 外观：把"一堆子系统"简化成"一个入口"——简化
class TV:
    def on(self):
        print("电视：开机")


class SoundBar:
    def on(self):
        print("音响：开机")


class MediaFacade:
    def __init__(self):
        self._tv = TV()
        self._sound = SoundBar()

    def watch(self):
        self._tv.on()
        self._sound.on()


print(UsbCAdapter(OldSocket()).usb_c())
MediaFacade().watch()
```

运行输出：

```
老式插头 → 转成 USB-C
电视：开机
音响：开机
```

一句话区分：**适配器改的是"接口的形状"，外观改的是"接口的数量"，中介者改的是"对象之间的关系"。**

### 误区 3：以为外观是"唯一入口"，必须封锁子系统

有人把外观当成安全门，想方设法让调用方"只能"走外观，把子系统全部藏起来。这是本末倒置——外观的价值是**便利**，不是**强制**。子系统保持可见，高级用户才能按需定制（见 3.3）。真需要"禁止访问"时，那已经是另一层安全/权限问题了，别用外观硬扛。

### 误区 4：用外观掩盖糟糕的子系统设计

"反正外面包了一层，里面乱就乱吧"——这是最危险的偷懒。外观能藏住复杂性，也能藏住臭味：如果子系统之间互相扯皮、职责混乱，外观只是把混乱集中到了一处。**正确的顺序是：先整理子系统，再决定要不要外观。**

---

## 9. 练习题

### 练习 1：给"面包店"写一个外观

有三个子系统：搅拌机（`Mixer`）、烤箱（`Oven`）、包装机（`Packer`）。请写一个 `BakerFacade`，让"做面包"变成一句话：

```python
# 答案：BakerFacade 把三个子系统串成一条龙
class Mixer:
    def mix(self, ingredient: str) -> None:
        print(f"搅拌 {ingredient}")


class Oven:
    def preheat(self, temp: int) -> None:
        print(f"烤箱预热 {temp} 度")

    def bake(self, minutes: int) -> None:
        print(f"烘烤 {minutes} 分钟")


class Packer:
    def pack(self, product: str) -> None:
        print(f"包装 {product}")


class BakerFacade:
    """面包师外观：从配料到出炉一条龙"""

    def __init__(self):
        self._mixer = Mixer()
        self._oven = Oven()
        self._packer = Packer()

    def make_bread(self, flour: str, temp: int = 180, minutes: int = 30) -> None:
        self._mixer.mix(flour)
        self._oven.preheat(temp)
        self._oven.bake(minutes)
        self._packer.pack("吐司面包")
        print("面包出炉，可以卖了！")


BakerFacade().make_bread("高筋面粉")
```

运行输出：

```
搅拌 高筋面粉
烤箱预热 180 度
烘烤 30 分钟
包装 吐司面包
面包出炉，可以卖了！
```

### 练习 2：拆分"上帝外观"

下面的 `SuperFacade` 把订单、财务、账号三件事混在一个类里。请按业务域拆成三个小外观，并各调用一次：

```python
# 答案：按业务域拆分——每个外观只干一件事
class OrderFacade:
    """订单域外观：只做下单相关"""
    def place_order(self):
        print("下单")
    def refund(self):
        print("退款")


class BillingFacade:
    """财务域外观：只做发票相关"""
    def invoice(self):
        print("开发票")


class AccountFacade:
    """账号域外观：只做账号相关"""
    def reset_password(self):
        print("重置密码")


OrderFacade().place_order()
BillingFacade().invoice()
AccountFacade().reset_password()
```

运行输出：

```
下单
开发票
重置密码
```

### 练习 3：用"模块级外观函数"重写

有一个散乱的播放流程：找文件、加载字幕、设置音轨、播放。请把它们整理成一个模块，对外只暴露一个 `play()` 函数：

```python
# 答案：模块级外观——公共 API 只有一个 play()
def _find_file(name: str) -> None:
    print(f"查找文件：{name}")


def _load_subtitle(name: str) -> None:
    print(f"加载字幕：{name}.srt")


def _set_audio(track: str) -> None:
    print(f"设置音轨：{track}")


def _play(name: str) -> None:
    print(f"正在播放：{name}")


def play(movie: str, audio: str = "国语") -> None:
    """模块的对外 API——外观函数"""
    _find_file(movie)
    _load_subtitle(movie)
    _set_audio(audio)
    _play(movie)


play("流浪地球", audio="粤语")
```

运行输出：

```
查找文件：流浪地球
加载字幕：流浪地球.srt
设置音轨：粤语
正在播放：流浪地球
```

---

## 10. 小结与口诀

> **口诀：一个前台，搞定一切；内部多复杂，外面多简单。想精细操作？高级用户随时可以绕过前台。**

外观模式是"为复杂性减负"的模式：它不改变子系统的能力，只是把"怎么配合"这件事集中到一处。记住三条：

1. **外观是简化，不是封锁**——子系统永远保持可访问；
2. **按业务域拆外观**，别让外观变成上帝类；
3. Python 里最地道的"外观"往往是一个**组织良好的模块**——先把公共 API 设计好。

下一章，我们进入创建型家族，看看比简单工厂更"讲究"的套路——**工厂方法**：把"创建谁"的决定权交给子类。

---

*本章金句：外观模式的本质是"复杂度隔离"——让大多数调用方只认识一个简单入口，剩下的复杂让子系统自己消化。*
