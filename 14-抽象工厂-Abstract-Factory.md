# 第 14 章 抽象工厂（Abstract Factory）

> **一句话总结**：一套产品，成套生产；换工厂，换全家。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 创建型 | ★★★☆☆ | ★★★☆☆ |

---

## 1. 引子：先讲个故事

你装修新家，跑到家具城。销售员问你："先生，您是走现代风还是中式风？"现代风是一整套：布艺沙发、玻璃茶几、白橡木柜子；中式风也是一整套：红木沙发、雕花茶几、实木柜子。你问能不能单买？能。但你刚把现代风沙发搬回家，又配了张中式雕花茶几——客厅瞬间变成灾难现场 🛋️。

程序里也一样。很多系统需要"成套"的对象：一套 UI 主题、一套数据库方言、一套平台控件。麻烦在于，**创建这些对象的代码常常散落在各处，各管各的**：

```python
# 引子：没有抽象工厂的世界——主题"混搭"翻车现场
class LightButton:
    def render(self) -> str:
        return "浅色按钮（白底黑字）"


class DarkButton:
    def render(self) -> str:
        return "深色按钮（黑底白字）"


class LightDialog:
    def render(self) -> str:
        return "浅色弹窗（白底黑框）"


class DarkDialog:
    def render(self) -> str:
        return "深色弹窗（黑底白框）"


def create_button(theme: str) -> object:
    """每个组件一个创建函数，各自用 if 判断主题"""
    if theme == "light":
        return LightButton()
    return DarkButton()


def create_dialog(theme: str) -> object:
    if theme == "light":
        return LightDialog()
    return DarkDialog()


# 模块 A：切了深色主题，创建深色按钮
button = create_button("dark")
# 模块 B：忘了切，还在用默认浅色弹窗
dialog = create_dialog("light")

print(button.render())
print(dialog.render())
print("？按钮深色、弹窗浅色——用户看了想报警")
```

运行输出：

```
深色按钮（黑底白字）
浅色弹窗（白底黑框）
？按钮深色、弹窗浅色——用户看了想报警
```

这段代码有三个毛病：

1. **没人保证成套**：按钮和弹窗由两个函数各自创建，谁也没拦着你混搭；
2. **加主题要改所有函数**：以后加一个"蓝色主题"，`create_button`、`create_dialog`……每一个都要加一个分支；
3. **客户端知道太多**：调用方得知道"按钮是深色、弹窗是浅色"这种细节。

**抽象工厂模式**就是来收拾这个烂摊子的：把"一套产品"的创建逻辑收拢到一个工厂里，**要换就整套换，想混搭？没门。**

---

## 2. 模式登场

### 定义

> **抽象工厂模式**：提供一个创建"一族相关对象"的接口，而无需指定它们的具体类。

注意关键词是"**一族**"。工厂方法（第 7 章）只负责"一个产品"，抽象工厂负责"**一组配套产品**"。

### 解决的问题

1. **产品族一致性**：同一套产品必须成套出现，禁止混搭；
2. **客户端解耦**：客户端只依赖抽象接口，不知道也不关心具体类叫什么名字；
3. **换族如换装**：想换一整套，只要换一个工厂对象。

### 结构

```
              ┌──────────────────────────────┐
              │       UIFactory（抽象工厂）     │
              ├──────────────────────────────┤
              │ + create_button() -> Button  │
              │ + create_dialog() -> Dialog  │
              └──────────────────────────────┘
                          ▲
            ┌─────────────┴─────────────┐
            │                           │
   ┌────────────────┐         ┌────────────────┐
   │  WindowsFactory │         │   LinuxFactory  │
   ├────────────────┤         ├────────────────┤
   │ create_button  │         │ create_button  │
   │ create_dialog  │         │ create_dialog  │
   └────────────────┘         └────────────────┘
       │          │               │          │
       ▼          ▼               ▼          ▼
┌───────────┐┌───────────┐ ┌───────────┐┌───────────┐
│WinButton  ││WinDialog  │ │LinuxButton││LinuxDialog│
└───────────┘└───────────┘ └───────────┘└───────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **抽象工厂** | 定义"一族产品"的创建接口（UIFactory） |
| **具体工厂** | 实现某个产品族的所有产品（WindowsFactory / LinuxFactory） |
| **抽象产品** | 某类产品的共同接口（Button / Dialog） |
| **具体产品** | 某个产品族里的具体实现（WinButton / LinuxDialog） |
| **客户端** | 只依赖抽象工厂和抽象产品，与具体类彻底解耦 |

---

## 3. Python 实现

### 3.1 经典版：跨平台 UI 组件

先来最标准的写法。要做一个跨平台应用：Windows 上的按钮是圆角的，Linux 上的按钮是直角的，输入框、弹窗也各有各的脾气。用抽象工厂把每个平台"整套"打包：

```python
from abc import ABC, abstractmethod


