# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #11：练习 1：给文件服务写一个保护代理
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：保护代理
class FileService:
    def read(self, filename):
        return f"{filename} 的内容"

    def delete(self, filename):
        return f"{filename} 已删除"

class SecureFileProxy:
    """保护代理：部门匹配才能读，一律不能删"""

    def __init__(self, service, user, department):
        self._service = service
        self._user = user
        self._department = department

    def read(self, filename):
        if self._department not in filename:
            return f"拒绝：{self._user} 无权读取 {filename}"
        return self._service.read(filename)

    def delete(self, filename):
        return f"拒绝：普通员工没有删除权限"

svc = FileService()
proxy = SecureFileProxy(svc, "小王", "研发部")
print(proxy.read("研发部-需求文档.md"))
print(proxy.read("财务部-工资表.xlsx"))
print(proxy.delete("研发部-需求文档.md"))
