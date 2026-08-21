# 随书源码

本目录是《Python 设计模式修炼手册》的**全部代码示例**，由 `scripts/export_src.py`
自动从各章节 Markdown 中提取生成（339 个文件，与书中代码**逐字一致**）。

## 目录结构

每个章节一个文件夹，文件名取自书中代码块前的小节标题：

```
随书源码/
├── README.md
├── 00-导读-设计模式入门/
│   ├── 0.3-类、对象、继承、多态.py
│   └── ...
├── 01-单例模式-Singleton/
│   ├── 1. 引子：先讲个故事.py
│   ├── 3.1 经典版：用 __new__ 拦截创建.py
│   └── ...
├── 02-简单工厂-Simple-Factory/
└── ...（每个章节一个文件夹）
```

每个 `.py` 文件都是**完整、自包含、可独立运行**的（这是全书代码规范），
文件头注释标明来源章节与代码块序号，方便对照书中位置。

## 如何运行

```bash
# 运行任意一个示例（Python 3.8+，只用标准库）
python "随书源码\01-单例模式-Singleton\3.1 经典版：用 __new__ 拦截创建.py"

# 批量验证所有 339 个文件都能运行
python scripts\verify_src.py
```

## 重新导出

修改了章节 Markdown 后，重新生成本目录：

```bash
python scripts\export_src.py          # 全量重新导出
python scripts\export_src.py --dry    # 只统计不写入
```

## 验证闭环

- `scripts/verify_code.py`：验证 **Markdown 里的代码块**可运行、输出标注一致；
- `scripts/verify_src.py`：验证 **本目录导出的文件**可独立运行；
- 两边都通过 = 书中代码与源码文件完全对应且全部可运行。