# ── 抽象产品：三类组件的统一接口 ──
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError


class TextBox(ABC):
    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError


class Dialog(ABC):
    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError


# ── 具体产品：Windows 一套 ──
class WindowsButton(Button):
    def render(self) -> str:
        return "渲染 [Windows 按钮]（圆角、蓝色高亮）"


class WindowsTextBox(TextBox):
    def render(self) -> str:
        return "渲染 [Windows 输入框]（带聚焦边框）"


class WindowsDialog(Dialog):
    def render(self) -> str:
        return "渲染 [Windows 弹窗]（带关闭按钮）"


# ── 具体产品：Linux 一套 ──
class LinuxButton(Button):
    def render(self) -> str:
        return "渲染 [Linux 按钮]（直角、极简风）"


class LinuxTextBox(TextBox):
    def render(self) -> str:
        return "渲染 [Linux 输入框]（无边框）"


class LinuxDialog(Dialog):
    def render(self) -> str:
        return "渲染 [Linux 弹窗]（带确定/取消）"


# ── 抽象工厂：定义"一族产品"的创建接口 ──
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        raise NotImplementedError

    @abstractmethod
    def create_textbox(self) -> TextBox:
        raise NotImplementedError

    @abstractmethod
    def create_dialog(self) -> Dialog:
        raise NotImplementedError


# ── 具体工厂：每个平台一套 ──
class WindowsFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_textbox(self) -> TextBox:
        return WindowsTextBox()

    def create_dialog(self) -> Dialog:
        return WindowsDialog()


class LinuxFactory(UIFactory):
    def create_button(self) -> Button:
        return LinuxButton()

    def create_textbox(self) -> TextBox:
        return LinuxTextBox()

    def create_dialog(self) -> Dialog:
        return LinuxDialog()


def build_login_page(factory: UIFactory) -> None:
    """客户端只认抽象工厂：不管底层是 Windows 还是 Linux"""
    print(factory.create_button().render())
    print(factory.create_textbox().render())
    print(factory.create_dialog().render())


print("=== 在 Windows 上构建登录页 ===")
build_login_page(WindowsFactory())
print("=== 在 Linux 上构建登录页 ===")
build_login_page(LinuxFactory())
```

运行输出：

```
=== 在 Windows 上构建登录页 ===
渲染 [Windows 按钮]（圆角、蓝色高亮）
渲染 [Windows 输入框]（带聚焦边框）
渲染 [Windows 弹窗]（带关闭按钮）
=== 在 Linux 上构建登录页 ===
渲染 [Linux 按钮]（直角、极简风）
渲染 [Linux 输入框]（无边框）
渲染 [Linux 弹窗]（带确定/取消）
```

`build_login_page` 从头到尾不知道 `WindowsButton`、`LinuxDialog` 这些名字——它只跟 `UIFactory` 打交道。**具体类藏在工厂背后，这就是依赖倒置原则（DIP）的实战。**

### 3.2 数据库方言版：连接 + 查询 + 转义

产品不一定是"控件"，也可以是一组**语义上必须配套**的对象。不同数据库的方言差异很大：MySQL 的标识符用反引号，PostgreSQL 用双引号。连接、查询构造器、转义规则必须来自同一个方言，混着用必出 bug：

```python
from abc import ABC, abstractmethod


class Connection(ABC):
    @abstractmethod
    def execute(self, sql: str) -> str:
        raise NotImplementedError


class SQLBuilder(ABC):
    @abstractmethod
    def quote_identifier(self, name: str) -> str:
        raise NotImplementedError


class MySQLConnection(Connection):
    def __init__(self, host: str):
        self.host = host

    def execute(self, sql: str) -> str:
        return f"[MySQL] 在 {self.host} 上执行：{sql}"


