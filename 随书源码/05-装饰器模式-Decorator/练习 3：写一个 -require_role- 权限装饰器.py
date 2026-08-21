# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #17：练习 3：写一个 `require_role` 权限装饰器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def require_role(allowed_roles):
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if user["role"] not in allowed_roles:
                return f"拒绝访问：{user['name']} 没有权限（需要角色：{'/'.join(allowed_roles)}）"
            return func(user, *args, **kwargs)
        return wrapper
    return decorator


@require_role(["admin"])
def delete_user(user, target: str) -> str:
    return f"{user['name']} 删除了用户 {target}"


admin = {"name": "管理员", "role": "admin"}
guest = {"name": "访客", "role": "guest"}
print(delete_user(admin, "小明"))
print(delete_user(guest, "小明"))
