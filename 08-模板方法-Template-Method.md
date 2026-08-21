# 第 8 章 模板方法（Template Method）

> **一句话总结**：流程骨架固定，步骤细节交给子类。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 行为型 | ★★☆☆☆ | ★★★★☆ |

---

## 1. 引子：先讲个故事

做菜的流程其实很固定：**备菜 → 烹饪 → 装盘**。不管你是做红烧肉还是清炒时蔬，这个骨架都一样，变的只是"切什么、怎么炒、摆什么盘"。聪明的厨师会先把流程定好，每一道菜只换"配料"——而不是每道菜都从零开始想"今天要不要先备菜"。

程序里也有同样的故事。你的项目要支持从不同数据源导入数据，CSV 和 JSON 各写了一套导入代码，你复制粘贴了"读取 → 清洗 → 入库"的流程，然后噩梦开始了：

```python
# 引子：两段 90% 相同的代码——复制粘贴的代价
import json
import os
import tempfile


def import_csv(path):
    print("1. 读取 CSV 文件")
    with open(path, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    print(f"2. 清洗：去掉空行，剩 {len(lines)} 行")
    print("3. 入库：写入数据库")
    return len(lines)


def import_json(path):
    print("1. 读取 JSON 文件")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    print(f"2. 清洗：校验字段，剩 {len(data)} 条")
    print("3. 入库：写入数据库")
    return len(data)


with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
    f.write("name,age\n小明,18\n\n小红,20\n")
    csv_path = f.name
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    json.dump([{"name": "小明"}, {"name": "小红"}], f)
    json_path = f.name

try:
    print("CSV 导入：", import_csv(csv_path), "行")
    print("JSON 导入：", import_json(json_path), "条")
finally:
    os.unlink(csv_path)
    os.unlink(json_path)
```

运行输出：

```
1. 读取 CSV 文件
2. 清洗：去掉空行，剩 3 行
3. 入库：写入数据库
CSV 导入： 3 行
1. 读取 JSON 文件
2. 清洗：校验字段，剩 2 条
3. 入库：写入数据库
JSON 导入： 2 条
```

问题很明显：两段代码的**骨架一模一样**，只有"怎么读、怎么清洗"不同。今天加一个 XML 导入，你再复制一遍；明天改流程（比如入库前先做校验），三个函数都要改——改漏一个，线上就悄悄出 bug。

**模板方法模式**就是来收拾这种局面的：把流程骨架写死在基类里，把"会变的步骤"声明成抽象方法，让子类各填各的。

---

## 2. 模式登场

### 定义

> **模板方法模式**：在基类里定义一个算法的骨架（模板方法），把其中一些步骤延迟到子类实现。子类可以重定义某些步骤，但不能改变算法的结构。

### 核心思想：好莱坞原则

> **"别打电话给我们，我们会打给你。"**（Don't call us, we'll call you）

基类把流程编排好了，子类不要去主动调用流程，只要实现自己的步骤，等着基类在合适的时机"打给你"。**控制权在基类手里，这就是"控制反转"的雏形。**

### 两类"步骤"

| 步骤类型 | 说明 | 子类怎么办 |
|---------|------|-----------|
| **抽象方法** | 骨架里的关键步骤，没有默认实现 | 必须实现 |
| **钩子方法（hook）** | 骨架里的可选环节，有默认实现 | 可选覆盖，不覆盖就用默认行为 |

### 结构

```
        ┌────────────────────────────────┐
        │         AbstractClass          │
        ├────────────────────────────────┤
        │ + template_method()   ← 骨架固定 │
        │ + primitive_op1()     ← 抽象    │
        │ + primitive_op2()     ← 抽象    │
        │ + hook()              ← 钩子    │
        └──────────────┬─────────────────┘
                       ▲
          ┌────────────┴────────────┐
          ▼                         ▼
┌───────────────────┐   ┌───────────────────┐
│  ConcreteClassA   │   │  ConcreteClassB   │
│ + primitive_op1() │   │ + primitive_op1() │
│ + primitive_op2() │   │ + primitive_op2() │
│ + hook()（可选覆盖）│   │ （什么都不用改）     │
└───────────────────┘   └───────────────────┘
```

### 角色

