#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《Python 设计模式修炼手册》一致性检查脚本

检查：
1. 章节文件是否齐全、编号是否连续（00~25）
2. 每个模式章节（01~24）的 10 个小节结构是否完整
3. 每章头部的星级/分类是否与 README 目录表一致
4. README 目录中的链接是否有效

用法：
    python scripts/check_consistency.py
    python scripts/check_consistency.py --verbose
"""

import argparse
import pathlib
import re
import sys

BOOK_DIR = pathlib.Path(__file__).resolve().parent.parent

EXPECTED = [
    ("00", "导读"),
    ("01", "单例"), ("02", "简单工厂"), ("03", "策略"), ("04", "迭代器"),
    ("05", "装饰器"), ("06", "外观"), ("07", "工厂方法"), ("08", "模板方法"),
    ("09", "观察者"), ("10", "适配器"), ("11", "建造者"), ("12", "代理"),
    ("13", "责任链"), ("14", "抽象工厂"), ("15", "命令"), ("16", "状态"),
    ("17", "组合"), ("18", "原型"), ("19", "中介者"), ("20", "备忘录"),
    ("21", "桥接"), ("22", "访问者"), ("23", "享元"), ("24", "解释器"),
    ("25", "结语"),
]

# README 中的期望星级：{章节链接文件名: (难度, 使用率)}
# 与 README.md 目录表保持一致，修改 README 时需同步修改这里
EXPECTED_STARS = {
    "01-单例模式-Singleton.md": ("★☆☆☆☆", "★★★★★"),
    "02-简单工厂-Simple-Factory.md": ("★☆☆☆☆", "★★★★★"),
    "03-策略模式-Strategy.md": ("★★☆☆☆", "★★★★★"),
    "04-迭代器模式-Iterator.md": ("★★☆☆☆", "★★★★★"),
    "05-装饰器模式-Decorator.md": ("★★★☆☆", "★★★★★"),
    "06-外观模式-Facade.md": ("★★☆☆☆", "★★★★☆"),
    "07-工厂方法-Factory-Method.md": ("★★☆☆☆", "★★★★☆"),
    "08-模板方法-Template-Method.md": ("★★☆☆☆", "★★★★☆"),
    "09-观察者模式-Observer.md": ("★★☆☆☆", "★★★★☆"),
    "10-适配器模式-Adapter.md": ("★★☆☆☆", "★★★★☆"),
    "11-建造者模式-Builder.md": ("★★★☆☆", "★★★★☆"),
    "12-代理模式-Proxy.md": ("★★★☆☆", "★★★★☆"),
    "13-责任链模式-Chain-of-Responsibility.md": ("★★★☆☆", "★★★★☆"),
    "14-抽象工厂-Abstract-Factory.md": ("★★★☆☆", "★★★☆☆"),
    "15-命令模式-Command.md": ("★★★☆☆", "★★★☆☆"),
    "16-状态模式-State.md": ("★★★☆☆", "★★★☆☆"),
    "17-组合模式-Composite.md": ("★★★☆☆", "★★★☆☆"),
    "18-原型模式-Prototype.md": ("★★☆☆☆", "★★☆☆☆"),
    "19-中介者模式-Mediator.md": ("★★★☆☆", "★★☆☆☆"),
    "20-备忘录模式-Memento.md": ("★★★☆☆", "★★☆☆☆"),
    "21-桥接模式-Bridge.md": ("★★★★☆", "★★☆☆☆"),
    "22-访问者模式-Visitor.md": ("★★★★☆", "★★☆☆☆"),
    "23-享元模式-Flyweight.md": ("★★★★☆", "★☆☆☆☆"),
    "24-解释器模式-Interpreter.md": ("★★★★★", "★☆☆☆☆"),
}

SECTION_RE = re.compile(r"^## (\d+)\. ", re.M)
# 匹配章节头部 blockquote 表格中的数据行：> | 创建型 | ★☆☆☆☆ | ★★★★★ |
STARS_RE = re.compile(r"^>\s*\| [^|]+ \| ([★☆]+) \| ([★☆]+) \|", re.M)
TITLE_RE = re.compile(r"^# 第 (\d+) 章 ")


def main():
    parser = argparse.ArgumentParser(description="全书一致性检查")
    parser.add_argument("--verbose", action="store_true", help="输出详细信息")
    args = parser.parse_args()

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    problems = []
    chapter_mantras = {}   # {章节号: 口诀}，用于与附录 A 对比

    # 1. 文件齐全性
    md_files = {p.name: p for p in BOOK_DIR.glob("*.md")}
    for num, keyword in EXPECTED:
        matches = [n for n in md_files if n.startswith(num + "-")]
        if not matches:
            problems.append(f"缺少章节文件：{num}-（应包含关键词'{keyword}'）")
        elif len(matches) > 1:
            problems.append(f"章节号重复：{num} -> {matches}")
        else:
            name = matches[0]
            if keyword not in name:
                problems.append(f"章节文件名与预期不符：{name}（预期含'{keyword}'）")

    # 2. README 链接有效性
    readme = (BOOK_DIR / "README.md").read_text(encoding="utf-8")
    for name in md_files:
        if name == "README.md":
            continue
        if f"](./{name})" not in readme:
            problems.append(f"README 目录缺少链接：{name}")

    # 3. 章节结构 + 星级
    for num, _ in EXPECTED:
        matches = [n for n in md_files if n.startswith(num + "-")]
        if len(matches) != 1:
            continue
        name = matches[0]
        path = BOOK_DIR / name
        text = path.read_text(encoding="utf-8")

        if num in ("00", "25"):
            continue  # 导读与结语不检查小节结构

        # 首行标题
        first_line = text.strip().splitlines()[0] if text.strip() else ""
        title_match = TITLE_RE.match(first_line)
        if not title_match:
            problems.append(f"{name}：首行标题应为 '# 第 {int(num)} 章 ...'，实际为：{first_line[:40]}")
        elif int(title_match.group(1)) != int(num):
            problems.append(f"{name}：标题章节号 {title_match.group(1)} 与文件名 {num} 不一致")

        # 10 个小节
        sections = {int(m) for m in SECTION_RE.findall(text)}
        missing = [i for i in range(1, 11) if i not in sections]
        if missing:
            problems.append(f"{name}：缺少小节 {missing}")

        # 星级
        star_rows = STARS_RE.findall(text)
        if not star_rows:
            problems.append(f"{name}：头部缺少难度/使用率星级")
        else:
            expected = EXPECTED_STARS.get(name)
            if expected is None:
                problems.append(f"{name}：check_consistency.py 中未登记期望星级")
            else:
                got = tuple(star_rows[0])
                if got != expected:
                    problems.append(
                        f"{name}：星级与 README 不一致，章节={got}，期望={expected}"
                    )

        # 金句（模式章节 01~24 必须有"本章金句"，导读 00 已有）
        if "本章金句" not in text:
            problems.append(f"{name}：缺少'本章金句'")

        # 收集口诀（小结里的 > **口诀：...**），供与附录 A 对比
        mantra_m = re.search(r"^> \*\*口诀[：:](.+?)\*\*$", text, re.M)
        if num not in ("00", "25", "26"):
            if mantra_m is None:
                problems.append(f"{name}：缺少小结口诀（> **口诀：...**）")
            else:
                chapter_mantras[int(num)] = mantra_m.group(1).strip()

    # 3.5 附录 A：存在性 + 口诀表与各章口诀一致性
    appendix_files = [n for n in md_files if n.startswith("26-")]
    if len(appendix_files) != 1:
        problems.append("缺少附录 A 文件（26-附录A-24模式速查表.md）")
    else:
        appendix_text = (BOOK_DIR / appendix_files[0]).read_text(encoding="utf-8")
        # 只解析"## 5. 口诀汇总"到"## 6."之间的表格
        sec5 = re.search(r"## 5\. 口诀汇总.*?(?=\n## 6\.)", appendix_text, re.S)
        if sec5 is None:
            problems.append("附录 A：找不到'## 5. 口诀汇总'小节")
        else:
            table_rows = re.findall(r"^\| (\d+) \| (.+) \|$", sec5.group(0), re.M)
            appendix_mantras = {int(n): m.strip() for n, m in table_rows}
            for num, mantra in sorted(chapter_mantras.items()):
                if num not in appendix_mantras:
                    problems.append(f"附录 A 口诀表缺少第 {num} 章")
                elif appendix_mantras[num] != mantra:
                    problems.append(
                        f"附录 A 第 {num} 章口诀与正文不一致：\n"
                        f"    正文：{mantra}\n"
                        f"    附录：{appendix_mantras[num]}"
                    )
            for num in appendix_mantras:
                if num not in chapter_mantras:
                    problems.append(f"附录 A 口诀表多出第 {num} 章（正文无此章）")

    # 4. 代码块/运行输出配对数（提示性，不判错）
    for num, _ in EXPECTED:
        matches = [n for n in md_files if n.startswith(num + "-")]
        if len(matches) != 1:
            continue
        name = matches[0]
        text = (BOOK_DIR / name).read_text(encoding="utf-8")
        code_blocks = len(re.findall(r"```python\s*\n", text))
        outputs = len(re.findall(r"^运行输出：$", text, re.M))
        if args.verbose:
            print(f"{name}: {code_blocks} 个代码块, {outputs} 个'运行输出：'标注")

    print("=" * 60)
    if problems:
        print("发现 %d 个问题：" % len(problems))
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    else:
        print("一致性检查全部通过 ✓（章节齐全、结构完整、星级一致、链接有效、金句齐全、附录口诀一致）")
        sys.exit(0)


if __name__ == "__main__":
    main()
