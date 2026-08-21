# 第 10 章 适配器模式（Adapter）

> **一句话总结**：接口不一样？加个转换层，两边都别改。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 结构型 | ★★☆☆☆ | ★★★★☆ |

---

## 1. 引子：先讲个故事

你从美国出差回来，带了一个充电器，插头是两根平行的扁脚（美标）。回到家往墙上的国标插座一插——插不进去。你不会去拆墙换插座，也不会把充电器扔了，你会去便利店买一个**转换插头**：一头插充电器，一头插插座，两头都不用动，问题就解决了。

程序世界里这种事天天发生：新系统要的接口是 A，老系统只提供接口 B，两边都是"大爷"，谁都不肯改。硬怼的结果就是闹笑话：

```python
# 引子：老设备只输出华氏度，新系统只认摄氏度——直接怼上就出洋相
class OldThermometer:
    """服役十年的老温度计：只会报华氏度"""

    def read_fahrenheit(self):
        return 98.6

class NewDisplay:
    """新买的智能大屏：只接受摄氏度"""

    def show(self, celsius):
        print(f"当前体温：{celsius:.1f} ℃")

old = OldThermometer()
display = NewDisplay()
# 直接把华氏度塞给摄氏度显示器——98.6 ℉ 被当成 98.6 ℃，离谱
display.show(old.read_fahrenheit())
```

运行输出：

```
当前体温：98.6 ℃
```

看到没？98.6 华氏度（正常体温）被显示成 98.6 摄氏度（发烧 40 分钟人就没了）。问题不在温度计，也不在显示屏，而在**两边接口不匹配**。**适配器模式**就是程序世界的"转换插头"：中间垫一层，把一边的接口翻译成另一边听得懂的话，两边都不用改。

---

## 2. 模式登场

### 定义

> **适配器模式**：将一个类的接口转换成客户端期望的另一个接口，让原本因接口不兼容而无法协作的类可以一起工作。

### 解决的问题

1. **新旧系统对接**：老系统的接口跟新系统不匹配，又不能重写老系统；
2. **第三方库封装**：库的接口风格跟你的代码风格不一致（比如它给你 XML，你要 JSON）；
3. **复用现有类**：一个类功能完全符合需求，只是方法名、参数长得不一样。

### 结构

```
┌────────────────────────────┐
│      Target（目标接口）       │
├────────────────────────────┤
│ + request()                │  ← 客户端期望的接口
└────────────────────────────┘
        ▲
        │ 实现
┌───────┴───────────────────────────────┐
│            Adapter（适配器）             │
├────────────────────────────────────────┤
│ - adaptee: Adaptee                    │  ← 组合：持有被适配对象
├────────────────────────────────────────┤
│ + request()                           │  ← 内部转调 adaptee 的方法
└────────────────────────────────────────┘
        ▲
        │ 组合（持有）
┌───────┴───────────────────────────────┐
│         Adaptee（被适配者）              │
├────────────────────────────────────────┤
│ + specific_request()                  │  ← 老接口，名字不一样
└────────────────────────────────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **目标接口 Target** | 客户端期望的接口，也就是新系统的"标准插孔" |
| **适配器 Adapter** | 实现目标接口，内部把调用"翻译"给被适配者 |
| **被适配者 Adaptee** | 老接口或第三方类，接口跟目标不匹配 |
| **客户端 Client** | 只认目标接口，完全不知道适配器的存在 |

关键点：**适配器不改原类，也不改调用方**——它只是夹在中间的那个转换插头。

---

## 3. Python 实现

### 3.1 经典对象适配器（组合）

对象适配器用**组合**：适配器内部持有一个被适配对象，把目标接口的调用翻译成被适配对象能听懂的方法。这是最常用、也最推荐的方式（呼应导读里的"组合优于继承"）：

```python
class OldThermometer:
    """老设备：只能读出华氏温度"""

    def read_fahrenheit(self):
        return 98.6

class NewDisplay:
    """新系统：只接受摄氏度"""

    def show(self, celsius):
        print(f"当前体温：{celsius:.1f} ℃")

class FahrenheitToCelsiusAdapter:
    """对象适配器：包住老设备，对外提供新接口"""

    def __init__(self, thermometer):
        self._thermometer = thermometer      # 组合：持有被适配对象

    def read_celsius(self):
        """翻译：华氏度 → 摄氏度"""
        f = self._thermometer.read_fahrenheit()
        return (f - 32) * 5 / 9

