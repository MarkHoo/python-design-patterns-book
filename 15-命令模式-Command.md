# 第 15 章 命令模式（Command）

> **一句话总结**：把"做一件事"打包成对象：可排队、可撤销、可记录。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 行为型 | ★★★☆☆ | ★★★☆☆ |

---

## 1. 引子：先讲个故事

你去餐厅吃饭。服务员不会直接冲进后厨喊"红烧肉！"，而是先在你的**点单小票**上记一笔，然后把小票按顺序贴在厨房窗口。后厨照着小票一道道做。小票有什么用？它可以排队（一桌一桌来）、可以退单（没做的划掉）、可以留底（月底对账）。📋

如果服务员直接扯着嗓子喊，喊完就完了——菜没做要重喊，做错了没法追溯，客人改主意也没法撤销。程序里的"按钮"就是服务员：如果按钮的点击逻辑**直接调用**业务代码，动作执行完就"蒸发"了，撤销、排队、录制宏统统没戏：

```python
# 引子：没有命令的世界——按钮和业务逻辑焊死在一起
class TextEditor:
    def __init__(self):
        self.text = ""

    def insert(self, text: str) -> None:
        self.text += text

    def delete(self, count: int) -> None:
        self.text = self.text[:-count]


class Toolbar:
    """工具栏按钮：直接调用业务对象的方法"""

    def __init__(self, editor: TextEditor):
        self.editor = editor

    def on_insert_click(self, text: str) -> None:
        # 想撤销？想记录宏？没门——动作执行完就消失了
        self.editor.insert(text)

    def on_delete_click(self, count: int) -> None:
        self.editor.delete(count)


editor = TextEditor()
toolbar = Toolbar(editor)
toolbar.on_insert_click("你好")
toolbar.on_insert_click("世界")
print("当前文本:", editor.text)
toolbar.on_delete_click(2)
print("删了 2 个字符后:", editor.text)
print("用户手滑想撤销？动作已经'蒸发'，无从撤起")
```

运行输出：

```
当前文本: 你好世界
删了 2 个字符后: 你好
用户手滑想撤销？动作已经'蒸发'，无从撤起
```

这段代码有三个毛病：

1. **按钮直接依赖编辑器**：换个编辑器，按钮全部要改；
2. **动作不可追溯**：执行完就没了，撤销、重做无从谈起；
3. **无法排队和录制**：想"把这串操作录下来重放"，没有一个可操作的对象。

**命令模式**就是那张"小票"：把"做一件事"（连同参数）打包成一个对象，于是它就能被排队、被撤销、被记录。

---

## 2. 模式登场

### 定义

> **命令模式**：把请求封装成对象，从而可以用不同的请求对客户端参数化、对请求排队或记录日志，以及支持可撤销的操作。

### 解决的问题

1. **解耦调用者与接收者**：按钮不知道谁在干活，干活的人不知道谁按了按钮；
2. **动作可记录**：动作变成了对象，可以排队、可以撤销、可以录制成宏；
3. **延迟执行**：命令可以先创建、后执行（甚至永不执行，比如"取消"）。

### 结构

```
   ┌────────────┐                 ┌───────────────────┐
   │  Invoker   │────────────────▶│   Command（接口）   │
   │ （调用者）   │  持有并调用命令   ├───────────────────┤
   │            │                 │ + execute()       │
   └────────────┘                 │ + undo()          │
                                  └─────────▲─────────┘
                                            │ 实现
                                  ┌─────────┴─────────┐
                                  │ ConcreteCommand    │
                                  │ （具体命令）         │──────▶┌────────────┐
                                  │  持有接收者+参数     │       │ Receiver   │
                                  └───────────────────┘       │ （接收者）   │
                                                               └────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **Command** | 抽象接口：声明 `execute()`（执行）和 `undo()`（撤销） |
| **ConcreteCommand** | 具体命令：绑定接收者和参数，`execute` 时调用接收者 |
| **Receiver** | 接收者：真正干活的业务对象（编辑器、后厨、灯） |
| **Invoker** | 调用者：持有命令，决定何时执行/撤销（按钮、服务员、遥控器） |
| **Client** | 客户端：创建具体命令并交给调用者 |

---

## 3. Python 实现

### 3.1 经典版：编辑器撤销 / 重做

文本编辑器的撤销/重做是命令模式最经典的场景。关键是：**命令执行时把自己记住的"反操作"存好**——插入命令记住删掉它，删除命令记住补回来：

```python
class TextEditor:
    """接收者：真正干活的文本编辑器"""

    def __init__(self):
        self.text = ""

    def insert(self, text: str) -> None:
        self.text += text

    def delete(self, count: int) -> None:
        self.text = self.text[:-count]

    def __repr__(self):
        return f"<编辑器 文本={self.text!r}>"


