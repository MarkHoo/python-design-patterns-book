# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #7：4.3 自定义 `__copy__` / `__deepcopy__`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class DatabaseConnection:
    """数据库连接：复制时只复制"配置"，连接资源直接复用"""
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._socket = f"<socket {host}:{port}>"  # 模拟真实的连接资源
    def __deepcopy__(self, memo):
        """深拷贝时只复制配置，不复制连接资源本身"""
        print(f"深拷贝 {self.host}:{self.port}，连接资源复用")
        new = DatabaseConnection(self.host, self.port)
        new._socket = self._socket   # 关键：复用同一个连接资源
        memo[id(self)] = new
        return new
    def __repr__(self):
        return f"<DB {self.host}:{self.port} {self._socket}>"


class Player:
    """自定义 __copy__：浅拷贝时只复制部分字段"""
    def __init__(self, name, level, inventory):
        self.name = name
        self.level = level
        self.inventory = inventory  # 背包列表
    def __copy__(self):
        """浅拷贝：只复制名字和等级，背包给个新的空列表"""
        print("调用自定义 __copy__")
        return Player(self.name, self.level, [])
    def __repr__(self):
        return f"<Player {self.name} Lv{self.level} 背包={self.inventory}>"


conn = DatabaseConnection("192.168.1.1", 3306)
conn_copy = copy.deepcopy(conn)
print("原连接：", conn)
print("复制品：", conn_copy)
print("连接资源被复用（同一个 socket）:", conn._socket is conn_copy._socket)

p = Player("阿伟", 10, ["木剑", "药水"])
p2 = copy.copy(p)
p2.inventory.append("屠龙刀")
print("原版：", p)
print("复制品：", p2)
