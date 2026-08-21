# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #12：练习 2：用"列表 + 循环"实现用户名校验链
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：列表 + 循环（校验链）
def check_length(text):
    if len(text) < 4:
        return "太短，至少 4 个字符"
    return None

def check_blacklist(text):
    if text in {"admin", "root"}:
        return "该用户名被禁止"
    return None

def check_format(text):
    if not text.isalnum():
        return "只能包含字母和数字"
    return None

checks = [check_length, check_blacklist, check_format]

def validate(username):
    for check in checks:
        error = check(username)
        if error:
            return f"用户名 {username!r}：{error}"
    return f"用户名 {username!r} 校验通过"

for name in ("ab", "admin", "hello!", "python123"):
    print(validate(name))
