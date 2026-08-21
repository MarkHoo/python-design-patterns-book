# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #2：3.1 经典版：下单系统一条龙
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Inventory:
    """库存子系统"""

    def check(self, sku: str, qty: int) -> bool:
        print(f"  库存：检查 {sku} x{qty}")
        return qty <= 10

    def reduce(self, sku: str, qty: int) -> None:
        print(f"  库存：扣减 {sku} x{qty}")


class Payment:
    """支付子系统"""

    def pay(self, order_id: str, amount: float) -> bool:
        print(f"  支付：订单 {order_id} 收款 {amount} 元")
        return True


class Logistics:
    """物流子系统"""

    def ship(self, order_id: str, address: str) -> None:
        print(f"  物流：订单 {order_id} 发往 {address}")


class OrderFacade:
    """外观：把三个子系统串成一条龙服务"""

    def __init__(self):
        self._inventory = Inventory()
        self._payment = Payment()
        self._logistics = Logistics()

    def place_order(self, sku: str, qty: int, amount: float, address: str) -> str:
        """对外只暴露一个方法：下单"""
        if not self._inventory.check(sku, qty):
            raise ValueError(f"{sku} 库存不足")
        self._inventory.reduce(sku, qty)
        order_id = f"ORD-{sku}-{qty}"
        if not self._payment.pay(order_id, amount):
            raise RuntimeError("支付失败")
        self._logistics.ship(order_id, address)
        return f"下单成功，订单号 {order_id}"


facade = OrderFacade()
print(facade.place_order("P001", 2, 199.0, "上海市浦东新区"))

# 库存不足的情况：外观负责把"流程中断"翻译成清晰的错误
try:
    facade.place_order("P999", 99, 1.0, "火星基地")
except ValueError as e:
    print("下单被拒：", e)
