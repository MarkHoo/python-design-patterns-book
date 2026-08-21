# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #3：3.2 变体：图片解码器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import abc


class ImageDecoder(abc.ABC):
    """产品：图片解码器"""

    @abc.abstractmethod
    def decode(self, data: bytes) -> str:
        pass


class PngDecoder(ImageDecoder):
    def decode(self, data: bytes) -> str:
        return f"PNG 图片，{len(data)} 字节，支持透明通道"


class JpgDecoder(ImageDecoder):
    def decode(self, data: bytes) -> str:
        return f"JPEG 图片，{len(data)} 字节，适合照片"


class WebpDecoder(ImageDecoder):
    def decode(self, data: bytes) -> str:
        return f"WebP 图片，{len(data)} 字节，体积更小"


class ImageDecoderFactory(abc.ABC):
    """抽象工厂：负责产出解码器"""

    @abc.abstractmethod
    def create_decoder(self) -> ImageDecoder:
        pass


class PngDecoderFactory(ImageDecoderFactory):
    def create_decoder(self) -> ImageDecoder:
        return PngDecoder()


class JpgDecoderFactory(ImageDecoderFactory):
    def create_decoder(self) -> ImageDecoder:
        return JpgDecoder()


class WebpDecoderFactory(ImageDecoderFactory):
    def create_decoder(self) -> ImageDecoder:
        return WebpDecoder()


# 客户端只认抽象：新增格式 = 新增一对类，旧代码不动
def decode_file(data: bytes, factory: ImageDecoderFactory) -> str:
    decoder = factory.create_decoder()   # 工厂方法
    return decoder.decode(data)


print(decode_file(b"\x89PNG\r\n\x1a\n" + b"0" * 100, PngDecoderFactory()))
print(decode_file(b"\xff\xd8\xff\xe0" + b"0" * 100, JpgDecoderFactory()))
print(decode_file(b"RIFF" + b"0" * 64, WebpDecoderFactory()))
