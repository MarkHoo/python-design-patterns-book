# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》19-中介者模式-Mediator
# 代码块 #8：误区 3：同事之间偷偷直接引用
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面教材：同事之间"私通"——绕过中介者直接引用
class User:
    def __init__(self, name, room):
        self.name = name
        self.room = room
        self.secret_friend = None
    def send(self, message):
        self.room.broadcast(self.name, message)
    def send_secret(self, message):
        # 绕过中介者直接私聊——中介者再也管不到这条消息
        self.secret_friend.receive(self.name, message)
    def receive(self, sender, message):
        print(f"{self.name} 收到 {sender}：{message}")


class Room:
    def __init__(self):
        self.users = []
    def join(self, user):
        self.users.append(user)
    def broadcast(self, sender, message):
        for u in self.users:
            if u.name != sender:
                u.receive(sender, message)


room = Room()
a = User("阿伟", room)
b = User("小明", room)
room.join(a)
room.join(b)
a.secret_friend = b
a.send_secret("别告诉别人")
print("问题：这种消息没人记录、没人审计，中介者形同虚设")
