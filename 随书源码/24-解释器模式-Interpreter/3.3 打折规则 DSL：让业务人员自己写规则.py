# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #4：3.3 打折规则 DSL：让业务人员自己写规则
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 规则 DSL："周末 打 8 折" 这种话，让解释器来读懂
def tokenize_rule(text: str) -> list:
    """词法：把规则字符串切成记号"""
    tokens = []
    for word in text.split():
        if word in ("周末", "工作日", "会员", "非会员", "打", "折"):
            tokens.append(("KW", word))
        elif word.isdigit():
            tokens.append(("NUM", int(word)))
        else:
            raise ValueError(f"未知词：{word}")
    tokens.append(("END", ""))
    return tokens

def parse_rule(tokens: list):
    """语法：'条件 打 N 折' → ('折扣', 条件, N)"""
    cond = tokens[0][1]
    if tokens[1] != ("KW", "打") or tokens[2][0] != "NUM":
        raise ValueError("规则格式应为：条件 打 N 折")
    return ("折扣", cond, tokens[2][1])

def apply_rule(rule, is_weekend: bool, is_vip: bool) -> float:
    """求值：根据实际场景算出这条规则打几折（不匹配就是不打折）"""
    _, cond, discount = rule
    match = {
        "周末": is_weekend,
        "工作日": not is_weekend,
        "会员": is_vip,
        "非会员": not is_vip,
    }[cond]
    return discount / 10 if match else 1.0

def final_discount(rules, is_weekend: bool, is_vip: bool) -> float:
    """多条规则都生效时，取最优惠的折扣"""
    return min(apply_rule(r, is_weekend, is_vip) for r in rules)

rules = [
    parse_rule(tokenize_rule("周末 打 8 折")),
    parse_rule(tokenize_rule("会员 打 9 折")),
]
print("周六 + 会员：", final_discount(rules, True, True))
print("周六 + 非会员：", final_discount(rules, True, False))
print("周二 + 会员：", final_discount(rules, False, True))
print("周二 + 非会员：", final_discount(rules, False, False))