display = NewDisplay()
adapter = FahrenheitToCelsiusAdapter(OldThermometer())
display.show(adapter.read_celsius())        # 新系统眼里，这就是个"摄氏度温度计"
```

运行输出：

```
当前体温：37.0 ℃
```

注意：`OldThermometer` 一行没改，`NewDisplay` 一行没改，中间只多了一个适配器，两边就接上了。

### 3.2 类适配器（继承）

类适配器用**继承**：直接继承被适配类，在子类里补上目标接口。在 Python 里这种写法比较少——因为 Python 支持多重继承，继承路径容易乱；而且继承把"被适配者"死死绑在适配器身上，想换一个被适配者就得再写一个类：

```python
class OldThermometer:
    """老设备：只能读出华氏温度"""

    def read_fahrenheit(self):
        return 98.6

class CelsiusThermometer(OldThermometer):
    """类适配器：继承老设备，补上新接口"""

    def read_celsius(self):
        return (self.read_fahrenheit() - 32) * 5 / 9

t = CelsiusThermometer()
print(f"摄氏度读数：{t.read_celsius():.1f} ℃")
print(f"老接口还在：{t.read_fahrenheit()} ℉")
```

运行输出：

```
摄氏度读数：37.0 ℃
老接口还在：98.6 ℉
```

> **经验之谈**：Python 里优先用对象适配器（组合）。只有当"被适配者"是一组需要同时保留的方法、且继承关系本来就合理时，才考虑类适配器。

### 3.3 函数式适配器：适配"签名"不匹配

Python 里函数是一等公民，很多"类与类"的适配，退化成"函数包函数"就够了。比如老函数返回 `(数值, 单位)` 元组，新代码只收纯数值：

```python
# 老代码：返回 (数值, 单位) 元组
def read_temperature():
    return 98.6, "F"

# 新代码：只收一个纯数值
def show_celsius(value):
    print(f"当前体温：{value:.1f} ℃")

# 函数式适配：包一层，把元组"翻译"成纯数值
def adapt_read():
    value, unit = read_temperature()
    if unit == "F":
        value = (value - 32) * 5 / 9
    return value

show_celsius(adapt_read())
```

运行输出：

```
当前体温：37.0 ℃
```

函数式适配的好处是零类开销：老函数、新函数都不动，一个包装函数就完成了"翻译"。

---

## 4. Python 特有玩法

### 4.1 鸭子类型：被适配对象不需要继承任何接口

在 Java/C++ 里，适配器必须显式实现某个接口（`implements Target`）。Python 信奉鸭子类型——**只要对象有目标方法，它就能被当成目标用**，连接口都不用声明。所以我们的适配器只要"长得像"目标就行：

```python
class USBDevice:
    """新系统要求的接口：有 transfer 方法"""

    def transfer(self, data):
        print(f"USB 传输：{data}")

class OldPrinter:
    """老设备：只有 print_document 方法，没有 transfer"""

    def print_document(self, doc):
        print(f"打印机输出：{doc}")

class PrinterAdapter:
    """适配器：把 print_document 翻译成 transfer"""

    def __init__(self, printer):
        self._printer = printer

    def transfer(self, data):
        self._printer.print_document(data)

def connect_to_pc(device):
    """电脑只认 transfer 方法（鸭子类型，不检查类型）"""
    device.transfer("年度报告.pdf")

connect_to_pc(USBDevice())                  # 本来就兼容，直接用
connect_to_pc(PrinterAdapter(OldPrinter())) # 老设备包一层适配器
```

运行输出：

```
USB 传输：年度报告.pdf
打印机输出：年度报告.pdf
```

`OldPrinter` 没有继承任何 USB 接口，`PrinterAdapter` 也没有——它们只是"恰好有 `transfer` 方法"，电脑就认了。这就是 Python 里适配器可以写得很轻的原因。

### 4.2 `__getattr__` 自动转发：万能适配器

如果老接口有一堆方法要适配，一个个手写转发太啰嗦。Python 的 `__getattr__` 钩子可以**把所有未知属性自动转发**给被适配对象，十几行就是一个万能适配器：

```python
class LegacyAPI:
    """老接口：一堆方法，名字各不相同"""

    def get_user_name(self):
        return "小明"

    def get_user_age(self):
        return 18

