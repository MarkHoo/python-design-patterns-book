# -*- coding: utf-8 -*-
"""构建静态网站数据：直接读取各章节文件 → site/data/*.js（无需合并版）
用法: python build_site.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))  # site/tools
SITE = os.path.dirname(BASE)                        # site
BOOK = os.path.dirname(SITE)                        # python-design-patterns-book
DATA_DIR = os.path.join(SITE, 'data')

# 章节文件（顺序即网站目录顺序）：key = 文件名去 .md
CHAPTER_FILES = [
    'README.md',
    '00-导读-设计模式入门.md',
    '01-单例模式-Singleton.md', '02-简单工厂-Simple-Factory.md',
    '03-策略模式-Strategy.md', '04-迭代器模式-Iterator.md',
    '05-装饰器模式-Decorator.md', '06-外观模式-Facade.md',
    '07-工厂方法-Factory-Method.md', '08-模板方法-Template-Method.md',
    '09-观察者模式-Observer.md', '10-适配器模式-Adapter.md',
    '11-建造者模式-Builder.md', '12-代理模式-Proxy.md',
    '13-责任链模式-Chain-of-Responsibility.md', '14-抽象工厂-Abstract-Factory.md',
    '15-命令模式-Command.md', '16-状态模式-State.md',
    '17-组合模式-Composite.md', '18-原型模式-Prototype.md',
    '19-中介者模式-Mediator.md', '20-备忘录模式-Memento.md',
    '21-桥接模式-Bridge.md', '22-访问者模式-Visitor.md',
    '23-享元模式-Flyweight.md', '24-解释器模式-Interpreter.md',
    '25-结语-模式不是银弹.md',
    '26-附录A-24模式速查表.md',
]


def js_escape(text):
    """转义为 JS 单引号字符串内容"""
    text = text.replace('\\', '\\\\')
    text = text.replace("'", "\\'")
    text = text.replace('\r', '')
    text = text.replace('\n', '\\n')
    text = text.replace('</script>', '<\\/script>')
    return text


def main():
    blocks = []
    for fname in CHAPTER_FILES:
        path = os.path.join(BOOK, fname)
        if not os.path.isfile(path):
            print('缺少章节文件:', fname)
            return 1
        with open(path, encoding='utf-8') as fh:
            blocks.append((fname[:-3], fh.read().strip()))

    # 清空旧数据
    os.makedirs(DATA_DIR, exist_ok=True)
    for f in os.listdir(DATA_DIR):
        if f.endswith('.js'):
            os.remove(os.path.join(DATA_DIR, f))

    for name, block in blocks:
        escaped = js_escape(block)
        js = "window.BOOK_DATA = window.BOOK_DATA || {};\nwindow.BOOK_DATA['%s'] = '%s';\n" % (name, escaped)
        with open(os.path.join(DATA_DIR, name + '.js'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(js)

    print('生成数据文件: %d 个' % len(blocks))
    for name, block in blocks:
        print('  %s (%d 字符)' % (name, len(block)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