class Command:
    """命令接口：执行 + 撤销"""

    def execute(self) -> None:
        raise NotImplementedError

    def undo(self) -> None:
        raise NotImplementedError


class InsertCommand(Command):
    """插入命令：撤销 = 把自己插进去的删掉"""

    def __init__(self, editor: TextEditor, text: str):
        self.editor = editor
        self.text = text

    def execute(self) -> None:
        self.editor.insert(self.text)

    def undo(self) -> None:
        self.editor.delete(len(self.text))


class DeleteCommand(Command):
    """删除命令：执行前先记下删掉的内容，撤销 = 补回去"""

    def __init__(self, editor: TextEditor, count: int):
        self.editor = editor
        self.count = count
        self.deleted = ""       # 执行时才记录

    def execute(self) -> None:
        self.deleted = self.editor.text[-self.count:]
        self.editor.delete(self.count)

    def undo(self) -> None:
        self.editor.insert(self.deleted)


class CommandHistory:
    """调用者：管理命令的撤销栈和重做栈"""

    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()        # 新操作会清空重做栈

    def undo(self) -> None:
        if not self._undo_stack:
            print("没有可以撤销的操作")
            return
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self) -> None:
        if not self._redo_stack:
            print("没有可以重做的操作")
            return
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)


editor = TextEditor()
history = CommandHistory()

history.execute(InsertCommand(editor, "你好"))
history.execute(InsertCommand(editor, "世界"))
print("输入两段文字后:", editor)

history.execute(DeleteCommand(editor, 3))
print("删除 3 个字符后:", editor)

history.undo()
print("撤销删除后:", editor)

history.undo()
print("再撤销一次后:", editor)

history.redo()
print("重做一次后:", editor)
```

运行输出：

```
输入两段文字后: <编辑器 文本='你好世界'>
删除 3 个字符后: <编辑器 文本='你'>
撤销删除后: <编辑器 文本='你好世界'>
再撤销一次后: <编辑器 文本='你好'>
重做一次后: <编辑器 文本='你好世界'>
```

注意 `DeleteCommand`：它必须在 `execute` 时把"删掉的文本"先存起来，否则 `undo` 无从恢复——这就是命令模式与备忘录（第 20 章）经常配合的原因。

### 3.2 任务队列版：餐厅小票排队

命令对象放进队列，就是"任务队列"；还支持**退单**（取消还没执行的任务）：

```python
from collections import deque


class Kitchen:
    """接收者：后厨"""

    def __init__(self):
        self.dishes = []

    def cook(self, dish: str) -> None:
        self.dishes.append(dish)
        print(f"后厨做好：{dish}（当前共 {len(self.dishes)} 道）")


class OrderCommand:
    """具体命令：一张点菜单"""

    def __init__(self, kitchen: Kitchen, dish: str):
        self.kitchen = kitchen
        self.dish = dish

    def execute(self) -> None:
        self.kitchen.cook(self.dish)


class Waiter:
    """调用者：服务员，负责记单、排队、退单、传菜"""

    def __init__(self, kitchen: Kitchen):
        self.kitchen = kitchen
        self.queue = deque()        # 未执行的点单，按顺序排队

    def take_order(self, dish: str) -> None:
        self.queue.append(OrderCommand(self.kitchen, dish))
        print(f"服务员记下点单：{dish}")

    def cancel_order(self, dish: str) -> None:
        """退单：从队列里移除还没做的菜"""
        before = len(self.queue)
        self.queue = deque(c for c in self.queue if c.dish != dish)
        removed = before - len(self.queue)
        print(f"退掉 {removed} 份还没做的「{dish}」")

    def send_to_kitchen(self) -> None:
        """把队列里所有单子一次性传给后厨"""
        print("--- 传单给后厨 ---")
        while self.queue:
            self.queue.popleft().execute()