class PostgreSQLConnection(Connection):
    def __init__(self, host: str):
        self.host = host

    def execute(self, sql: str) -> str:
        return f"[PostgreSQL] 在 {self.host} 上执行：{sql}"


class MySQLBuilder(SQLBuilder):
    def quote_identifier(self, name: str) -> str:
        return f"`{name}`"        # MySQL 用反引号


class PostgreSQLBuilder(SQLBuilder):
    def quote_identifier(self, name: str) -> str:
        return f'"{name}"'        # PostgreSQL 用双引号


class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self, host: str) -> Connection:
        raise NotImplementedError

    @abstractmethod
    def create_sql_builder(self) -> SQLBuilder:
        raise NotImplementedError


class MySQLFactory(DatabaseFactory):
    def create_connection(self, host: str) -> Connection:
        return MySQLConnection(host)

    def create_sql_builder(self) -> SQLBuilder:
        return MySQLBuilder()


class PostgreSQLFactory(DatabaseFactory):
    def create_connection(self, host: str) -> Connection:
        return PostgreSQLConnection(host)

    def create_sql_builder(self) -> SQLBuilder:
        return PostgreSQLBuilder()


def query_users(factory: DatabaseFactory, host: str, table: str) -> None:
    """同一段业务代码，跑在哪个数据库上由工厂决定"""
    conn = factory.create_connection(host)
    builder = factory.create_sql_builder()
    sql = f"SELECT * FROM {builder.quote_identifier(table)} WHERE id = ?"
    print(conn.execute(sql))


print("=== 业务代码跑在 MySQL 上 ===")
query_users(MySQLFactory(), "db-mysql-01", "users")
print("=== 业务代码跑在 PostgreSQL 上 ===")
query_users(PostgreSQLFactory(), "db-pg-01", "users")
```

运行输出：

```
=== 业务代码跑在 MySQL 上 ===
[MySQL] 在 db-mysql-01 上执行：SELECT * FROM `users` WHERE id = ?
=== 业务代码跑在 PostgreSQL 上 ===
[PostgreSQL] 在 db-pg-01 上执行：SELECT * FROM "users" WHERE id = ?
```

注意：连接和 SQL 构造器**永远成套出现**。你没法从 MySQL 工厂里拿到一个 PostgreSQL 的构造器——因为客户端只能通过工厂拿产品，而工厂是"一族"的。

### 3.3 主题切换版：换工厂 = 换全家

最常见的实际用法：**运行时按配置选工厂**。用户切了深色主题，整个 UI 自动换装：

```python
class Button:
    def render(self) -> str:
        return "通用按钮"


class LightButton(Button):
    def render(self) -> str:
        return "浅色按钮（白底黑字）"


class DarkButton(Button):
    def render(self) -> str:
        return "深色按钮（黑底白字）"


class Dialog:
    def render(self) -> str:
        return "通用弹窗"


class LightDialog(Dialog):
    def render(self) -> str:
        return "浅色弹窗（白底黑框）"


class DarkDialog(Dialog):
    def render(self) -> str:
        return "深色弹窗（黑底白框）"


class ThemeFactory:
    """抽象工厂：这里故意不用 ABC，靠子类重写 + 鸭子类型"""

    def create_button(self) -> Button:
        raise NotImplementedError

    def create_dialog(self) -> Dialog:
        raise NotImplementedError


class LightThemeFactory(ThemeFactory):
    def create_button(self) -> Button:
        return LightButton()

    def create_dialog(self) -> Dialog:
        return LightDialog()


class DarkThemeFactory(ThemeFactory):
    def create_button(self) -> Button:
        return DarkButton()

    def create_dialog(self) -> Dialog:
        return DarkDialog()


def get_theme_factory(name: str) -> ThemeFactory:
    """根据用户偏好返回对应工厂——运行时决定用哪一套"""
    if name == "light":
        return LightThemeFactory()
    if name == "dark":
        return DarkThemeFactory()
    raise ValueError(f"未知主题：{name}")


def apply_theme(name: str) -> None:
    factory = get_theme_factory(name)
    print(f"--- 用户切换到「{name}」主题 ---")
    print(" ", factory.create_button().render())
    print(" ", factory.create_dialog().render())


