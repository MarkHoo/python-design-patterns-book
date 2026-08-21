# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #10：误区 2：滥用工厂——简单场景也套工厂
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面：只有一个实现也套工厂——为了模式而模式
class Database:
    def connect(self):
        print("连接数据库")


class DatabaseFactory:
    """就一个产品，工厂毫无存在意义"""
    def create(self):
        return Database()


Database().connect()                 # 直接 new 就完了
DatabaseFactory().create().connect() # 工厂版没带来任何灵活性