| 角色 | 说明 |
|------|------|
| **抽象类（AbstractClass）** | 定义模板方法（骨架）和抽象步骤 |
| **具体类（ConcreteClass）** | 实现抽象步骤，可选择性覆盖钩子 |
| **模板方法** | 基类里编排流程的方法，通常不可覆盖 |

---

## 3. Python 实现

### 3.1 经典版：数据导入流程

把引子的复制粘贴收敛成一个抽象基类：骨架 `import_data` 固定，三个抽象方法下放：

```python
import abc
import json
import os
import tempfile


class DataImporter(abc.ABC):
    """抽象类：固定了导入流程的骨架"""

    def import_data(self, source: str) -> int:
        """模板方法：流程骨架固定，子类不能改"""
        raw = self.read(source)           # 步骤 1：读取
        cleaned = self.clean(raw)         # 步骤 2：清洗
        count = self.load(cleaned)        # 步骤 3：入库
        if self.should_verify():          # 钩子：默认不校验
            self.verify(count)
        return count

    @abc.abstractmethod
    def read(self, source: str):
        """抽象方法：必须实现——怎么读"""
        pass

    @abc.abstractmethod
    def clean(self, raw) -> list:
        """抽象方法：必须实现——怎么清洗"""
        pass

    @abc.abstractmethod
    def load(self, cleaned: list) -> int:
        """抽象方法：必须实现——怎么入库"""
        pass

    def should_verify(self) -> bool:
        """钩子方法：有默认实现，子类可选覆盖"""
        return False

    def verify(self, count: int) -> None:
        print(f"  校验：{count} 条数据已入库")


class CsvImporter(DataImporter):
    def read(self, source: str):
        print("  读取：CSV 文件")
        with open(source, encoding="utf-8") as f:
            return [ln.strip() for ln in f if ln.strip()]

    def clean(self, raw) -> list:
        print(f"  清洗：去掉注释行，剩 {len(raw)} 行")
        return [ln for ln in raw if not ln.startswith("#")]

    def load(self, cleaned: list) -> int:
        print(f"  入库：写入 {len(cleaned)} 行")
        return len(cleaned)


class JsonImporter(DataImporter):
    def read(self, source: str):
        print("  读取：JSON 文件")
        with open(source, encoding="utf-8") as f:
            return json.load(f)

    def clean(self, raw) -> list:
        print(f"  清洗：过滤无 name 字段的记录，剩 {len(raw)} 条")
        return [item for item in raw if item.get("name")]

    def load(self, cleaned: list) -> int:
        print(f"  入库：写入 {len(cleaned)} 条记录")
        return len(cleaned)

    def should_verify(self) -> bool:
        """覆盖钩子：JSON 导入后做校验"""
        return True


with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
    f.write("name,age\n# 注释行\n小明,18\n小红,20\n")
    csv_path = f.name
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    json.dump([{"name": "小明"}, {"age": 99}], f)
    json_path = f.name

try:
    print("== CSV 导入 ==")
    CsvImporter().import_data(csv_path)
    print("== JSON 导入 ==")
    JsonImporter().import_data(json_path)
finally:
    os.unlink(csv_path)
    os.unlink(json_path)
```

运行输出：

```
== CSV 导入 ==
  读取：CSV 文件
  清洗：去掉注释行，剩 4 行
  入库：写入 3 行
== JSON 导入 ==
  读取：JSON 文件
  清洗：过滤无 name 字段的记录，剩 2 条
  入库：写入 1 条记录
  校验：1 条数据已入库
```

以后加 XML 导入？写一个 `XmlImporter` 实现三个抽象方法即可，**流程骨架一行不用动**。注意 `JsonImporter` 通过覆盖钩子 `should_verify` 给自己"加戏"——这就是钩子的意义：默认行为之外，给子类留一扇窗。

### 3.2 变体：游戏关卡

游戏关卡的流程同样固定：**开局 → 出怪 → 战斗 → 结算**。不同关卡换怪物、换战斗方式，个别关卡还有"奖励关"这种加餐（钩子）：

