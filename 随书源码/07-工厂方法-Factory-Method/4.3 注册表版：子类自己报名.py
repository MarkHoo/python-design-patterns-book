# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #7：4.3 注册表版：子类自己报名
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class MessageEncoder:
    """产品基类 + 注册表：子类注册自己，create 按名字造"""

    _registry = {}

    @classmethod
    def register(cls, name: str):
        """装饰器：把子类登记进注册表"""
        def decorator(subclass):
            cls._registry[name] = subclass
            return subclass
        return decorator

    @classmethod
    def create(cls, name: str) -> "MessageEncoder":
        """工厂方法：按名字查注册表创建"""
        if name not in cls._registry:
            raise ValueError(f"未知编码器：{name}")
        return cls._registry[name]()

    def encode(self, text: str) -> str:
        raise NotImplementedError


@MessageEncoder.register("plain")
class PlainEncoder(MessageEncoder):
    def encode(self, text: str) -> str:
        return text


@MessageEncoder.register("upper")
class UpperEncoder(MessageEncoder):
    def encode(self, text: str) -> str:
        return text.upper()


# 新增编码器：加一个带 @register 的类即可，create 不用改
@MessageEncoder.register("reverse")
class ReverseEncoder(MessageEncoder):
    def encode(self, text: str) -> str:
        return text[::-1]


for name in ("plain", "upper", "reverse"):
    encoder = MessageEncoder.create(name)
    print(f"{name:>7}：{encoder.encode('你好世界')}")
