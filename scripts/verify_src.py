#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《Python 设计模式修炼手册》随书源码验证脚本

逐一运行「随书源码/」目录下导出的所有 .py 文件（每个文件独立进程、
独立工作目录），确认每个文件都能独立运行。与 scripts/verify_code.py
（验证 Markdown 代码块）互为印证：两边都通过，即"书中代码 = 源码文件"
且全部可运行。

用法：
    python scripts/verify_src.py
    python scripts/verify_src.py --files "01-单例模式-Singleton/*.py"
"""

import argparse
import os
import pathlib
import subprocess
import sys

BOOK_DIR = pathlib.Path(__file__).resolve().parent.parent
SRC_DIR = BOOK_DIR / "随书源码"
WORK_DIR = BOOK_DIR / ".verify_tmp"


def collect(patterns):
    if not patterns:
        return sorted(SRC_DIR.rglob("*.py"))
    files = []
    for p in patterns:
        files.extend(SRC_DIR.glob(p))
    return sorted(set(files))


def run_one(py_file, timeout=30):
    """独立进程运行，输出重定向到文件（避开管道限制）"""
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    out = WORK_DIR / ("src_out.txt")
    err = WORK_DIR / ("src_err.txt")
    try:
        with out.open("wb") as fo, err.open("wb") as fe:
            proc = subprocess.run(
                [sys.executable, str(py_file)],
                cwd=str(WORK_DIR),
                env=env,
                stdout=fo,
                stderr=fe,
                timeout=timeout,
            )
    except subprocess.TimeoutExpired:
        return False, "[TIMEOUT] 超过 %d 秒未结束" % timeout
    stderr = err.read_text(encoding="utf-8", errors="replace")
    return proc.returncode == 0, stderr


def main():
    parser = argparse.ArgumentParser(description="验证随书源码目录中的所有文件")
    parser.add_argument("--files", nargs="*", default=None, help="相对随书源码/ 的通配，默认全部")
    parser.add_argument("--show", action="store_true", help="失败时打印错误详情")
    args = parser.parse_args()

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    WORK_DIR.mkdir(exist_ok=True)
    files = collect(args.files)
    if not files:
        print("没有找到文件。先运行 scripts/export_src.py 导出随书源码。")
        sys.exit(1)

    ok = fail = 0
    failures = []
    for f in files:
        good, stderr = run_one(f)
        rel = f.relative_to(SRC_DIR)
        if good:
            ok += 1
            print("[ OK ] %s" % rel)
        else:
            fail += 1
            failures.append((rel, stderr))
            print("[FAIL] %s" % rel)
            if args.show:
                for line in stderr.strip().splitlines()[-8:]:
                    print("       | " + line)

    print("=" * 60)
    print(f"结果：{ok} 通过，{fail} 失败，共 {ok + fail} 个文件")
    if failures:
        for rel, _ in failures:
            print("  - " + str(rel))
    print("=" * 60)
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