```python
import abc


class GameLevel(abc.ABC):
    """抽象关卡：开局 → 打怪 → 结算 的骨架固定"""

    def play(self) -> None:
        """模板方法：整关的流程，子类不能改"""
        self.on_start()
        self.spawn_enemies()
        self.battle()
        self.on_clear()
        if self.bonus_round():            # 钩子：默认没有奖励关
            self.play_bonus()

    def on_start(self) -> None:
        print("关卡开始，加载地图……")

    @abc.abstractmethod
    def spawn_enemies(self) -> None:
        pass

    @abc.abstractmethod
    def battle(self) -> None:
        pass

    def on_clear(self) -> None:
        print("敌人清空，本关通过！")

    def bonus_round(self) -> bool:
        """钩子：默认没有奖励关"""
        return False

    def play_bonus(self) -> None:
        print("进入奖励关！")


class ForestLevel(GameLevel):
    def spawn_enemies(self) -> None:
        print("出现 5 只史莱姆")

    def battle(self) -> None:
        print("主角挥剑，击败史莱姆")


class BossLevel(GameLevel):
    def spawn_enemies(self) -> None:
        print("出现最终 Boss：暗影魔王")

    def battle(self) -> None:
        print("Boss 战！消耗三个血瓶险胜")

    def bonus_round(self) -> bool:
        return True   # 覆盖钩子：Boss 关有奖励关

    def play_bonus(self) -> None:
        print("奖励关：连开三个宝箱！")


print("===== 第 1 关 =====")
ForestLevel().play()
print("===== 最终关 =====")
BossLevel().play()
```

运行输出：

```
===== 第 1 关 =====
关卡开始，加载地图……
出现 5 只史莱姆
主角挥剑，击败史莱姆
敌人清空，本关通过！
===== 最终关 =====
关卡开始，加载地图……
出现最终 Boss：暗影魔王
Boss 战！消耗三个血瓶险胜
敌人清空，本关通过！
奖励关：连开三个宝箱！
```

`ForestLevel` 只实现了两个抽象方法就"通关"了；`BossLevel` 多覆盖了一个钩子，就有了奖励关。**想做新关卡？照着抽象方法填就行，玩法骨架由基类兜底。**

### 3.3 钩子的妙用：报表生成器

钩子最常见的用法是"**按条件决定要不要执行某一步**"。报表生成器里，数据够多才配图表，够少就别画：

```python
import abc


class ReportGenerator(abc.ABC):
    """抽象报表生成器：骨架固定，细节下放"""

    def generate(self, title: str, data: dict) -> str:
        """模板方法：生成完整报告"""
        parts = [self.make_header(title)]
        parts.append(self.make_body(data))
        if self.should_include_chart(data):   # 钩子
            parts.append(self.make_chart(data))
        parts.append(self.make_footer())
        return "\n".join(parts)

    def make_header(self, title: str) -> str:
        return f"===== {title} ====="

    @abc.abstractmethod
    def make_body(self, data: dict) -> str:
        pass

    def make_chart(self, data: dict) -> str:
        return "图表：趋势折线图"

    @abc.abstractmethod
    def make_footer(self) -> str:
        pass

    def should_include_chart(self, data: dict) -> bool:
        """钩子：默认数据量够大才配图表"""
        return len(data) >= 3


class TextReport(ReportGenerator):
    def make_body(self, data: dict) -> str:
        return "\n".join(f"  {k}: {v}" for k, v in data.items())

    def make_footer(self) -> str:
        return "（文字版报告，无图表）"

    def should_include_chart(self, data: dict) -> bool:
        return False   # 覆盖钩子：文字版永不配图


class HtmlReport(ReportGenerator):
    def make_body(self, data: dict) -> str:
        return "<ul>" + "".join(f"<li>{k}={v}</li>" for k, v in data.items()) + "</ul>"

    def make_footer(self) -> str:
        return "</html>"

    def make_chart(self, data: dict) -> str:
        return "<img src='chart.png' />"


sales = {"周一": 100, "周二": 120, "周三": 90, "周四": 150}
print("== 文字版 ==")
print(TextReport().generate("本周销售", sales))
print("== HTML 版（数据量大，自动配图） ==")
print(HtmlReport().generate("本周销售", sales))
```

运行输出：

```
== 文字版 ==
===== 本周销售 =====
  周一: 100
  周二: 120
  周三: 90
  周四: 150
（文字版报告，无图表）
== HTML 版（数据量大，自动配图） ==
===== 本周销售 =====
<ul><li>周一=100</li><li>周二=120</li><li>周三=90</li><li>周四=150</li></ul>
<img src='chart.png' />
</html>
```