apply_theme("light")
apply_theme("dark")
```

运行输出：

```
--- 用户切换到「light」主题 ---
  浅色按钮（白底黑字）
  浅色弹窗（白底黑框）
--- 用户切换到「dark」主题 ---
  深色按钮（黑底白字）
  深色弹窗（黑底白框）
```

关键区别在这：引子里的代码是"按钮一个函数、弹窗一个函数，各判各的主题"；现在是"**一个工厂管一整族**"。想混搭？你得先拆散工厂，而工厂是成套的，拆散它等于自己给自己找麻烦。

---

## 4. Python 特有玩法

### 4.1 模块级函数即工厂：一个模块 = 一个产品族

GoF 时代抽象工厂必须是一堆类。Python 里，**函数是一等公民，模块顶层的函数集合天然就是"产品族"**。真实项目里常常是 `theme_light.py`、`theme_dark.py` 各一个文件，每个文件导出 `create_button` / `create_dialog`。这里用 `types.ModuleType` 模拟两个模块：

```python
import types

# 模拟两个"模块"：每个模块 = 一个产品族，自带一组 create_* 工厂函数
light_theme = types.ModuleType("theme_light")
dark_theme = types.ModuleType("theme_dark")


def install_theme(module, style: str, bg: str, fg: str) -> None:
    """往模块里安装一对工厂函数"""

    def create_button() -> str:
        return f"{style}按钮（{bg}底{fg}字）"

    def create_dialog() -> str:
        return f"{style}弹窗（{bg}底{fg}框）"

    module.create_button = create_button
    module.create_dialog = create_dialog


install_theme(light_theme, "浅色", "白", "黑")
install_theme(dark_theme, "深色", "黑", "白")


def build_page(theme_module) -> str:
    """客户端只认两个函数：create_button 和 create_dialog"""
    return theme_module.create_button() + " | " + theme_module.create_dialog()


print("浅色模块:", build_page(light_theme))
print("深色模块:", build_page(dark_theme))
```

运行输出：

```
浅色模块: 浅色按钮（白底黑字） | 浅色弹窗（白底黑框）
深色模块: 深色按钮（黑底白字） | 深色弹窗（黑底白框）
```

没有抽象基类、没有继承，**"长得像工厂"就是工厂**——这就是 Python 的鸭子类型哲学。

### 4.2 dict 注册表选工厂：把 if/elif 变成查字典

3.3 里 `get_theme_factory` 还是 if/elif。Python 更地道的做法是**注册表**：主题名 → 工厂函数，一张字典搞定。好处是加新主题时旧代码一行都不用改（开闭原则）：

```python
class Button:
    def __init__(self, style: str):
        self.style = style

    def render(self) -> str:
        return f"{self.style}按钮"


class Dialog:
    def __init__(self, style: str):
        self.style = style

    def render(self) -> str:
        return f"{self.style}弹窗"


def make_light_kit():
    return Button("浅色"), Dialog("浅色")


def make_dark_kit():
    return Button("深色"), Dialog("深色")


def make_blue_kit():          # 新主题：只要新增一个函数 + 注册一行
    return Button("蓝色"), Dialog("蓝色")


KITS = {
    "light": make_light_kit,
    "dark": make_dark_kit,
    "blue": make_blue_kit,
}


def apply_theme(name: str) -> None:
    factory = KITS.get(name)
    if factory is None:
        raise KeyError(f"未知主题：{name}")
    button, dialog = factory()
    print(f"「{name}」主题：{button.render()} | {dialog.render()}")


apply_theme("light")
apply_theme("dark")
apply_theme("blue")

try:
    apply_theme("red")
except KeyError as e:
    print("未知主题被拦截:", e)
```

运行输出：

```
「light」主题：浅色按钮 | 浅色弹窗
「dark」主题：深色按钮 | 深色弹窗
「blue」主题：蓝色按钮 | 蓝色弹窗
未知主题被拦截: '未知主题：red'
```

> 注意 `KeyError` 打印出来自带引号，这是 Python 的惯例，别当成 bug。

### 4.3 用 Protocol 代替抽象基类

`typing.Protocol` 是 Python 3.8+ 的"接口"：它描述"要有什么方法"，但**不强制继承**。配合鸭子类型，可以让不继承你任何类的代码直接当产品用：

```python
from typing import Protocol