kitchen = Kitchen()
waiter = Waiter(kitchen)
waiter.take_order("红烧肉")
waiter.take_order("清蒸鱼")
waiter.take_order("红烧肉")
waiter.cancel_order("红烧肉")        # 客人改主意了，退单
waiter.send_to_kitchen()
```

运行输出：

```
服务员记下点单：红烧肉
服务员记下点单：清蒸鱼
服务员记下点单：红烧肉
退掉 2 份还没做的「红烧肉」
--- 传单给后厨 ---
后厨做好：清蒸鱼（当前共 1 道）
```

### 3.3 宏录制版：一串命令打包成一个命令

"宏"就是命令的数组：把若干命令合成一个 `MacroCommand`，整体执行、整体撤销：

```python
class Light:
    """接收者：灯"""

    def __init__(self):
        self.is_on = False

    def switch(self) -> None:
        self.is_on = not self.is_on
        print(f"灯现在是{'开' if self.is_on else '关'}的")


class LightCommand:
    """具体命令：按一下开关"""

    def __init__(self, light: Light):
        self.light = light

    def execute(self) -> None:
        self.light.switch()

    def undo(self) -> None:
        self.light.switch()        # 灯的撤销 = 再按一下


class MacroCommand:
    """宏命令：把一串命令打包成一个命令"""

    def __init__(self, commands):
        self.commands = commands

    def execute(self) -> None:
        print("== 宏开始执行 ==")
        for cmd in self.commands:
            cmd.execute()

    def undo(self) -> None:
        print("== 宏整体撤销（逆序） ==")
        for cmd in reversed(self.commands):
            cmd.undo()


light = Light()
macro = MacroCommand([
    LightCommand(light),
    LightCommand(light),
    LightCommand(light),
])
macro.execute()
print("执行 3 次开关后，灯是开的:", light.is_on)
macro.undo()
print("整体撤销后，灯是关的:", light.is_on)
```

运行输出：

```
== 宏开始执行 ==
灯现在是开的
灯现在是关的
灯现在是开的
执行 3 次开关后，灯是开的: True
== 宏整体撤销（逆序） ==
灯现在是关的
灯现在是开的
灯现在是关的
整体撤销后，灯是关的: False
```

---

## 4. Python 特有玩法

### 4.1 函数 / `partial` 直接当命令

GoF 时代每个命令都要写一个类。Python 里**函数就是命令**——`functools.partial` 可以把"函数 + 参数"预先打包好，点击时直接调用，连类都省了：

```python
import functools


def save_file(path: str, content: str) -> None:
    """接收者上的动作：保存文件"""
    print(f"保存文件：{path}，内容 {len(content)} 个字符")


# partial 把"函数 + 参数"打包成一个可调用对象——这就是命令！
save_report = functools.partial(save_file, "report.txt", "本月营收 100 万")
save_backup = functools.partial(save_file, "backup.db", "数据库快照")


class Button:
    """调用者：按钮只负责在点击时调用命令"""

    def __init__(self, label: str, command):
        self.label = label
        self.command = command

    def click(self) -> None:
        print(f"[点击 {self.label}]")
        self.command()


Button("保存报表", save_report).click()
Button("备份数据库", save_backup).click()
```

运行输出：

```
[点击 保存报表]
保存文件：report.txt，内容 10 个字符
[点击 备份数据库]
保存文件：backup.db，内容 5 个字符
```

### 4.2 `__call__` 对象当命令：命令即函数

想让命令对象既能"当函数调"，又能携带自己的状态？实现 `__call__` 即可——调用者眼里它就是一个函数，但它暗地里是个对象：

```python
class Logger:
    """接收者：操作日志"""

    def __init__(self):
        self.entries = []

    def add(self, message: str) -> None:
        self.entries.append(message)
        print(f"记录日志：{message}")


class LogCommand:
    """__call__ 版命令：实例本身就能当函数调用"""

    def __init__(self, logger: Logger, message: str):
        self.logger = logger
        self.message = message

    def __call__(self) -> None:
        self.logger.add(self.message)


logger = Logger()
commands = [LogCommand(logger, f"第 {i} 步操作") for i in range(1, 4)]
for cmd in commands:          # 命令排队执行
    cmd()                     # 直接当函数调用

