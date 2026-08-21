# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》14-抽象工厂-Abstract-Factory
# 代码块 #3：3.2 数据库方言版：连接 + 查询 + 转义
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from abc import ABC, abstractmethod


class Connection(ABC):
    @abstractmethod
    def execute(self, sql: str) -> str:
        raise NotImplementedError


class SQLBuilder(ABC):
    @abstractmethod
    def quote_identifier(self, name: str) -> str:
        raise NotImplementedError


class MySQLConnection(Connection):
    def __init__(self, host: str):
        self.host = host

    def execute(self, sql: str) -> str:
        return f"[MySQL] 在 {self.host} 上执行：{sql}"


class PostgreSQLConnection(Connection):
    def __init__(self, host: str):
        self.host = host

    def execute(self, sql: str) -> str:
        return f"[PostgreSQL] 在 {self.host} 上执行：{sql}"


class MySQLBuilder(SQLBuilder):
    def quote_identifier(self, name: str) -> str:
        return f"`{name}`"        # MySQL 用反引号


class PostgreSQLBuilder(SQLBuilder):
    def quote_identifier(self, name: str) -> str:
        return f'"{name}"'        # PostgreSQL 用双引号


class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self, host: str) -> Connection:
        raise NotImplementedError

    @abstractmethod
    def create_sql_builder(self) -> SQLBuilder:
        raise NotImplementedError


class MySQLFactory(DatabaseFactory):
    def create_connection(self, host: str) -> Connection:
        return MySQLConnection(host)

    def create_sql_builder(self) -> SQLBuilder:
        return MySQLBuilder()


class PostgreSQLFactory(DatabaseFactory):
    def create_connection(self, host: str) -> Connection:
        return PostgreSQLConnection(host)

    def create_sql_builder(self) -> SQLBuilder:
        return PostgreSQLBuilder()


def query_users(factory: DatabaseFactory, host: str, table: str) -> None:
    """同一段业务代码，跑在哪个数据库上由工厂决定"""
    conn = factory.create_connection(host)
    builder = factory.create_sql_builder()
    sql = f"SELECT * FROM {builder.quote_identifier(table)} WHERE id = ?"
    print(conn.execute(sql))


print("=== 业务代码跑在 MySQL 上 ===")
query_users(MySQLFactory(), "db-mysql-01", "users")
print("=== 业务代码跑在 PostgreSQL 上 ===")
query_users(PostgreSQLFactory(), "db-pg-01", "users")