class Widget(Protocol):
    """协议版抽象产品：只要会 render，就算组件"""

    def render(self) -> str:
        """渲染自己"""


class KitFactory(Protocol):
    """协议版抽象工厂：只要提供 create_button / create_dialog，就算工厂"""

    def create_button(self) -> Widget:
        """造一个按钮"""

    def create_dialog(self) -> Widget:
        """造一个弹窗"""


# 具体实现：不继承任何抽象类，长得像就行
class ModernButton:
    def render(self) -> str:
        return "现代风按钮（玻璃拟态）"


class ModernDialog:
    def render(self) -> str:
        return "现代风弹窗（圆角卡片）"


class RetroButton:
    def render(self) -> str:
        return "复古风按钮（像素边框）"


class RetroDialog:
    def render(self) -> str:
        return "复古风弹窗（CRT 扫描线）"


class ModernKit:
    def create_button(self) -> Widget:
        return ModernButton()

    def create_dialog(self) -> Widget:
        return ModernDialog()


class RetroKit:
    def create_button(self) -> Widget:
        return RetroButton()

    def create_dialog(self) -> Widget:
        return RetroDialog()


def build_page(kit: KitFactory) -> None:
    """客户端只认协议：谁长得像工厂，谁就能上"""
    print(kit.create_button().render())
    print(kit.create_dialog().render())


print("=== 现代风整套 ===")
build_page(ModernKit())
print("=== 复古风整套 ===")
build_page(RetroKit())
```

运行输出：

```
=== 现代风整套 ===
现代风按钮（玻璃拟态）
现代风弹窗（圆角卡片）
=== 复古风整套 ===
复古风按钮（像素边框）
复古风弹窗（CRT 扫描线）
```

Protocol 的价值在大型项目里尤其明显：**接口是"约定"而不是"血统"**，你的产品类不需要知道抽象工厂的存在。

---

## 5. 真实世界中的它

### 标准库：`codecs` 的编码注册表

Python 标准库的 `codecs` 模块，本质上就是一张"编码产品族注册表"：每种编码（utf-8、gbk……）对应一族工具——编码器、解码器、流读写器，成套提供，按名字查表：

```python
import codecs

# codecs.lookup 按名字返回一个 CodecInfo：一族编码工具的"包装盒"
info = codecs.lookup("utf-8")
print("编码族名称:", info.name)

