# 第 4 章 迭代器模式（Iterator）

> **一句话总结**：Python 早就替你实现了，你天天在用。
>
> | 分类 | 难度 | 实际使用率 |
> |------|:----:|:----:|
> | 行为型 | ★★☆☆☆ | ★★★★★ |

---

## 1. 引子：先讲个故事

去自助餐厅取餐，你端着盘子沿着餐台走：看到喜欢的，拿一份；盘子空了，继续往前；走到头，收工。你不需要知道后厨怎么做的菜，也不需要一次把整条餐台搬回家——**拿一份、吃一份、再拿下一份**，这个循环你熟得不能再熟。翻书也一样：一页一页翻，翻完为止，从来没人要求你先把整本书背下来再开始看。

程序里"翻书"就是遍历集合。Python 的 `for` 循环让你遍历列表、字典、文件……**只要对象"可迭代"，`for` 就替你翻**。但如果你自己写一个集合类，会发现它根本不认 `for`：

```python
# 引子：没有迭代协议的世界——自己写的集合没法用 for 遍历
class BookShelf:
    def __init__(self):
        self._books = ["三体", "活着", "百年孤独"]

    def count(self):
        return len(self._books)

    def get(self, index):
        return self._books[index]


shelf = BookShelf()
try:
    for book in shelf:
        print(book)
except TypeError as e:
    print("报错：", e)
```

运行输出：

```
报错： 'BookShelf' object is not iterable
```

"不是可迭代对象"——这个报错就是**迭代器模式**要解决的：让你的集合能被 `for` 遍历，而且遍历方式（一页一页翻）与内部存储方式（书放在哪）完全解耦。

---

## 2. 模式登场

### 定义

> **迭代器模式（Iterator）**：提供一种方法**顺序访问**一个聚合对象中的各个元素，而又不暴露其内部表示。

翻译：你告诉集合"我要从头到尾看一遍"，集合给你一个"翻书签"（迭代器），你每翻一次，它给你下一页——至于书是纸质的还是电子的、字是怎么排的，你完全不用管。

### 核心概念

- **可迭代对象（Iterable）**：有 `__iter__` 方法，调用它返回一个迭代器；
- **迭代器（Iterator）**：有 `__next__` 方法，每次调用返回下一个元素，没有就抛 `StopIteration`；
- **for 循环的本质**：`iter()` 拿迭代器 → 反复 `next()` 取元素 → 捕获 `StopIteration` 结束。

### 结构

```
┌───────────────────┐         ┌───────────────────┐
│     Iterable      │ __iter__│      Iterator     │
│  （可迭代对象）      │────────▶│     （迭代器）      │
├───────────────────┤  返回    ├───────────────────┤
│ + __iter__()      │         │ + __next__()      │
└───────────────────┘         └───────────────────┘
                                      │ 取完抛
                                      ▼
                              StopIteration
```

`for x in 集合` 的底层翻译：

```
it = iter(集合)                    # ① 拿到迭代器
while True:
    try:
        x = next(it)               # ② 取下一个元素
    except StopIteration:          # ③ 取完了就停
        break
```

### 角色

| 角色 | 说明 |
|------|------|
| **可迭代对象（Iterable）** | 能被遍历的集合，实现 `__iter__` 返回迭代器 |
| **迭代器（Iterator）** | 记录遍历位置，实现 `__next__`，取完抛 `StopIteration` |
| **客户端（Client）** | 用 `for` / `next()` 遍历，完全不关心内部结构 |

---

## 3. Python 实现

### 3.1 经典版：手写迭代协议（书架 + 独立迭代器）

教科书式写法：集合类实现 `__iter__`，再单独写一个迭代器类记录"翻到第几页"：

```python
class BookShelf:
    """可迭代对象：书架"""

    def __init__(self, books: list[str]):
        self._books = books

    def __iter__(self):
        return BookIterator(self)   # 每次调用返回一个新的迭代器

    def __len__(self):
        return len(self._books)


class BookIterator:
    """迭代器：记录遍历到哪里了"""

    def __init__(self, shelf: BookShelf):
        self._shelf = shelf
        self._index = 0

    def __next__(self) -> str:
        if self._index >= len(self._shelf):
            raise StopIteration     # 取完了：抛信号告诉 for 结束
        book = self._shelf._books[self._index]
        self._index += 1
        return book


shelf = BookShelf(["三体", "活着", "百年孤独"])
for book in shelf:
    print(f"读到：{book}")
```

运行输出：

