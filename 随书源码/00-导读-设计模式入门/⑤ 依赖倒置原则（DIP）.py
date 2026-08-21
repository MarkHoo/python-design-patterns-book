# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》00-导读-设计模式入门
# 代码块 #8：⑤ 依赖倒置原则（DIP）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面教材：业务代码直接 new 一个 MySQL 连接
class ReportGeneratorV1:
    def generate(self) -> None:
        db = MySQLDatabase()          # 想换成 PostgreSQL？改业务代码！
        data = db.query("SELECT * FROM sales")
        print(f"生成报表：{data}")


class MySQLDatabase:
    def query(self, sql: str) -> str:
        return f"MySQL 返回了 {sql} 的结果"


# 正确姿势：业务代码只认抽象接口
class Database:
    def query(self, sql: str) -> str: ...


class MySQLDatabase(Database):
    def query(self, sql: str) -> str:
        return f"MySQL 返回了 {sql} 的结果"


class PostgreSQLDatabase(Database):
    def query(self, sql: str) -> str:
        return f"PostgreSQL 返回了 {sql} 的结果"


class ReportGenerator:
    def __init__(self, db: Database):   # 依赖注入：数据库从外面给
        self._db = db

    def generate(self) -> None:
        data = self._db.query("SELECT * FROM sales")
        print(f"生成报表：{data}")


ReportGenerator(MySQLDatabase()).generate()
ReportGenerator(PostgreSQLDatabase()).generate()