class AutoForwardAdapter:
    """万能适配器：自己不认识的调用，全部转发给被适配对象"""

    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        # 只在属性查找失败时触发：把请求转发给被适配对象
        return getattr(self._target, name)

adapter = AutoForwardAdapter(LegacyAPI())
print(adapter.get_user_name())   # 适配器自己没这个方法 → 自动转发
print(adapter.get_user_age())
```

运行输出：

```
小明
18
```

注意：`__getattr__` 只在属性**找不到**时才触发，所以 `adapter.get_user_name()` 会被转发成 `LegacyAPI.get_user_name(adapter)`？不对——`getattr(self._target, name)` 返回的是**绑定到 `_target` 的方法**，调用时 `self` 是 `_target`，不是适配器。这正是我们要的效果：转发得干干净净。递归陷阱见第 8 节误区 3。

### 4.3 适配 `collections.abc` 协议：让自定义类支持 `len()` / `iter()`

Python 的"协议"就是轻量接口。把自定义类适配成 `Sequence` 协议后，`len()`、下标、`in`、遍历全都自动可用：

```python
from collections.abc import Sequence

class Playlist(Sequence):
    """把歌单适配成序列协议：支持 len()、下标、in、遍历"""

    def __init__(self, songs):
        self._songs = list(songs)

    def __len__(self):
        return len(self._songs)

    def __getitem__(self, index):
        return self._songs[index]

songs = Playlist(["晴天", "七里香", "稻香"])
print(f"共 {len(songs)} 首")                # len() 来自 __len__
print("第 2 首：", songs[1])                # 下标来自 __getitem__
print("'晴天' 在歌单里吗：", "晴天" in songs)  # in 由 Sequence 自动补全
print("遍历：", " / ".join(songs))          # 迭代由 Sequence 自动补全
```

运行输出：

```
共 3 首
第 2 首： 七里香
'晴天' 在歌单里吗： True
遍历： 晴天 / 七里香 / 稻香
```

我们只实现了两个方法，`in`、`join`、`reversed` 这些全是 `Sequence` 基类基于 `__len__`/`__getitem__` 自动补全的——这就是"适配到协议"的威力：**接口隔离原则**说客户端不该依赖用不到的接口，而协议恰好只要求实现最核心的那几个方法。

---

## 5. 真实世界中的它

### 标准库：`json.dumps` 的 `default` 参数

序列化时，`datetime` 这种对象 JSON 不认识。`json.dumps` 的 `default` 参数就是官方预留的"适配器插槽"：你提供一个函数，把不认识的对象翻译成 JSON 能序列化的类型——典型的适配器思想，而且天天在用：

```python
import json
from datetime import datetime, date

