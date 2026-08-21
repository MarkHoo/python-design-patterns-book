# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #11：误区 3：工厂方法忘记返回"抽象类型"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面：工厂方法返回具体类，调用方被迫依赖实现细节
class Notifier:
    def send(self, msg):
        print(f"通知：{msg}")


class EmailNotifier(Notifier):
    def send(self, msg):
        print(f"邮件：{msg}")


class BadFactory:
    def create(self) -> EmailNotifier:   # 返回类型写死成具体类
        return EmailNotifier()


# 想换 SmsNotifier？create 的签名、调用方的类型标注都要跟着改
class SmsNotifier(Notifier):
    def send(self, msg):
        print(f"短信：{msg}")


class GoodFactory:
    def create(self) -> Notifier:        # 返回抽象类型，替换无感
        return SmsNotifier()


print(type(BadFactory().create()).__name__)
print(type(GoodFactory().create()).__name__)
