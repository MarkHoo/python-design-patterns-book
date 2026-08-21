# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》00-导读-设计模式入门
# 代码块 #4：① 单一职责原则（SRP）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面教材：一个类包揽所有事
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def save_to_db(self) -> None:          # 职责 1：存储
        print(f"把 {self.name} 存入数据库")

    def send_welcome_email(self) -> None:  # 职责 2：邮件
        print(f"给 {self.email} 发欢迎邮件")

    def export_report(self) -> None:       # 职责 3：报表
        print(f"导出 {self.name} 的报表")


# 正确姿势：拆成三个各司其职的类
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class UserRepository:
    def save(self, user: User) -> None:
        print(f"把 {user.name} 存入数据库")


class EmailService:
    def send_welcome(self, user: User) -> None:
        print(f"给 {user.email} 发欢迎邮件")


user = User("小明", "xiaoming@example.com")
UserRepository().save(user)
EmailService().send_welcome(user)
