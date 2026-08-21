# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》19-中介者模式-Mediator
# 代码块 #2：3.1 经典版：聊天室
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class ChatRoom:
    """中介者：聊天室，负责在用户之间转发消息"""
    def __init__(self):
        self.users = []
    def join(self, user):
        self.users.append(user)
        user.room = self
        for other in self.users:
            if other is not user:
                other.receive("系统", f"{user.name} 加入了群聊")
    def broadcast(self, sender, message):
        for user in self.users:
            if user is not sender:
                user.receive(sender.name, message)


class User:
    """同事：用户不直接找别人说话，都通过聊天室"""
    def __init__(self, name):
        self.name = name
        self.room = None
    def send(self, message):
        print(f"[{self.name} 发言] {message}")
        self.room.broadcast(self, message)
    def receive(self, sender, message):
        print(f"{self.name} 收到来自 {sender} 的消息：{message}")


room = ChatRoom()
alice = User("爱丽丝")
bob = User("鲍勃")
carol = User("卡罗尔")
for u in (alice, bob, carol):
    room.join(u)
alice.send("今晚吃火锅？")
bob.send("走起！")
