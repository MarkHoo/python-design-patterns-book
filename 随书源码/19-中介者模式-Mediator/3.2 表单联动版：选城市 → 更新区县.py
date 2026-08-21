# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》19-中介者模式-Mediator
# 代码块 #3：3.2 表单联动版：选城市 → 更新区县
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class FormMediator:
    """表单中介者：协调省/市/区三个下拉框联动"""
    def __init__(self):
        self.province = None
        self.city = None
        self.district = None
        self.data = {
            "广东省": {"广州市": ["天河区", "越秀区"], "深圳市": ["南山区", "福田区"]},
            "浙江省": {"杭州市": ["西湖区", "滨江区"], "宁波市": ["海曙区", "鄞州区"]},
        }
    def on_province_changed(self, province):
        cities = list(self.data.get(province, {}).keys())
        self.city.select(cities[0] if cities else None)
        self.on_city_changed(cities[0] if cities else None)
    def on_city_changed(self, city):
        districts = []
        for cities in self.data.values():
            if city in cities:
                districts = cities[city]
                break
        self.district.select(districts[0] if districts else None)


class SelectBox:
    """同事：下拉框，不直接认识其他下拉框"""
    def __init__(self, name, mediator):
        self.name = name
        self.mediator = mediator
    def select(self, value):
        print(f"{self.name} 选中：{value}")
    def user_select(self, value):
        """用户手动选择：通知中介者协调其他框"""
        self.select(value)
        if self.name == "省":
            self.mediator.on_province_changed(value)
        elif self.name == "市":
            self.mediator.on_city_changed(value)


mediator = FormMediator()
province = SelectBox("省", mediator)
city = SelectBox("市", mediator)
district = SelectBox("区", mediator)
mediator.province, mediator.city, mediator.district = province, city, district

province.user_select("广东省")
print("---")
city.user_select("深圳市")