同一个 `generate` 骨架，两个子类一个不配图、一个按数据量自动配图——**基类管"流程"，钩子管"选择"。**

---

## 4. Python 特有玩法

### 4.1 GoF 经典例子的 Python 版：泡咖啡与泡茶

《设计模式》原书里模板方法的例子就是"泡咖啡 vs 泡茶"：烧水 → 冲泡 → 倒杯 → 加料，骨架一致。我们用 `abc` 写一版，顺便演示钩子的默认实现：

```python
import abc


class CaffeineBeverage(abc.ABC):
    """含咖啡因饮料：烧水→冲泡→倒杯→加料，骨架固定"""

    def prepare(self) -> None:
        print("1. 把水烧开")
        self.brew()                    # 抽象：怎么冲泡
        self.pour_in_cup()             # 具体：倒进杯子
        if self.wants_condiments():    # 钩子：要不要加料
            self.add_condiments()      # 抽象：加什么料

    @abc.abstractmethod
    def brew(self) -> None:
        pass

    def pour_in_cup(self) -> None:
        print("3. 倒进杯子里")

    def wants_condiments(self) -> bool:
        """钩子：默认要加料"""
        return True

    @abc.abstractmethod
    def add_condiments(self) -> None:
        pass


class Coffee(CaffeineBeverage):
    def brew(self) -> None:
        print("2. 用沸水冲泡咖啡粉")

    def add_condiments(self) -> None:
        print("4. 加糖和牛奶")


class Tea(CaffeineBeverage):
    def brew(self) -> None:
        print("2. 用沸水浸泡茶叶")

    def add_condiments(self) -> None:
        print("4. 加柠檬片")

    def wants_condiments(self) -> bool:
        return False   # 覆盖钩子：纯茶不加料


print("== 泡咖啡 ==")
Coffee().prepare()
print("== 泡茶 ==")
Tea().prepare()
```

运行输出：

```
== 泡咖啡 ==
1. 把水烧开
2. 用沸水冲泡咖啡粉
3. 倒进杯子里
4. 加糖和牛奶
== 泡茶 ==
1. 把水烧开
2. 用沸水浸泡茶叶
3. 倒进杯子里
```

`Coffee` 啥都没覆盖钩子，默认"加料"；`Tea` 覆盖了钩子，跳过了加料。**钩子的默认实现让"大部分子类不用写多余代码"。**

### 4.2 讨论：继承（模板方法）还是组合（函数参数）？

模板方法用继承，但**组合优于继承**（见导读）——如果流程只有一两个变化点，用"函数参数"更轻。同一需求，两种写法对比：

```python
import abc
import os
import tempfile


# ---- 方案 A：模板方法（继承）----
class ImporterA(abc.ABC):
    def run(self, source):
        rows = self.read(source)
        return self.save(rows)

    @abc.abstractmethod
    def read(self, source):
        pass

    @abc.abstractmethod
    def save(self, rows):
        pass


class CsvImporterA(ImporterA):
    def read(self, source):
        with open(source, encoding="utf-8") as f:
            return [ln.strip() for ln in f if ln.strip()]

    def save(self, rows):
        print(f"[继承版] 入库 {len(rows)} 行")
        return len(rows)


# ---- 方案 B：组合 + 函数参数 ----
def run_import(source, reader, saver):
    rows = reader(source)
    return saver(rows)


def read_csv(source):
    with open(source, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def save_db(rows):
    print(f"[组合版] 入库 {len(rows)} 行")
    return len(rows)


with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
    f.write("1\n2\n3\n")
    path = f.name

try:
    print("继承版：", CsvImporterA().run(path), "行")
    print("组合版：", run_import(path, read_csv, save_db), "行")
finally:
    os.unlink(path)
```

运行输出：

```
[继承版] 入库 3 行
继承版： 3 行
[组合版] 入库 3 行
组合版： 3 行
```

**怎么选？** 步骤多、流程稳定、希望强制子类实现、需要钩子 → 用模板方法（继承）；只有一两个变化点、流程简单 → 用函数参数（组合）。继承是"骨架强制"，组合是"零件自由"。