```
读到：三体
读到：活着
读到：百年孤独
```

注意两个类的分工：`BookShelf` 只负责"我有书"，`BookIterator` 负责"翻到哪了"——**遍历的状态和集合的数据分开了**。这也是为什么 `for` 遍历 `shelf` 两次没问题：每次 `__iter__` 都返回一个全新的迭代器。

### 3.2 迭代器同时是可迭代对象：`__iter__` 返回 `self`

很多迭代器（比如文件对象、生成器）自己就"既是迭代器又是可迭代对象"——实现 `__iter__` 返回 `self` 即可。这样 `next()` 和 `for` 可以混着用：

```python
class CountDown:
    """倒计时迭代器：3 → 1"""

    def __init__(self, start: int):
        self._current = start

    def __iter__(self):
        return self                # 迭代器自己就是可迭代对象

    def __next__(self) -> int:
        if self._current <= 0:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value


it = CountDown(3)
print("手动取第一个：", next(it))
print("手动取第二个：", next(it))
print("剩下的交给 for：", end=" ")
for n in it:                       # for 会自动捕获 StopIteration
    print(n, end=" ")
print()
```

运行输出：

```
手动取第一个： 3
手动取第二个： 2
剩下的交给 for： 1
```

### 3.3 无限序列：斐波那契迭代器（惰性求值）

迭代器最大的本事：**可以不存数据，现取现算**。斐波那契数列是无限的，用列表根本装不下，但迭代器可以——要多少算多少：

```python
class Fibonacci:
    """无限斐波那契数列的迭代器"""

    def __init__(self):
        self._a, self._b = 0, 1

    def __iter__(self):
        return self

    def __next__(self) -> int:
        value = self._a
        self._a, self._b = self._b, self._a + self._b
        return value


fib = Fibonacci()
first_ten = [next(fib) for _ in range(10)]
print("前 10 个斐波那契数：", first_ten)
```

运行输出：

```
前 10 个斐波那契数： [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

**惰性求值**就是"按需计算"：不提前算出全部，取一个算一个。大文件、无限序列、数据流，全靠这个特性才能在内存里活下来。

---

## 4. Python 特有玩法

### 4.1 生成器 `yield`：最强的迭代器

手写 `__iter__`/`__next__` 太啰嗦？Python 给了语法糖：**函数里出现 `yield`，这个函数就自动变成迭代器**——不用写类、不用管 `StopIteration`：

```python
def countdown(n: int):
    while n > 0:
        yield n
        n -= 1


def even_numbers(limit: int):
    """生成偶数序列"""
    for i in range(limit):
        if i % 2 == 0:
            yield i


print("倒计时：", list(countdown(5)))
print("前几个偶数：", list(even_numbers(10)))
```

运行输出：

```
倒计时： [5, 4, 3, 2, 1]
前几个偶数： [0, 2, 4, 6, 8]
```

`yield` 比手写迭代器类好在哪？状态（`n` 减到哪了、`i` 循环到哪了）**由函数局部变量自动保存**，不用自己记 `_index`。写迭代器，90% 的场景用生成器就够了。

### 4.2 `itertools`：标准库的迭代器工具箱

`itertools` 是一堆"迭代器零件"：拼接、组合、切片……组合起来能玩出花：

```python
import itertools


def fib_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


merged = itertools.chain([1, 2], ["a", "b"], "hi")
print("chain 拼接：", list(merged))

for combo in itertools.product(["红", "蓝"], ["大", "小"]):
    print("product：", combo)

print("斐波那契前 8 个：", list(itertools.islice(fib_gen(), 8)))
```

运行输出：

```
chain 拼接： [1, 2, 'a', 'b', 'h', 'i']
product： ('红', '大')
product： ('红', '小')
product： ('蓝', '大')
product： ('蓝', '小')
斐波那契前 8 个： [0, 1, 1, 2, 3, 5, 8, 13]
```

`islice` 给无限迭代器"切一片"，`chain` 把多个迭代器串成一条流水线——全都是惰性的，不产生中间大列表。

### 4.3 手动模拟 `for`：看懂循环的底裤

`for` 的底层就三步：`iter()` → `next()` → 捕获 `StopIteration`。咱们手动来一遍：

```python
words = ["迭代", "器", "模式"]

it = iter(words)                   # ① 拿到迭代器
while True:
    try:
        word = next(it)            # ② 取下一个
        print("取到：", word)
    except StopIteration:          # ③ 取完了
        print("迭代结束")
        break
