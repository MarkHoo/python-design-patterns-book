#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《Python 设计模式修炼手册》输出一致性检查脚本

verify_code.py 只保证代码块"能运行"，本脚本进一步核对：每个代码块
后面的"运行输出："块中的内容，是否与代码块实际运行产生的 stdout 一致
（宽松对比：忽略空行与首尾空白）。

注意：
- "运行输出："块中若包含输出之外的说明文字（如注释性内容），会报为不一致，
  请人工判断后决定是修改输出块还是调整代码。
- 每个代码块与其后紧跟的"运行输出："块配对；代码块后没有"运行输出："块时，
  如果该代码块实际有 stdout 输出，也会提示。

用法：
    python scripts/check_outputs.py
    python scripts/check_outputs.py --files "03-策略模式-Strategy.md"
    python scripts/check_outputs.py --verbose
"""

import argparse
import pathlib
import re
import sys

import verify_code  # 复用提取与运行逻辑（同目录）

BOOK_DIR = pathlib.Path(__file__).resolve().parent.parent
FENCE = re.compile(r"```(\w*)\s*\n(.*?)```", re.S)
OUTPUT_MARK = "运行输出："


def normalize(text: str) -> str:
    """宽松归一化：去空白行、去首尾空白"""
    lines = [ln.strip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def pair_blocks(md_path: pathlib.Path):
    """返回 [(代码块文本, 其后的运行输出块文本或 None), ...]"""
    text = md_path.read_text(encoding="utf-8")
    fences = list(FENCE.finditer(text))
    pairs = []
    for i, m in enumerate(fences):
        lang = m.group(1)
        if lang not in ("python", "py"):
            continue
        code = m.group(2)
        # 代码块与其后紧跟的 fence 之间若有 "运行输出：" 标记，
        # 且该 fence 是裸 ``` 块，则它就是输出标注块
        output_block = None
        if i + 1 < len(fences):
            between = text[m.end(): fences[i + 1].start()]
            if OUTPUT_MARK in between and fences[i + 1].group(1) == "":
                output_block = fences[i + 1].group(2)
        pairs.append((code, output_block))
    return pairs


def main():
    parser = argparse.ArgumentParser(description="核对代码块运行输出与书中的'运行输出：'标注")
    parser.add_argument("--files", nargs="*", default=None, help="要检查的文件名，默认全部")
    parser.add_argument("--verbose", action="store_true", help="输出对比详情")
    args = parser.parse_args()

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    md_files = verify_code.collect_md_files(args.files)
    total = mismatch = no_mark = 0
    issues = []

    for md in md_files:
        for idx, (code, output_block) in enumerate(pair_blocks(md), start=1):
            total += 1
            ok, stderr, stdout = verify_code.run_block(code, 30)
            if not ok:
                issues.append((md, idx, "代码块运行失败（请先用 verify_code.py 修复）", ""))
                mismatch += 1
                continue
            if output_block is None:
                if stdout.strip():
                    issues.append((md, idx, "代码块有输出但后面没有'运行输出：'标注", stdout.strip()[:60]))
                    no_mark += 1
                continue
            actual = normalize(stdout)
            claimed = normalize(output_block)
            if actual == claimed:
                if args.verbose:
                    print(f"[MATCH] {md.name} #{idx:02d}")
            else:
                issues.append((md, idx, "运行输出与实际不一致", ""))
                mismatch += 1
                if args.verbose:
                    print(f"[DIFF ] {md.name} #{idx:02d}")
                    print(f"        书中所写: {claimed[:120]!r}")
                    print(f"        实际输出: {actual[:120]!r}")

    print("=" * 60)
    print(f"共 {total} 个代码块：{total - mismatch - no_mark} 一致，{mismatch} 不一致，{no_mark} 缺标注")
    if issues:
        for md, idx, reason, detail in issues:
            print(f"  - {md.name} #{idx:02d}: {reason} {detail}")
    print("=" * 60)
    sys.exit(0 if mismatch == 0 else 1)


if __name__ == "__main__":
    main()