---

## 5. 真实世界中的它

### 标准库：`unittest.TestCase` 的 `setUp` / `tearDown`

你天天写的单元测试，就是模板方法模式的现场！`unittest` 运行每个测试用例时，骨架固定为 `setUp → 测试方法 → tearDown`，而 `setUp` / `tearDown` 就是**钩子方法**——你不写，它默认什么都不做；你写了，每个用例执行前后都会自动调用：

```python
import unittest


class ShoppingCartTest(unittest.TestCase):
    """unittest 就是模板方法：setUp/tearDown 是钩子"""

    def setUp(self):           # 钩子：每个用例执行前调用
        print("  钩子 setUp：准备购物车")
        self.cart = ["苹果", "香蕉"]

    def tearDown(self):        # 钩子：每个用例执行后调用
        print("  钩子 tearDown：清理购物车")
        self.cart = None

    def test_add_item(self):
        self.cart.append("橘子")
        self.assertEqual(len(self.cart), 3)

    def test_remove_item(self):
        self.cart.remove("苹果")
        self.assertEqual(len(self.cart), 1)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(ShoppingCartTest)
result = unittest.TestResult()           # 只收集结果，不做进度输出
suite.run(result)

print("用例数：", result.testsRun)
print("失败数：", len(result.failures))
print("错误数：", len(result.errors))
print("全部通过：", result.wasSuccessful())
```

运行输出：

```
  钩子 setUp：准备购物车
  钩子 tearDown：清理购物车
  钩子 setUp：准备购物车
  钩子 tearDown：清理购物车
用例数： 2
失败数： 0
错误数： 0
全部通过： True
```

你没在测试方法里调用 `setUp`，但它在每个用例前自动执行了——**谁在背后调用你？基类的模板方法。** 这就是好莱坞原则：框架（unittest）掌握流程，你的代码只负责实现钩子。

### 框架：Django 类视图的 `dispatch`

Django 的类视图（`View`）是模板方法的大户：基类的 `dispatch()` 负责"根据 HTTP 方法把请求路由给对应处理函数"，你写视图时只覆盖 `get()`、`post()` 这些钩子。加一个接口？加一个视图类、实现几个钩子方法即可，路由、鉴权、异常处理这些骨架由基类统一兜底。

---

## 6. 优缺点与适用场景

### 优点

- **复用骨架**：流程只写一遍，子类只填差异，消除复制粘贴；
- **强制一致性**：所有子类必须走同一套流程，不会有人"自由发挥"漏掉步骤；
- **钩子留扩展点**：默认行为之外，子类有选择性地"加戏"；
- **符合开闭原则**：加新流程 = 加新子类，不改基类。

### 缺点

- **继承耦合**：子类和基类绑死，基类改骨架，所有子类跟着受影响；
- **骨架过重**：模板方法里逻辑太多，子类想定制却无从下手；
- **类层次变深**：步骤一多，抽象类和子类的层级让人头晕；
- **过度统一**：流程其实各不相同却硬套一个骨架，反而别扭。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 多个流程骨架相同、细节不同（导入/导出/报表） | 流程之间差异巨大 |
| 想强制团队遵守统一流程 | 只有一两个变化点（用组合更轻） |
| 需要钩子提供"默认 + 可选扩展" | 骨架本身还在频繁变动 |
| 框架设计（让使用者填钩子） | 简单的一次性流程 |

> **Python 圈的共识**：模板方法在 Python 里经常被"函数参数"或装饰器替代——先问自己"真的需要强制继承吗"，再决定用哪种。

---

## 7. 与其他模式的关系

- **模板方法 vs 策略**：模板方法用**继承**固定骨架、子类换步骤；策略用**组合**换整个算法（第 3 章）。同一需求"换格式输出"，模板方法=抽象类+子类，策略=函数参数——4.2 已经对比过；
- **模板方法 + 工厂方法**：模板方法的骨架里，经常调用工厂方法（第 7 章）去创建需要的对象——基类定流程，子类定"造什么"；
- **模板方法 vs 状态**：状态模式（第 16 章）是"行为随状态变化"，模板方法是"行为随子类变化"——一个换的是状态，一个换的是身份。

---

## 8. 常见误区

### 误区 1：模板方法里塞太多逻辑，子类难以定制