```

运行输出：

```
取到： 迭代
取到： 器
取到： 模式
迭代结束
```

看懂这段，你就看懂了 Python 里一切 `for`——不管是遍历列表、字典、文件还是生成器，底层都是这套协议。

---

## 5. 真实世界中的它

### 文件对象：逐行读大文件（惰性的典范）

读一个 10 GB 的日志文件，你不可能 `read()` 全读进内存——文件对象本身就是迭代器，**一行一行吐**，内存占用恒定为一行的大小：

```python
import io

# 用 io.StringIO 模拟一个"文件"
fake_file = io.StringIO("第一行\n第二行\n第三行\n")

for line in fake_file:             # 文件对象可迭代，每次吐一行
    print("读到：", line.strip())
```

运行输出：

```
读到： 第一行
读到： 第二行
读到： 第三行
```

### `zip` / `enumerate` / `map`：全是惰性迭代器

这三个高频函数返回的都是迭代器（不是列表），配合 `dict` 的迭代行为一起看：

```python
names = ["小明", "小红", "小刚"]
scores = [88, 95, 72]

pairs = zip(names, scores)         # zip 是迭代器，用一次就没了
print("zip 配对：", list(pairs))

print("enumerate 带下标：", list(enumerate(names)))

print("map 映射：", list(map(str.upper, ["a", "b", "c"])))

info = {"name": "小明", "age": 18}
print("dict 默认遍历键：", list(info))
print("dict.items() 遍历键值：", list(info.items()))
```

运行输出：

```
zip 配对： [('小明', 88), ('小红', 95), ('小刚', 72)]
enumerate 带下标： [(0, '小明'), (1, '小红'), (2, '小刚')]
map 映射： ['A', 'B', 'C']
dict 默认遍历键： ['name', 'age']
dict.items() 遍历键值： [('name', '小明'), ('age', 18)]
```

### `range`：一百亿个数，不占内存

`range(10**10)` 看起来像个巨型列表，其实是个惰性序列——它只记住"起点、终点、步长"三个数：

```python
r = range(10**10)                  # 一百亿个数，但不占内存
print("range 对象：", r)
print("前 5 个：", list(r[:5]))
print("前 100 个之和：", sum(range(100)))
```

运行输出：

```
range 对象： range(0, 10000000000)
前 5 个： [0, 1, 2, 3, 4]
前 100 个之和： 4950
```

再往大了说：**Python 的 `for` 循环本身就是迭代器模式的实现**，你从学 Python 第一天起就在用这个模式。

---

## 6. 优缺点与适用场景

### 优点

- **遍历与存储解耦**：换内部结构（列表→树→文件），遍历代码一行不用改；
- **惰性求值**：大文件、无限序列也能遍历，内存占用恒定；
- **统一接口**：所有可迭代对象都能 `for`，学习成本为零；
- **Python 原生支持**：实现 `__iter__` 即可，语法糖管够。

### 缺点

- **一次性消费**：迭代器用完就没了，想再遍历要重新拿一个；
- **不能随机访问**：迭代器只知道"下一个"，不知道"第 N 个"；
- **不知道长度**：迭代器不知道自己还剩多少元素（除非自己记）。

### 适用场景

| 适合 | 不适合 |
|------|--------|
| 自定义集合需要统一遍历 | 需要随机访问（直接用下标/索引） |
| 大文件、大数据流（惰性读） | 需要反复遍历同一份数据（先转成 list） |
| 无限/超长序列（斐波那契、ID 生成） | 需要知道元素个数或当前位置 |
| 隐藏集合内部结构 | 集合本身简单到不需要封装 |

---

## 7. 与其他模式的关系

- **迭代器 + 组合**：组合模式（第 17 章）把对象组织成树，树的深度优先遍历就靠迭代器——遍历树形结构是它俩的经典合作。
- **迭代器 + 访问者**：访问者（第 22 章）把"遍历"和"操作"分离，迭代器负责"怎么走"，访问者负责"走到哪干什么"。
- **迭代器 + 生成器**：生成器是迭代器的语法糖——`yield` 自动实现了 `__iter__`/`__next__`/`StopIteration`。
- **迭代器 vs 观察者**：迭代器是"拉"——主动去取下一个；观察者（第 9 章）是"推"——数据来了通知你。一个自己取，一个等人送。

---

## 8. 常见误区

### 误区 1：以为可迭代对象就是迭代器

这是新手第一坑：**list 能被 `for`，但它不是迭代器**——它有 `__iter__` 没有 `__next__`，不能直接 `next()`：

```python
words = ["a", "b", "c"]
print("list 有 __iter__：", hasattr(words, "__iter__"))
print("list 有 __next__：", hasattr(words, "__next__"))