text = "设计模式"
raw, _ = info.encode(text)        # 用这一族的编码器
print("用 utf-8 编码:", raw)
back, _ = info.decode(raw)        # 用这一族的解码器
print("再解码回来:", back)
```

运行输出：

```
编码族名称: utf-8
用 utf-8 编码: b'\xe8\xae\xbe\xe8\xae\xa1\xe6\xa8\xa1\xe5\xbc\x8f'
再解码回来: 设计模式
```

`codecs.lookup("utf-8")` 和 `codecs.lookup("gbk")` 返回的是一整套互不相同的编解码工具——你想"utf-8 编码 + gbk 解码"？可以，但那是你自找的乱码。

### 框架：SQLAlchemy 的 dialect 体系

SQLAlchemy（Python 最流行的 ORM）把"数据库方言"做成了教科书级的抽象工厂：`sqlalchemy.dialects.mysql`、`sqlalchemy.dialects.postgresql` 每个都是独立的方言模块，各自提供**连接器、类型编译器、SQL 编译器、转义规则**。ORM 的业务代码永远只跟抽象的 `Dialect` 打交道，具体落在哪个数据库上，由 `create_engine("mysql://...")` 里的 URL 决定——选方言 = 选工厂。

### 框架：Django 的多数据库后端

Django 的 `django.db.backends` 目录下每个子模块（`mysql`、`postgresql`、`sqlite`）就是一个产品族：`DatabaseWrapper`（连接）、`DatabaseOperations`（操作方言）、`DatabaseFeatures`（特性开关）成套提供。`settings.DATABASES` 里写 `"ENGINE": "django.db.backends.mysql"` 就是"换工厂"。

### GUI 工具包：tkinter / Qt 本身就是抽象工厂

换个角度看：tkinter 的 `Button`、`Entry`、`Toplevel`，Qt 的 `QPushButton`、`QLineEdit`、`QDialog`——这些控件本质上都是"同一族产品"的不同成员，由工具包这个"大工厂"统一生产。你永远不会把 tkinter 的按钮塞进 Qt 的窗口里，因为**它们不属于同一个产品族**。

---

## 6. 优缺点与适用场景

### 优点

- **一致性有保障**：产品族内部永远成套，杜绝混搭；
- **客户端彻底解耦**：只依赖抽象接口，加新实现不用动业务代码；
- **换族成本极低**：换一个工厂对象，全系统换装。

### 缺点

- **加新产品很痛**：每加一个产品，所有具体工厂都要跟着改（开闭原则的代价，见常见误区 1）；
- **类数量膨胀**：产品族 × 产品数量 = 一堆类；
- **抽象层有学习成本**：小项目里这种"绕一圈"的写法显得小题大做。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 跨平台 UI、多主题皮肤 | 只有一种产品要创建（用工厂方法甚至简单工厂） |
| 数据库方言、多后端适配 | 产品之间没有"配套"关系 |
| 需要保证"成套"一致性的场景 | 产品经常单独增删（每加一个就要改所有工厂） |

---

## 7. 与其他模式的关系

- **与工厂方法**：抽象工厂的每个 `create_xxx` 方法，通常就是用工厂方法实现的——**抽象工厂 = 一组工厂方法的集合**。区别一句话：工厂方法管"一个产品"，抽象工厂管"一族产品"。
- **与简单工厂**：简单工厂用一个函数按参数出对象；抽象工厂是"一族工厂函数"的组织形式。很多人把抽象工厂误写成简单工厂（见常见误区 3）。
- **与单例**：工厂对象本身通常做成单例——一个程序里一个平台一个工厂就够，没必要每次 new。第 1 章学的模块级单例正好派上用场。
- **与桥接**：抽象工厂创建"一族产品"，桥接分离"抽象与实现"。两者经常搭配：桥接的"实现部分"由抽象工厂来生产，让两个维度可以各自演化（第 21 章会细讲）。

---

## 8. 常见误区

### 误区 1：加新产品要改所有工厂（开闭原则的代价）

抽象工厂对"产品族"开放（加一个族 = 加一个工厂，旧代码不动），但对"新产品"关闭（加一个产品 = 所有工厂都要改）。Python 的 ABC 会当场抓住没跟上节奏的工厂：

```python
from abc import ABC, abstractmethod


