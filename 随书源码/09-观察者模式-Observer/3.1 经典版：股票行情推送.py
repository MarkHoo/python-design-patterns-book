# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #2：3.1 经典版：股票行情推送
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import abc


class Observer(abc.ABC):
    """观察者接口：所有想被通知的对象都实现 update"""

    @abc.abstractmethod
    def update(self, symbol: str, price: float) -> None:
        pass


class StockMarket:
    """被观察者（主题）：维护观察者列表，行情一变就广播"""

    def __init__(self):
        self._observers = []
        self._prices = {}

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def set_price(self, symbol: str, price: float) -> None:
        self._prices[symbol] = price
        print(f"【行情】{symbol} 最新价 {price}")
        self._notify(symbol, price)

    def _notify(self, symbol: str, price: float) -> None:
        for observer in self._observers:
            observer.update(symbol, price)


class AppClient(Observer):
    """手机 App 客户端"""

    def update(self, symbol: str, price: float) -> None:
        print(f"  [App] {symbol} 价格变动提醒：{price}")


class BigScreen(Observer):
    """交易所大屏"""

    def update(self, symbol: str, price: float) -> None:
        print(f"  [大屏] 滚动显示 {symbol}：{price}")


market = StockMarket()
app = AppClient()
screen = BigScreen()
market.attach(app)
market.attach(screen)

market.set_price("AAPL", 188.5)
market.detach(app)          # 注销：App 不再接收通知
market.set_price("AAPL", 190.2)
