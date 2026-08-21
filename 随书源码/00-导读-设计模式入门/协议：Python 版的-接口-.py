# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》00-导读-设计模式入门
# 代码块 #3：协议：Python 版的"接口"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Playlist:
    """一个能像列表一样被遍历的歌单"""

    def __init__(self, songs: list[str]):
        self._songs = songs

    def __len__(self) -> int:
        return len(self._songs)

    def __getitem__(self, index: int) -> str:
        return self._songs[index]


pl = Playlist(["晴天", "七里香", "稻香"])
for song in pl:          # 没有 __iter__，但 Python 会退而求其次用 __getitem__
    print(f"播放：{song}")
print(f"共 {len(pl)} 首")
