# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》26-附录A-24模式速查表
# 代码块 #1：6. 附：迷你"模式查找器"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 迷你模式查找器：输入关键词，输出候选模式
PATTERNS = {
    "唯一": "单例 Singleton：全局只能有一份的资源",
    "按参数创建": "简单工厂 Simple Factory：一个函数按参数出对象",
    "换算法": "策略 Strategy：同一件事多种算法，运行时切换",
    "遍历": "迭代器 Iterator：自定义集合支持 for 循环与惰性求值",
    "叠加能力": "装饰器 Decorator：日志/缓存/权限，不改原代码",
    "简化入口": "外观 Facade：复杂子系统包一层简单接口",
    "子类定制创建": "工厂方法 Factory Method：创建逻辑下沉到子类",
    "固定流程": "模板方法 Template Method：骨架固定，步骤可换",
    "通知": "观察者 Observer：一对多广播，互不认识",
    "接口不兼容": "适配器 Adapter：换插头，两边都不改",
    "参数太多": "建造者 Builder：分步构建，链式调用",
    "控制访问": "代理 Proxy：懒加载/权限/远程，经纪人模式",
    "多级处理": "责任链 Chain of Responsibility：层层审批，传到为止",
    "成套产品": "抽象工厂 Abstract Factory：一族产品成套生产",
    "可撤销": "命令 Command：动作打包，可排队可撤销",
    "状态流转": "状态 State：行为随状态切换",
    "流转": "状态 State：行为随状态切换",
    "缓存": "装饰器 Decorator：日志/缓存/权限，不改原代码（如 @lru_cache）",
    "树形": "组合 Composite：叶子与容器一视同仁",
    "克隆": "原型 Prototype：复制现成的再微调",
    "多对多": "中介者 Mediator：中间人传话，避免乱成一团",
    "回滚": "备忘录 Memento：快照存档，随时回档",
    "两个维度": "桥接 Bridge：双维度各自演化",
    "操作常变": "访问者 Visitor：结构不动，操作外挂",
    "省内存": "享元 Flyweight：共享重复的细粒度对象",
    "小语言": "解释器 Interpreter：定义一门 DSL 并解释执行",
}


def find_pattern(question: str) -> list:
    """输入一句需求描述，返回匹配的模式建议"""
    hits = []
    for keyword, advice in PATTERNS.items():
        if keyword in question:
            hits.append(advice)
    return hits or ["未匹配到模式，试试更具体的描述，或先别用模式（YAGNI）"]


for q in ("这个配置要全局唯一", "订单状态需要流转", "我想给接口加个缓存"):
    print(f"问：{q}")
    for advice in find_pattern(q):
        print(f"  答：{advice}")
    print()