try:
    next(words)
except TypeError as e:
    print("直接 next(list) 报错：", e)

it = iter(words)                   # 先 iter() 拿到迭代器
print("迭代器有 __next__：", hasattr(it, "__next__"))
print("next(it)：", next(it))
```

运行输出：

```
list 有 __iter__： True
list 有 __next__： False
直接 next(list) 报错： 'list' object is not an iterator
迭代器有 __next__： True
next(it)： a
```

关系一句话：**可迭代对象"产"迭代器，迭代器"管"遍历**。`iter(可迭代对象)` 把前者变成后者。

### 误区 2：以为迭代器可以反复遍历

迭代器是**一次性**的——取完就空了，不会"回到开头"：

```python
it = iter([1, 2, 3])
print("第一次遍历：", list(it))
print("第二次遍历：", list(it))   # 空的！迭代器没有"复位"功能
```

运行输出：

```
第一次遍历： [1, 2, 3]
第二次遍历： []
```

想遍历两遍？重新 `iter()` 一次（对可迭代对象），或者干脆 `list(it)` 缓存成列表。

### 误区 3：遍历的时候修改集合

"边遍历边删"是经典翻车现场——`for` 底层在数元素，你一边数一边改，计数就乱了：

```python
data = {"a": 1, "b": 2, "c": 3}
try:
    for key in data:
        if key == "b":
            data.pop(key)
except RuntimeError as e:
    print("报错：", e)
```

运行输出：

```
报错： dictionary changed size during iteration
```

正确姿势：**先收集要删的键，遍历完再删**（`for key in list(data.keys())` 或先 `to_remove.append(key)`）。

---

## 9. 练习题

### 练习 1：给"扑克牌"实现 `__iter__`

让 `Deck` 能被 `for` 遍历出全部 52 张牌（花色 × 点数）：

```python
class Deck:
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __iter__(self):
        # 答案：列表推导 + iter()，一行搞定
        return iter([f"{r}{s}" for s in self.suits for r in self.ranks])


deck = Deck()
cards = list(deck)
print("总牌数：", len(cards))
print("前 5 张：", cards[:5])
print("后 5 张：", cards[-5:])
```

运行输出：

```
总牌数： 52
前 5 张： ['A♠', '2♠', '3♠', '4♠', '5♠']
后 5 张： ['9♣', '10♣', 'J♣', 'Q♣', 'K♣']
```

### 练习 2：用 `yield` 重写书架遍历

把 3.1 的书架迭代改成生成器版：

```python
class BookShelf:
    def __init__(self, books):
        self._books = books

    def __iter__(self):
        # 答案：yield 版，三行搞定
        for book in self._books:
            yield book


shelf = BookShelf(["三体", "活着", "百年孤独"])
print([f"《{b}》" for b in shelf])
```

运行输出：

```
['《三体》', '《活着》', '《百年孤独》']
```

### 练习 3：写一个惰性"质数迭代器"

生成无限质数序列，只取前 6 个（提示：用 `itertools.islice` 切片）：

```python
import itertools


def primes():
    n = 2
    while True:
        for d in range(2, int(n ** 0.5) + 1):
            if n % d == 0:
                break
        else:                      # for 循环没被 break → 是质数
            yield n
        n += 1


first_six = list(itertools.islice(primes(), 6))
print("前 6 个质数：", first_six)
```

运行输出：

```
前 6 个质数： [2, 3, 5, 7, 11, 13]
```

---

## 10. 小结与口诀

> **口诀：可迭代对象出迭代器，迭代器管 next；for 是糖，yield 是神器，惰性求值省到底。**

迭代器模式是唯一一个"Python 帮你实现好了"的 GoF 模式——你天天用 `for`，却很少意识到它背后是一整套协议。记住三条：

1. **`__iter__` 产迭代器，`__next__` 管遍历**，取完抛 `StopIteration`；
2. 自己写迭代器，**优先用 `yield` 生成器**，别手写类；
3. **惰性求值**是它最值钱的特性：大文件、无限序列，照遍历不误。

下一章，我们来看 Python 里另一个"语法即模式"的存在——**装饰器模式**：一层层包装，不动原物。

---

*本章金句：迭代器把"怎么存"和"怎么遍历"分开——集合负责保管，迭代器负责翻页，for 负责喊"下一页"。*