print("日志条数:", len(logger.entries))
```

运行输出：

```
记录日志：第 1 步操作
记录日志：第 2 步操作
记录日志：第 3 步操作
日志条数: 3
```

### 4.3 函数式命令 + 撤销栈：闭包打包"执行/撤销"一对

最 Pythonic 的撤销玩法：一个工厂函数返回 `(执行函数, 撤销函数)` 一对闭包，撤销栈里存函数而不是对象：

```python
def make_commands(editor, text: str):
    """函数式命令：把"执行"和"撤销"打包成一对函数"""
    def do() -> None:
        editor.text += text

    def undo() -> None:
        editor.text = editor.text[:-len(text)]

    return do, undo


class Editor:
    def __init__(self):
        self.text = ""


editor = Editor()
undo_stack = []

do1, undo1 = make_commands(editor, "设计")
do2, undo2 = make_commands(editor, "模式")

do1()
undo_stack.append(undo1)
do2()
undo_stack.append(undo2)
print("执行两条命令后:", repr(editor.text))

undo_stack.pop()()
print("撤销一次后:", repr(editor.text))

undo_stack.pop()()
print("再撤销一次后:", repr(editor.text))
```

运行输出：

```
执行两条命令后: '设计模式'
撤销一次后: '设计'
再撤销一次后: ''
```

---

## 5. 真实世界中的它

### 标准库：`concurrent.futures` 的"任务对象"

`concurrent.futures` 的 `submit` 把"函数 + 参数"打包成一个 **Future 任务对象**提交给线程池——这就是命令思想：动作先打包、后执行、结果可查询：

```python
import concurrent.futures


def upload(url: str, data: str) -> str:
    """模拟一个耗时的上传任务"""
    return f"已上传 {data} 到 {url}"


# 把"函数 + 参数"打包成任务对象提交——每个任务就是一个命令
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures = [
        pool.submit(upload, "http://cdn.example.com/a", "图片A"),
        pool.submit(upload, "http://cdn.example.com/b", "图片B"),
    ]
    for f in futures:             # 按提交顺序取结果
        print(f.result())
```

运行输出：

```
已上传 图片A 到 http://cdn.example.com/a
已上传 图片B 到 http://cdn.example.com/b
```

### GUI：tkinter 的 `command` 参数

tkinter 按钮的 `command=` 参数就是命令思想的直接体现：`Button(text="保存", command=save_action)`——按钮（Invoker）不知道 `save_action` 是谁，只知道"点击时调用它"。Qt 更进一步，`QUndoCommand` 是完整的命令模式实现：每个命令必须实现 `redo()` 和 `undo()`，配合 `QUndoStack` 管理撤销/重做，还支持把多个命令压成"一个可撤销操作"——这正是 Qt 文档编辑器撤销功能的基石。

### 框架：任务调度与宏

Celery、APScheduler 这类任务框架的"任务"本质上都是命令对象：任务 = 函数 + 参数 + 执行策略，可以被排队、被重试、被记录。编辑器里的"宏录制"（如 Vim 的 `q` 录制）则是把一串命令录下来重放——3.3 的 `MacroCommand` 就是它的原型。

---

## 6. 优缺点与适用场景

### 优点

- **彻底解耦**：调用者与接收者互不认识，中间只隔一个命令对象；
- **可撤销/重做**：动作被记录成对象，可以回放、可以倒放；
- **可排队、可延迟**：命令可以先创建，后执行，甚至不执行；
- **可组合**：命令可以打包成宏命令。

### 缺点

- **类数量膨胀**：每个动作一个命令类（Python 里可用函数/partial 缓解）；
- **过度包装**：一次性的简单调用被命令化，纯属自找麻烦；
- **撤销本身很难**："恢复状态"往往需要命令 + 备忘录配合，逻辑并不简单。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 编辑器撤销/重做、快捷键系统 | 一次性的简单动作（直接调用即可） |
| 任务队列、延迟调度 | 动作之间没有"记录/回放"需求 |
| 宏录制、按钮与动作解耦 | 团队没人愿意维护命令历史时 |

---

## 7. 与其他模式的关系

- **与策略**：两者结构相似（一个接口多个实现），但意图不同——命令封装"动作"（延迟执行、可撤销），策略封装"算法"（运行时替换）。命令强调"什么时候做"，策略强调"怎么做"。
- **与备忘录**：命令负责"记住做了什么"，备忘录负责"记住当时的状态"。撤销要恢复对象状态时，两者经常配对（第 20 章）。
- **与责任链**：命令可以被传递——某个调用者处理不了，就传给下一个（第 13 章）；请求/命令沿着链走，直到有人接单。
- **与组合**：宏命令 `MacroCommand` 本身就是组合模式的应用——命令套命令，构成树（第 17 章）。

---

## 8. 常见误区

### 误区 1：命令对象里塞了太多业务逻辑

命令的职责是"**转发**"，不是"实现"。把业务逻辑复制进命令类，等于同一个逻辑写两遍，改一处忘另一处：

```python
class BankAccount:
    """接收者：业务逻辑应该住在这里"""

    def __init__(self, balance: float):
        self.balance = balance

    def withdraw(self, amount: float) -> None:
        if self.balance < amount:
            raise ValueError(f"余额不足（余额 {self.balance}）")
        self.balance -= amount
        print(f"扣款 {amount}，余额 {self.balance}")