骨架里把"具体步骤"也写死了，子类想改格式只能整体复制模板方法——这等于把钩子焊死：

```python
# 反面：基类把"怎么显示"写死，子类想改格式只能复制整个方法
import abc


class BadReport(abc.ABC):
    def generate(self, data):
        header = "===== 报表 ====="
        lines = [f"- {k}: {v}" for k, v in data.items()]
        # 想改分隔符？想加边框？这里写死了，子类无能为力
        return "\n".join([header] + lines)


# 正确：把"每行怎么格式化"做成抽象方法，交给子类
class GoodReport(abc.ABC):
    def generate(self, data):
        lines = [self.format_row(k, v) for k, v in data.items()]
        return "\n".join([self.header()] + lines)

    def header(self):
        return "===== 报表 ====="

    @abc.abstractmethod
    def format_row(self, key, value):
        pass


class MarkdownReport(GoodReport):
    def format_row(self, key, value):
        return f"| {key} | {value} |"


data = {"周一": 100}
print("反面版输出：")
print(BadReport().generate(data))
print("正确版输出：")
print(MarkdownReport().generate(data))
```

运行输出：

```
反面版输出：
===== 报表 =====
- 周一: 100
正确版输出：
===== 报表 =====
| 周一 | 100 |
```

**判断标准**：子类想定制时，如果只能复制粘贴整个模板方法，说明变化点没抽象出来。

### 误区 2：用模板方法强行统一流程

流程其实各不相同，也硬塞进一个骨架，结果子类把每个方法都覆盖一遍，甚至把模板方法整个重写——骨架成了摆设：

```python
# 反面：子类把每个步骤都重写一遍——说明这套骨架根本不适合它
import abc


class Workflow(abc.ABC):
    def run(self):
        self.step1()
        self.step2()

    @abc.abstractmethod
    def step1(self):
        pass

    @abc.abstractmethod
    def step2(self):
        pass


class WeirdJob(Workflow):
    """这个任务的流程和基类骨架完全不一样"""
    def run(self):      # 连模板方法都整体重写了——骨架成了摆设
        print("直接做一件完全不相关的事")

    def step1(self):
        print("不会被调用")

    def step2(self):
        print("也不会被调用")


WeirdJob().run()
```

运行输出：

```
直接做一件完全不相关的事
```

**经验法则**：如果某个子类要覆盖 80% 的方法，说明它不属于这个骨架——考虑策略模式或干脆单独写一个函数。

### 误区 3：钩子方法命名不清，子类作者分不清"必须实现"和"可选覆盖"

抽象方法必须实现、钩子可选覆盖，如果命名没规律，使用者只能靠猜。约定俗成的命名：抽象方法用"动词"（`read` / `save`），钩子用 `should_` / `on_` / `after_` 前缀：

```python
import abc


class Downloader(abc.ABC):
    """命名规范演示：on_ 前缀 = 钩子（可选），_fetch = 抽象（必须）"""

    def download(self, url: str) -> str:
        self.on_before()                 # 钩子：可选覆盖
        data = self._fetch(url)          # 抽象：必须实现
        self.on_after(data)              # 钩子：可选覆盖
        return data

    def on_before(self) -> None:
        pass                             # 钩子默认什么都不做

    @abc.abstractmethod
    def _fetch(self, url: str) -> str:
        pass

    def on_after(self, data: str) -> None:
        print(f"（默认钩子）下载完成，共 {len(data)} 个字符")


class HttpDownloader(Downloader):
    def _fetch(self, url: str) -> str:
        return f"来自 {url} 的内容"

    def on_before(self) -> None:
        print("钩子：检查网络连接")


print(HttpDownloader().download("https://example.com/page"))
```

运行输出：

```
钩子：检查网络连接
（默认钩子）下载完成，共 31 个字符
来自 https://example.com/page 的内容
```

名字一规范，使用者一看就懂：`on_` 开头的随便覆盖，`_fetch` 必须自己写。

---

## 9. 练习题

### 练习 1：用模板方法实现"支付流程"

支付流程骨架固定：选择渠道 → 扣款 → 通知。请实现支付宝和微信两个子类：

