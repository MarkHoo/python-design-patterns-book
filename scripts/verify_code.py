#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《Python 设计模式修炼手册》全书代码验证脚本

提取所有 Markdown 文件中的 ```python / ```py 代码块，在隔离的临时目录中
逐个实际运行，任何一个代码块运行失败都会报告章节位置与错误信息。

用法：
    python scripts/verify_code.py                        # 验证书目录下所有 .md
    python scripts/verify_code.py --files "03-策略模式-Strategy.md"
    python scripts/verify_code.py --files "*.md"         # 支持通配符
    python scripts/verify_code.py --list                 # 只统计，不运行
    python scripts/verify_code.py --timeout 60           # 自定义单块超时（秒）
    python scripts/verify_code.py --show                 # 失败时打印完整代码
    python scripts/verify_code.py --verbose              # 成功时也打印运行输出
"""

import argparse
import glob as glob_mod
import os
import pathlib
import re
import subprocess
import sys
import tempfile

BOOK_DIR = pathlib.Path(__file__).resolve().parent.parent
BLOCK_RE = re.compile(r"```(?:python|py)\s*\n(.*?)```", re.S)


def extract_blocks(md_path: pathlib.Path):
    """返回 [(代码块序号, 代码文本), ...]"""
    text = md_path.read_text(encoding="utf-8")
    blocks = []
    for m in BLOCK_RE.finditer(text):
        code = m.group(1)
        # 去掉可能的语言属性行残留（如 ```python title="xxx" 的意外换行）
        lines = code.splitlines()
        blocks.append("\n".join(lines).strip("\n"))
    return blocks


def run_block(code: str, timeout: int):
    """
    在独立的临时工作目录中运行单个代码块。
    使用文件句柄重定向 stdout/stderr（不经过管道），
    并设置 PYTHONUTF8=1 保证中文/emoji 输出不乱码。
    返回 (是否成功, stderr 文本, stdout 文本)。
    """
    tmp_base = BOOK_DIR / ".verify_tmp"
    try:
        tmp_base.mkdir(exist_ok=True)
    except OSError:
        # 兜底：书目录下创建失败时退回系统临时目录
        tmp_base = pathlib.Path(tempfile.gettempdir())
    work_dir = tmp_base
    # 用 PID 区分文件名，避免多个验证进程（如并行写作的子代理）互相踩踏
    pid = os.getpid()
    src = work_dir / ("block_%d.py" % pid)
    out = work_dir / ("stdout_%d.txt" % pid)
    err = work_dir / ("stderr_%d.txt" % pid)
    src.write_text(code, encoding="utf-8")
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        with out.open("wb") as fo, err.open("wb") as fe:
            proc = subprocess.run(
                [sys.executable, str(src)],
                cwd=str(work_dir),
                env=env,
                stdout=fo,
                stderr=fe,
                timeout=timeout,
            )
    except subprocess.TimeoutExpired:
        return False, "[TIMEOUT] 代码块超过 %d 秒未结束（可能有死循环或阻塞调用）" % timeout, ""
    stdout = out.read_text(encoding="utf-8", errors="replace")
    stderr = err.read_text(encoding="utf-8", errors="replace")
    return proc.returncode == 0, stderr, stdout


def collect_md_files(patterns):
    if not patterns:
        patterns = ["*.md"]
    files = []
    for p in patterns:
        if not re.search(r"[*?\[\]]", p):
            files.append(BOOK_DIR / p)
        else:
            files.extend(pathlib.Path(BOOK_DIR).glob(p))
    # 去重并保持稳定顺序（按文件名排序）
    seen, ordered = set(), []
    for f in files:
        key = str(f.resolve())
        if key not in seen:
            seen.add(key)
            ordered.append(f)
    return sorted(ordered, key=lambda f: f.name)


def main():
    parser = argparse.ArgumentParser(description="验证书中的所有 Python 代码块")
    parser.add_argument("--files", nargs="*", default=None, help="要验证的文件名/通配符，默认全部 *.md")
    parser.add_argument("--list", action="store_true", help="只统计代码块数量，不运行")
    parser.add_argument("--timeout", type=int, default=30, help="单个代码块超时秒数，默认 30")
    parser.add_argument("--show", action="store_true", help="失败时打印完整代码")
    parser.add_argument("--verbose", action="store_true", help="成功时也打印运行输出")
    parser.add_argument("--exit-zero", action="store_true", help="即使有失败也以退出码 0 结束（CI 用）")
    args = parser.parse_args()

    # 无论控制台/管道编码如何，脚本自身的输出统一用 UTF-8
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    md_files = collect_md_files(args.files)
    if not md_files:
        print("没有找到 Markdown 文件。")
        sys.exit(1 if not args.exit_zero else 0)

    if args.list:
        total = 0
        for f in md_files:
            blocks = extract_blocks(f)
            total += len(blocks)
            print("%-46s %3d 个代码块" % (f.name, len(blocks)))
        print("-" * 60)
        print("共 %d 个文件，%d 个代码块" % (len(md_files), total))
        return

    print("=" * 66)
    print("《Python 设计模式修炼手册》代码验证开始")
    print("Python 版本：%s" % sys.version.split()[0])
    print("=" * 66)

    ok_count = fail_count = 0
    failures = []

    for md in md_files:
        blocks = extract_blocks(md)
        for idx, code in enumerate(blocks, start=1):
            ok, stderr, stdout = run_block(code, args.timeout)
            if ok:
                ok_count += 1
                print("[ OK ] %-42s #%02d" % (md.name, idx))
                if args.verbose and stdout.strip():
                    print("       └─ 输出: %s" % stdout.strip().replace("\n", " / "))
            else:
                fail_count += 1
                print("[FAIL] %-42s #%02d" % (md.name, idx))
                err_tail = stderr.strip().splitlines()
                for line in err_tail[-8:]:
                    print("       | " + line)
                if args.show:
                    print("       └─ 完整代码:")
                    for line in code.splitlines():
                        print("          " + line)
                failures.append((md, idx, stderr))

    print("=" * 66)
    print("结果：%d 通过，%d 失败，共 %d 个代码块（%d 个文件）" % (
        ok_count, fail_count, ok_count + fail_count, len(md_files)))
    if failures:
        print("\n失败的代码块：")
        for md, idx, _ in failures:
            print("  - %s #%02d" % (md.name, idx))
    print("=" * 66)
    sys.exit(0 if (fail_count == 0 or args.exit_zero) else 1)


if __name__ == "__main__":
    main()
