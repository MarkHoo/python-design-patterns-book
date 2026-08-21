# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》19-中介者模式-Mediator
# 代码块 #7：误区 1：中介者变成"上帝对象"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面教材：上帝中介者——什么逻辑都往里塞
class GodMediator:
    """中介者包揽一切：校验、存储、通知、日志……越写越长"""
    def on_login_click(self, username, password):
        if len(username) < 3:
            print("用户名太短")
            return
        if password != "123456":
            print("密码错误")
            return
        self._save_to_db(username)
        self._send_welcome(username)
        self._write_log(username)
    def _save_to_db(self, username):
        print(f"保存 {username} 到数据库")
    def _send_welcome(self, username):
        print(f"给 {username} 发欢迎邮件")
    def _write_log(self, username):
        print(f"记录日志：{username} 登录")


GodMediator().on_login_click("王小明", "123456")
