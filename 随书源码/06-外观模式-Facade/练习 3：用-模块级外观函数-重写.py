# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #13：练习 3：用"模块级外观函数"重写
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：模块级外观——公共 API 只有一个 play()
def _find_file(name: str) -> None:
    print(f"查找文件：{name}")


def _load_subtitle(name: str) -> None:
    print(f"加载字幕：{name}.srt")


def _set_audio(track: str) -> None:
    print(f"设置音轨：{track}")


def _play(name: str) -> None:
    print(f"正在播放：{name}")


def play(movie: str, audio: str = "国语") -> None:
    """模块的对外 API——外观函数"""
    _find_file(movie)
    _load_subtitle(movie)
    _set_audio(audio)
    _play(movie)


play("流浪地球", audio="粤语")