class ThemeFactory(ABC):
    @abstractmethod
    def create_button(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_slider(self) -> str:      # 新需求：加一个"滑块"产品
        raise NotImplementedError


class LightFactory(ThemeFactory):
    def create_button(self) -> str:
        return "浅色按钮"

    # 忘了实现 create_slider——老工厂立刻翻车


try:
    LightFactory()   # 抽象方法没实现，实例化直接报错
except TypeError as e:
    print("老工厂没跟上新需求:", e)
```

运行输出：

```
老工厂没跟上新需求: Can't instantiate abstract class LightFactory without an implementation for abstract method 'create_slider'
```

> 这是抽象工厂的**固有代价**，不是写错了。取舍思路：产品线稳定（不太会加新品类）时用抽象工厂很划算；产品经常增删时，考虑把"产品"也做成可插拔注册的，或者干脆退回工厂方法。

### 误区 2：产品族与产品等级混淆

"产品族"是一套配套产品（浅色按钮 + 浅色弹窗），"产品等级"是同一类产品的不同实现（浅色按钮 vs 深色按钮）。抽象工厂按**族**组织，工厂方法按**等级**组织。很多人一上来就问"我这算抽象工厂还是工厂方法"——先想清楚：**你要换的是"一套"还是"一个"？**

### 误区 3：抽象工厂被简单工厂滥用替代

有人图省事，把抽象工厂写成"一个大函数 + 一堆 if"——这是简单工厂，不是抽象工厂。判断标准很朴素：**你的 if 分支在换"单个产品"还是换"整套产品"？** 如果只是创建单个对象，用简单工厂/工厂方法就够；硬套抽象工厂只会收获一堆用不上的抽象类和翻倍的代码量。

---

## 9. 练习题

### 练习 1：补全一个主题工厂

下面缺了 `DarkThemeFactory`，请补全它，让两套主题都能正确渲染：

```python
# 答案：DarkThemeFactory 与 LightThemeFactory 结构对称
class Button:
    def __init__(self, style: str):
        self.style = style

    def render(self) -> str:
        return f"{self.style}按钮"


class Dialog:
    def __init__(self, style: str):
        self.style = style

    def render(self) -> str:
        return f"{self.style}弹窗"


class ThemeFactory:
    def create_button(self) -> Button:
        raise NotImplementedError

    def create_dialog(self) -> Dialog:
        raise NotImplementedError


class LightThemeFactory(ThemeFactory):
    def create_button(self) -> Button:
        return Button("浅色")

    def create_dialog(self) -> Dialog:
        return Dialog("浅色")


class DarkThemeFactory(ThemeFactory):
    def create_button(self) -> Button:
        return Button("深色")

    def create_dialog(self) -> Dialog:
        return Dialog("深色")


for factory in (LightThemeFactory(), DarkThemeFactory()):
    print(factory.create_button().render(), "|", factory.create_dialog().render())
```

运行输出：

```
浅色按钮 | 浅色弹窗
深色按钮 | 深色弹窗
```

### 练习 2：用注册表替换 if/elif

把下面 `get_factory` 里的 if/elif 改成 dict 注册表，并新增一个 `"blue"` 主题：

```python
# 答案：注册表 + 新增一行即可
class Kit:
    def __init__(self, style: str):
        self.style = style

    def render(self) -> str:
        return f"{self.style}套装"


def make_light() -> Kit:
    return Kit("浅色")


def make_dark() -> Kit:
    return Kit("深色")


def make_blue() -> Kit:          # 新主题：新函数
    return Kit("蓝色")


FACTORIES = {
    "light": make_light,
    "dark": make_dark,
    "blue": make_blue,           # 注册一行
}


def get_factory(name: str):
    if name not in FACTORIES:
        raise KeyError(f"未知主题：{name}")
    return FACTORIES[name]


for name in ("light", "dark", "blue"):
    print(f"{name}: {get_factory(name)().render()}")
```

运行输出：

```
light: 浅色套装
dark: 深色套装
blue: 蓝色套装
```

### 练习 3：用 Protocol 重写抽象工厂

用 `typing.Protocol` 定义"能创建整套控件的工厂"协议，并让两个互不继承的类都满足它：

```python
# 答案：协议只描述行为，不要求继承
from typing import Protocol


class Widget(Protocol):
    def render(self) -> str:
        """渲染自己"""


class WidgetKit(Protocol):
    def create_button(self) -> Widget:
        """造按钮"""

    def create_dialog(self) -> Widget:
        """造弹窗"""


class RoundButton:
    def render(self) -> str:
        return "圆角按钮"


class RoundDialog:
    def render(self) -> str:
        return "圆角弹窗"


class SquareButton:
    def render(self) -> str:
        return "方形按钮"


class SquareDialog:
    def render(self) -> str:
        return "方形弹窗"


class RoundKit:
    def create_button(self) -> Widget:
        return RoundButton()

    def create_dialog(self) -> Widget:
        return RoundDialog()


class SquareKit:
    def create_button(self) -> Widget:
        return SquareButton()

    def create_dialog(self) -> Widget:
        return SquareDialog()


def demo(kit: WidgetKit) -> None:
    print(kit.create_button().render(), "|", kit.create_dialog().render())


demo(RoundKit())
demo(SquareKit())
```

运行输出：

```
圆角按钮 | 圆角弹窗
方形按钮 | 方形弹窗
```

---

## 10. 小结与口诀

> **口诀：一套产品，成套生产；换工厂，换全家；想加新品，全厂加班。**

抽象工厂是创建型模式里"规模最大"的一个：它管的不再是一个对象，而是一族对象。三个记忆点：

1. **成套**：工厂按"产品族"组织，混搭是结构上不允许的；
2. **换装**：换产品族 = 换一个工厂对象，业务代码一行不改；
3. **代价**：加新产品要动所有工厂，产品线不稳定时慎用。

下一章，我们把目光从"怎么创建对象"转向"怎么组织行为"——**命令模式**：把"做一件事"打包成对象，可排队、可撤销、可记录。

---

*本章金句：抽象工厂保证"一家人整整齐齐"——产品可以整套换，套系内部不许乱搭。*