```python
# 答案：骨架在基类，差异在子类
import abc


class PayFlow(abc.ABC):
    """模板方法：支付流程骨架"""

    def pay(self, amount: float) -> str:
        self.choose_channel()
        result = self.deduct(amount)
        self.notify(result)
        return result

    @abc.abstractmethod
    def choose_channel(self) -> None:
        pass

    @abc.abstractmethod
    def deduct(self, amount: float) -> str:
        pass

    def notify(self, result: str) -> None:
        print(f"通知：支付{result}")


class AlipayFlow(PayFlow):
    def choose_channel(self):
        print("渠道：支付宝")

    def deduct(self, amount):
        print(f"支付宝扣款 {amount} 元")
        return "成功"


class WechatFlow(PayFlow):
    def choose_channel(self):
        print("渠道：微信支付")

    def deduct(self, amount):
        print(f"微信扣款 {amount} 元")
        return "成功"


AlipayFlow().pay(66.6)
WechatFlow().pay(88.8)
```

运行输出：

```
渠道：支付宝
支付宝扣款 66.6 元
通知：支付成功
渠道：微信支付
微信扣款 88.8 元
通知：支付成功
```

### 练习 2：给导入器加一个"是否打印日志"的钩子

给下面的 `Importer` 增加钩子 `verbose()`（默认 `False`），并在 `run` 里按钩子决定是否打印导入行数；再写一个覆盖钩子的子类：

```python
# 答案：钩子默认 False，子类可覆盖
import abc
import os
import tempfile


class Importer(abc.ABC):
    def run(self, source):
        rows = self.read(source)
        count = self.save(rows)
        if self.verbose():                 # 钩子：默认不打印
            print(f"本次导入 {count} 行")
        return count

    @abc.abstractmethod
    def read(self, source):
        pass

    @abc.abstractmethod
    def save(self, rows):
        pass

    def verbose(self) -> bool:
        return False


class TxtImporter(Importer):
    def read(self, source):
        with open(source, encoding="utf-8") as f:
            return [ln.strip() for ln in f if ln.strip()]

    def save(self, rows):
        print(f"入库 {len(rows)} 行")
        return len(rows)


class VerboseTxtImporter(TxtImporter):
    def verbose(self) -> bool:             # 覆盖钩子
        return True


with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
    f.write("a\nb\nc\n")
    path = f.name

try:
    print("普通导入：")
    TxtImporter().run(path)
    print("verbose 导入：")
    VerboseTxtImporter().run(path)
finally:
    os.unlink(path)
```

运行输出：

```
普通导入：
入库 3 行
verbose 导入：
入库 3 行
本次导入 3 行
```

### 练习 3：用"组合 + 函数参数"重写同一流程

不用继承，用一串函数实现"准备 → 烹饪 → 上桌"的流程：

```python
# 答案：组合版"模板"——流程就是函数列表，依次执行
def run_flow(steps, *args):
    """steps 是一串函数，前一个的输出作为后一个的输入"""
    result = None
    for step in steps:
        result = step(result, *args)
    return result


def step_prepare(prev, name):
    print(f"准备：{name}")
    return name


def step_cook(prev, name):
    print(f"烹饪：{prev}")
    return "熟了的" + prev


def step_serve(prev, name):
    print(f"上桌：{prev}")
    return prev


dish = run_flow([step_prepare, step_cook, step_serve], "红烧肉")
print("成品：", dish)
```

运行输出：

```
准备：红烧肉
烹饪：红烧肉
上桌：熟了的红烧肉
成品： 熟了的红烧肉
```

---

## 10. 小结与口诀

> **口诀：骨架基类定，步骤子类填；钩子留扇窗，好莱坞来掌权。**

模板方法模式是"复用流程、下放细节"的利器：**流程只写一遍，差异各填各的，钩子留足余地。** 记住三条：

1. 抽象方法**必须实现**，钩子**可选覆盖**——命名要让人一眼分清；
2. 骨架别塞太多细节，变化点都要抽象出来；
3. 流程简单时，用**组合 + 函数参数**比继承更轻。

下一章，我们来看另一种"流程反转"——这次反转的是通知的方向：**观察者模式**，有事广播，订阅者自知，互不认识。

---

*本章金句：模板方法是"好莱坞原则"的化身——别调用框架，框架会调用你；你只管填好钩子。*
