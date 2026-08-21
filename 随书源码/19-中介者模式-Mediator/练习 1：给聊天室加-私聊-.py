# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》19-中介者模式-Mediator
# 代码块 #9：练习 1：给聊天室加"私聊"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class ChatRoom:
    def __init__(self):
        self.users = {}
    def join(self, user):
        self.users[user.name] = user
        user.room = self
    def broadcast(self, sender, message):
        for name, user in self.users.items():
            if name != sender.name:
                user.receive(sender.name, message)
    def whisper(self, sender, target_name, message):
        target = self.users.get(target_name)
        if target:
            target.receive(f"{sender.name}(私聊)", message)
        else:
            print(f"{sender.name}：{target_name} 不在线，消息发送失败")


class User:
    def __init__(self, name):
        self.name = name
        self.room = None
    def send(self, message):
        self.room.broadcast(self, message)
    def whisper(self, target, message):
        self.room.whisper(self, target, message)
    def receive(self, sender, message):
        print(f"{self.name} 收到 {sender}：{message}")


room = ChatRoom()
a = User("爱丽丝")
b = User("鲍勃")
room.join(a)
room.join(b)
a.send("大家好")
a.whisper("鲍勃", "晚上一起吃饭吗？")
a.whisper("查尔斯", "在吗？")
