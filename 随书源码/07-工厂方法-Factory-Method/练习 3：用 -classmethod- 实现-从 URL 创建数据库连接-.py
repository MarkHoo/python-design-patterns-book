# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #14：练习 3：用 `classmethod` 实现"从 URL 创建数据库连接"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：classmethod 工厂方法——把"如何解析配置"交给类自己
class DbConnection:
    def __init__(self, host: str, port: int, db: str):
        self.host, self.port, self.db = host, port, db

    @classmethod
    def from_url(cls, url: str) -> "DbConnection":
        """工厂方法：从 URL 解析出连接参数"""
        # 形如 mysql://127.0.0.1:3306/orders
        scheme, rest = url.split("://")
        host_port, db = rest.split("/")
        host, port = host_port.split(":")
        return cls(host, int(port), db)

    def __repr__(self):
        return f"<DbConnection {self.host}:{self.port}/{self.db}>"


conn = DbConnection.from_url("mysql://127.0.0.1:3306/orders")
print(conn)