# 反面教材：命令复制了一份业务逻辑，以后改规则要改两处
class BadPayCommand:
    def __init__(self, account: BankAccount, amount: float):
        self.account = account
        self.amount = amount

    def execute(self) -> None:
        if self.account.balance < self.amount:      # ← 业务逻辑复制粘贴
            raise ValueError("余额不足")
        self.account.balance -= self.amount
        print(f"扣款 {self.amount}，余额 {self.account.balance}")


# 正确姿势：命令只做"转发"
class GoodPayCommand:
    def __init__(self, account: BankAccount, amount: float):
        self.account = account
        self.amount = amount

    def execute(self) -> None:
        self.account.withdraw(self.amount)          # ← 只转发，不实现


account = BankAccount(100)
BadPayCommand(account, 30).execute()
GoodPayCommand(account, 20).execute()
```

运行输出：

```
扣款 30，余额 70
扣款 20，余额 50
```

### 误区 2：撤销只记了动作，没记状态

"撤销删除"要求命令记得**被删掉的内容**。如果执行时不留痕，撤销时就是无米之炊：

```python
# 反面教材：撤销命令没保存"被删了什么"
class DeleteWithoutMemory:
    def __init__(self, editor, count: int):
        self.editor = editor
        self.count = count

    def execute(self) -> None:
        self.editor.text = self.editor.text[:-self.count]

    def undo(self) -> None:
        raise RuntimeError("我不知道刚才删了什么！")


class Editor:
    def __init__(self):
        self.text = "设计模式"


editor = Editor()
cmd = DeleteWithoutMemory(editor, 2)
cmd.execute()
print("删除后:", editor.text)
try:
    cmd.undo()
except RuntimeError as e:
    print("撤销失败:", e)
```

运行输出：

```
删除后: 设计
撤销失败: 我不知道刚才删了什么！
```

> 正确做法：`execute` 时把被删的文本存起来（见 3.1 的 `DeleteCommand`），或者配合备忘录模式在操作前存一份快照。

### 误区 3：滥用命令导致类爆炸

每个动作都写一个命令类，项目会变成"命令类批发市场"。Python 里**函数、`partial`、`__call__` 对象**已经覆盖了绝大多数场景，先问自己"这里真的需要一个类吗"：

```python
import functools


def toggle(light) -> None:
    light.is_on = not light.is_on
    print(f"灯现在是{'开' if light.is_on else '关'}的")


class Light:
    def __init__(self):
        self.is_on = False


light = Light()
turn_on = functools.partial(toggle, light)   # 打包好的"命令"
for _ in range(3):
    turn_on()
```

运行输出：

```
灯现在是开的
灯现在是关的
灯现在是开的
```

---

## 9. 练习题

### 练习 1：给电视遥控器加命令

实现 `VolumeUpCommand`（含撤销），并用遥控器连续按 3 次、撤销 2 次：

```python
# 答案：完整的命令模式小例子——电视机音量遥控
class TV:
    """接收者：电视机"""

    def __init__(self):
        self.volume = 10

    def volume_up(self) -> None:
        self.volume += 1

    def volume_down(self) -> None:
        self.volume -= 1


class VolumeUpCommand:
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self) -> None:
        self.tv.volume_up()

    def undo(self) -> None:
        self.tv.volume_down()


