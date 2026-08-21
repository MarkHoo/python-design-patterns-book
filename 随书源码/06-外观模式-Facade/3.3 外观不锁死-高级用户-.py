# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #4：3.3 外观不锁死"高级用户"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Projector:
    def on(self) -> None:
        print("投影仪：开机")


class Curtain:
    def close(self) -> None:
        print("窗帘：拉上")


class Light:
    def dim(self, percent: int) -> None:
        print(f"灯光：{percent}%")


class HomeTheaterFacade:
    """外观：一键观影"""

    def __init__(self):
        self.projector = Projector()
        self.curtain = Curtain()
        self.light = Light()

    def watch_movie(self, movie: str) -> None:
        print(f"===== 观影《{movie}》 =====")
        self.light.dim(10)
        self.curtain.close()
        self.projector.on()


# 普通用户：走外观，一条命令搞定
HomeTheaterFacade().watch_movie("功夫熊猫")

# 高级用户：不买外观的账，直接操作子系统——外观从不阻止你
print("——下午只想拉窗帘、不开投影——")
Curtain().close()
Light().dim(60)
