#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《Python 设计模式修炼手册》随书源码导出脚本

把书中所有 Markdown 章节里的 ```python 代码块，提取为可独立运行的
.py 文件，按章节归类到「随书源码/」目录。每个文件都附带来源注释
（章节、块序号、代码块前的标题），文件名取自代码块前最近的小节标题。

用法：
    python scripts/export_src.py            # 全量导出（先清空旧目录）
    python scripts/export_src.py --dry      # 只统计，不写文件
"""

import argparse
import pathlib
import re
import sys

BOOK_DIR = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = BOOK_DIR / "随书源码"

FENCE = re.compile(r"```(\w*)\s*\n(.*?)```", re.S)
HEADING = re.compile(r"^(#{2,4})\s+(.+?)\s*$", re.M)
ILLEGAL = re.compile(r'[\\/:*?"<>|`\x00-\x1f]')


def clean_name(text: str) -> str:
    """清理为合法的 Windows 文件名片段（全角字符保留）"""
    name = ILLEGAL.sub("-", text)
    name = name.strip().strip(".").strip()
    return name[:80] or "unnamed"


def heading_before(text: str, pos: int) -> str:
    """返回 pos 之前最近的 ## / ### / #### 标题文本"""
    best = None
    for m in HEADING.finditer(text, 0, pos):
        best = m
    if best is None:
        return "无标题"
    return best.group(2).strip()


def collect():
    """返回 [(md 文件, 块序号, 代码文本, 标题), ...]（按目录顺序）"""
    items = []
    for md in sorted(BOOK_DIR.glob("*.md")):
        if md.name == "README.md":
            continue
        text = md.read_text(encoding="utf-8")
        fences = list(FENCE.finditer(text))
        idx = 0
        for i, m in enumerate(fences):
            if m.group(1) not in ("python", "py"):
                continue
            idx += 1
            title = heading_before(text, m.start())
            items.append((md, idx, m.group(2).strip("\n"), title))
    return items


def main():
    parser = argparse.ArgumentParser(description="导出随书源码")
    parser.add_argument("--dry", action="store_true", help="只统计不写入")
    args = parser.parse_args()

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    items = collect()
    if args.dry:
        print(f"共 {len(items)} 个代码块：")
        from collections import Counter

        cnt = Counter(md.name for md, _, _, _ in items)
        for name, n in sorted(cnt.items()):
            print(f"  {name}: {n}")
        return

    # 清空旧导出目录（保留其中 README.md）
    if OUT_DIR.exists():
        for p in OUT_DIR.iterdir():
            if p.name != "README.md":
                if p.is_dir():
                    import shutil

                    shutil.rmtree(p, ignore_errors=True)
                else:
                    p.unlink()
    OUT_DIR.mkdir(exist_ok=True)

    written = 0
    for md, idx, code, title in items:
        chapter_dir = OUT_DIR / (md.stem + "/")
        chapter_dir.mkdir(exist_ok=True)
        base = clean_name(title)
        target = chapter_dir / (base + ".py")
        n = 2
        while target.exists():
            target = chapter_dir / f"{base}-{n}.py"
            n += 1
        header = (
            "# -*- coding: utf-8 -*-\n"
            f"# 来源：《Python 设计模式修炼手册》{md.stem}\n"
            f"# 代码块 #{idx}：{title}\n"
            "# 本书承诺：本文件与书中代码逐字一致，可独立运行。\n\n"
        )
        target.write_text(header + code + "\n", encoding="utf-8")
        written += 1

    print(f"导出完成：{written} 个代码块 → {OUT_DIR.name}/ 目录（{len(items)} 源）")


if __name__ == "__main__":
    main()