class RemoteControl:
    """调用者：遥控器，记录按键历史"""

    def __init__(self):
        self._history = []

    def press(self, command) -> None:
        command.execute()
        self._history.append(command)
        print(f"按了一下，音量现在是 {command.tv.volume}")

    def press_undo(self) -> None:
        if not self._history:
            print("没有可撤销的按键")
            return
        command = self._history.pop()
        command.undo()
        print(f"撤销一次，音量现在是 {command.tv.volume}")


tv = TV()
remote = RemoteControl()
remote.press(VolumeUpCommand(tv))
remote.press(VolumeUpCommand(tv))
remote.press(VolumeUpCommand(tv))
remote.press_undo()
remote.press_undo()
```

运行输出：

```
按了一下，音量现在是 11
按了一下，音量现在是 12
按了一下，音量现在是 13
撤销一次，音量现在是 12
撤销一次，音量现在是 11
```

### 练习 2：用 `partial` 造三个"发邮件"命令

一个发送函数 + 三个 `partial` 打包，配三个按钮：

```python
# 答案：partial 打包"函数 + 参数"，三个按钮共享一个发送函数
import functools


def send_email(to: str, subject: str) -> None:
    print(f"发送邮件 → {to}，主题：{subject}")


send_to_boss = functools.partial(send_email, "boss@company.com", "季度总结")
send_to_team = functools.partial(send_email, "team@company.com", "周报")
send_to_customer = functools.partial(send_email, "customer@example.com", "发票")


class Button:
    def __init__(self, label: str, command):
        self.label = label
        self.command = command

    def click(self) -> None:
        print(f"[点击 {self.label}]")
        self.command()


Button("发给老板", send_to_boss).click()
Button("发给团队", send_to_team).click()
Button("发给客户", send_to_customer).click()
```

运行输出：

```
[点击 发给老板]
发送邮件 → boss@company.com，主题：季度总结
[点击 发给团队]
发送邮件 → team@company.com，主题：周报
[点击 发给客户]
发送邮件 → customer@example.com，主题：发票
```

### 练习 3：实现一个可整体撤销的宏

把"插入两段文字"录成宏，整体执行后整体撤销：

```python
# 答案：宏命令——录一串命令，整体执行、整体撤销
class TextEditor:
    def __init__(self):
        self.text = ""

    def insert(self, text: str) -> None:
        self.text += text
        print(f"插入「{text}」，当前：{self.text}")

    def delete(self, count: int) -> None:
        self.text = self.text[:-count]
        print(f"删除 {count} 个字符，当前：{self.text}")


class InsertCommand:
    def __init__(self, editor: TextEditor, text: str):
        self.editor = editor
        self.text = text

    def execute(self) -> None:
        self.editor.insert(self.text)

    def undo(self) -> None:
        self.editor.delete(len(self.text))


class Macro:
    def __init__(self, commands):
        self.commands = commands

    def execute(self) -> None:
        for c in self.commands:
            c.execute()

    def undo(self) -> None:
        for c in reversed(self.commands):
            c.undo()


editor = TextEditor()
macro = Macro([
    InsertCommand(editor, "第一段"),
    InsertCommand(editor, "第二段"),
])
print("--- 执行宏 ---")
macro.execute()
print("--- 撤销宏 ---")
macro.undo()
print("最终文本:", repr(editor.text))
```

运行输出：

```
--- 执行宏 ---
插入「第一段」，当前：第一段
插入「第二段」，当前：第一段第二段
--- 撤销宏 ---
删除 3 个字符，当前：第一段
删除 3 个字符，当前：
最终文本: ''
```

---

## 10. 小结与口诀

> **口诀：动作打包成对象，排队撤销随你便；函数 partial 顶类用，别把业务塞里面。**

命令模式的核心就一句话：**把"做"变成"一个东西"**。动作一旦变成对象，排队、撤销、录制、延迟执行全都变得顺理成章。三个记忆点：

1. **三件套**：命令（做什么）、调用者（何时做）、接收者（怎么做），各管各的；
2. **可撤销的前提**：命令执行时要把"反操作所需的信息"先存好；
3. **别过度设计**：Python 里函数、`partial`、`__call__` 往往就够了。

下一章，我们来看一个"行为会随着状态改变"的模式——**状态模式**：状态变了，行为就变。

---

*本章金句：命令模式把"做"变成"物"——动作一旦打包成对象，就能排队、能撤销、能留档。*