def json_default(obj):
    """适配器：把不认识的对象翻译成可序列化的类型"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"类型 {type(obj).__name__} 不可序列化")

data = {"name": "会议", "time": datetime(2024, 6, 1, 9, 30)}
print(json.dumps(data, default=json_default, ensure_ascii=False))
```

运行输出：

```
{"name": "会议", "time": "2024-06-01T09:30:00"}
```

`datetime` 类没改，`json.dumps` 也没改，中间一个 `json_default` 函数就把两边接上了。

### 标准库：`sqlite3.Row` 适配"字典式访问"

`sqlite3` 返回的 `Row` 对象同时支持两种访问方式：按下标（像元组）和按列名（像字典）——它把数据库的行"适配"成了两种接口都能用的对象：

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row        # 启用 Row 工厂：行变成"元组+字典"双接口
conn.execute("CREATE TABLE user (id INTEGER, name TEXT)")
conn.execute("INSERT INTO user VALUES (1, '小明')")
row = conn.execute("SELECT id, name FROM user").fetchone()

print("按下标访问：", row[1])          # 像元组
print("按列名访问：", row["name"])     # 像字典
```

运行输出：

```
按下标访问： 小明
按列名访问： 小明
```

### 标准库：`pathlib.Path` 统一了 `os.path`

老一代的文件路径操作是 `os.path.join("a", "b")`、`os.path.exists(p)` 这种"函数 + 字符串"风格；`pathlib.Path` 把它们适配成了面向对象风格：`Path("a") / "b"`、`p.exists()`。同一个文件系统，两套接口，`pathlib` 就是那层转换插头——现在官方推荐直接用它。

---

## 6. 优缺点与适用场景

### 优点

- **不改旧代码**：老系统、第三方库一行不动，符合**开闭原则**（对扩展开放，对修改关闭）；
- **解耦**：客户端只依赖目标接口，不知道也不关心背后是谁；
- **复用**：让本不能共存的类一起工作，代码不用重写。

### 缺点

- **多一层间接**：调用多跳一次，轻微的性能与调试成本；
- **可能掩盖设计问题**：如果到处都在适配，说明当初接口设计就乱了；
- **类适配器有继承耦合**：把被适配者绑死在继承树上。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 新旧系统对接、逐步迁移 | 两边接口其实能直接兼容（先试试鸭子类型） |
| 封装第三方库的"别扭"接口 | 接口经常变、需要频繁改适配逻辑 |
| 统一多个相似但不同的接口 | 只是想让代码"看起来统一"，却牺牲了直接性 |

---

## 7. 与其他模式的关系

- **适配器 vs 外观**：适配器**改接口**（让接口匹配），外观**简化接口**（把一堆接口打包成一个）。适配器是"翻译"，外观是"前台"；
- **适配器 vs 代理**：代理**不改接口**（跟真实对象接口一模一样），适配器**改接口**。代理说"我替你办事"，适配器说"我替你翻译"；
- **适配器 vs 桥接**：桥接是**事前设计**（一开始就把抽象与实现分开，让它们各自演化），适配器是**事后补救**（系统写完了才发现不兼容）；
- **适配器 + 工厂**：工厂负责创建"哪款适配器"，两者常搭配使用。

---

## 8. 常见误区

### 误区 1：把适配器和外观搞混

适配器**改接口**：华氏变摄氏，方法名都换了。外观**简化接口**：方法还是那些方法，只是打包成一个"一键操作"。用途完全不同：

```python
# 适配器：改接口——老温度计说华氏，适配后说摄氏
class OldThermometer:
    def read_fahrenheit(self):
        return 98.6

class TempAdapter:
    def __init__(self, old):
        self._old = old

    def read_celsius(self):
        return (self._old.read_fahrenheit() - 32) * 5 / 9

adapter = TempAdapter(OldThermometer())
print("适配器改了接口：", f"{adapter.read_celsius():.1f} ℃")

# 外观：简化接口——把一大堆操作合成一个"一键离家"
class Light:
    def turn_off(self):
        print("灯已关")

class AirConditioner:
    def turn_off(self):
        print("空调已关")

class Door:
    def lock(self):
        print("门已锁")

class HomeFacade:
    """外观：把 3 个操作打包成 1 个"""

    def __init__(self):
        self.light = Light()
        self.ac = AirConditioner()
        self.door = Door()

    def leave_home(self):
        self.light.turn_off()
        self.ac.turn_off()
        self.door.lock()

HomeFacade().leave_home()
```

运行输出：

```
适配器改了接口： 37.0 ℃
灯已关
空调已关
门已锁
```

### 误区 2：过度适配——能用鸭子类型直接兼容，就别写适配器

如果目标接口恰好就是被适配对象已有的方法，直接传进去就行，包装一层纯属多余：

```python
class ModernPrinter:
    """新打印机：本来就有 transfer 方法"""

    def transfer(self, data):
        print(f"新打印机传输：{data}")

class OldPrinter:
    """老设备：只有 print_document，没有 transfer"""

    def print_document(self, doc):
        print(f"打印机输出：{doc}")

class PrinterAdapter:
    """只有老设备这种"接口不匹配"的才需要适配器"""

    def __init__(self, printer):
        self._printer = printer

    def transfer(self, data):
        self._printer.print_document(data)

def send_to_device(device, data):
    """调用方只认 transfer（鸭子类型）"""
    device.transfer(data)

send_to_device(ModernPrinter(), "文档.pdf")                   # 零适配，直接用
send_to_device(PrinterAdapter(OldPrinter()), "文档.pdf")      # 老设备才需要包一层
```

运行输出：

```
新打印机传输：文档.pdf
打印机输出：文档.pdf
```

判断标准很简单：**先试试直接传能不能跑，跑不通再写适配器**。为"可能的未来"提前适配，是过度设计。

### 误区 3：`__getattr__` 转发时的无限递归

`__getattr__` 里如果访问了**自身不存在的属性**，会再次触发 `__getattr__`，形成无限递归：

```python
class RecursiveAdapter:
    """反面教材：__getattr__ 里访问自身不存在的属性 → 死循环"""

    def __getattr__(self, name):
        return self.anything   # self.anything 又不存在 → 又触发 __getattr__

try:
    RecursiveAdapter().foo
except RecursionError:
    print("触发 RecursionError：__getattr__ 无限递归")
```

运行输出：

```
触发 RecursionError：__getattr__ 无限递归
```

正确写法：在 `__getattr__` 里只访问**确定存在**的实例属性（比如 `__init__` 里存好的 `self._target`），或者用 `object.__getattribute__(self, "_target")` 强制走真实属性查找；转发目标也不存在时，记得 `raise AttributeError(name)` 而不是返回奇怪的东西。

### 误区 4：适配器里塞业务逻辑

适配器只负责"翻译"，不负责"计算、统计、告警"等业务。塞进去的后果：业务规则散落各处，改规则要翻遍所有适配器（违反**单一职责原则**）：

```python
class OldSensor:
    """老传感器：输出原始读数"""

    def read_raw(self):
        return 100

# 正确姿势：适配器只做"翻译"
class VoltageAdapter:
    def __init__(self, sensor):
        self._sensor = sensor

    def read_voltage(self):
        return self._sensor.read_raw() / 10   # 只翻译单位，不管业务

adapter = VoltageAdapter(OldSensor())
print("电压：", adapter.read_voltage(), "V")
```

运行输出：

```
电压： 10.0 V
```

如果以后要加"电压过高告警"，那是告警类的事，不该写进 `VoltageAdapter`。

---

## 9. 练习题

### 练习 1：给老设备写一个适配器

新播放器只认 `play_audio(file)`，老 Walkman 只有 `play_cassette()`。请写一个适配器让 Walkman 也能被新播放器使用：

```python
# 答案：对象适配器——组合 + 翻译
class Walkman:
    """老设备：只会放磁带"""

    def play_cassette(self):
        return "磁带转动中……"

class WalkmanAdapter:
    """适配器：把 play_cassette 翻译成 play_audio"""

    def __init__(self, walkman):
        self._walkman = walkman

    def play_audio(self, file):
        return f"{file} → {self._walkman.play_cassette()}"

def new_player(device):
    """新播放器：只认 play_audio"""
    print("新播放器：", device.play_audio("我的歌单"))

new_player(WalkmanAdapter(Walkman()))
```

运行输出：

```
新播放器： 我的歌单 → 磁带转动中……
```

### 练习 2：用 `__getattr__` 写一个万能转发适配器

老服务有一堆 `fetch_xxx` 方法，请用一个适配器把它们全部转发出去，一个方法都不用手写：

```python
# 答案：__getattr__ 自动转发
class LegacyService:
    def fetch_orders(self):
        return ["订单1", "订单2"]

    def fetch_users(self):
        return ["用户1", "用户2"]

class ServiceAdapter:
    """万能转发适配器"""

    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        return getattr(self._target, name)

adapter = ServiceAdapter(LegacyService())
print(adapter.fetch_orders())
print(adapter.fetch_users())
```

运行输出：

```
['订单1', '订单2']
['用户1', '用户2']
```

### 练习 3：把 24 小时制适配成 12 小时制

欧洲系统输出 `"23:30"`，美国系统要 `"11:30 PM"`。写一个适配函数（提示：`h % 12` 处理 12 点，`h < 12` 判断 AM/PM）：

```python
# 答案：函数式适配
def to_12h(time_24: str) -> str:
    h, m = map(int, time_24.split(":"))
    period = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12          # 0 点和 12 点都显示为 12
    return f"{h12}:{m:02d} {period}"

print(to_12h("09:30"))
print(to_12h("12:00"))
print(to_12h("23:30"))
print(to_12h("00:15"))
```

运行输出：

```
9:30 AM
12:00 PM
11:30 PM
12:15 AM
```

---

## 10. 小结与口诀

> **口诀：接口不合，垫一层；两边不动，中间转。**

适配器模式是"事后补救"的温柔手段：老代码不动、新代码不动，中间加个转换层，两边就能握手。记住三条：

1. 优先用**对象适配器**（组合），少用类适配器（继承）；
2. Python 里先试试**鸭子类型**能不能直接兼容，不行再写适配器；
3. 适配器只做**翻译**，别往里面塞业务逻辑。

下一章，我们来看创建型模式里的"组装大师"——**建造者模式**：复杂对象，分步骤搭，最后一步才交货。

---

*本章金句：适配器是"接口的翻译官"——两边都不用学对方的语言，中间垫一层，世界就通了。*
