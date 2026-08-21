# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #7：4.3 适配 `collections.abc` 协议：让自定义类支持 `len()` / `iter()`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from collections.abc import Sequence

class Playlist(Sequence):
    """把歌单适配成序列协议：支持 len()、下标、in、遍历"""

    def __init__(self, songs):
        self._songs = list(songs)

    def __len__(self):
        return len(self._songs)

    def __getitem__(self, index):
        return self._songs[index]

songs = Playlist(["晴天", "七里香", "稻香"])
print(f"共 {len(songs)} 首")                # len() 来自 __len__
print("第 2 首：", songs[1])                # 下标来自 __getitem__
print("'晴天' 在歌单里吗：", "晴天" in songs)  # in 由 Sequence 自动补全
print("遍历：", " / ".join(songs))          # 迭代由 Sequence 自动补全
