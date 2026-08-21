# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #7：标准库：`unittest.TestCase` 的 `setUp` / `tearDown`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import unittest


class ShoppingCartTest(unittest.TestCase):
    """unittest 就是模板方法：setUp/tearDown 是钩子"""

    def setUp(self):           # 钩子：每个用例执行前调用
        print("  钩子 setUp：准备购物车")
        self.cart = ["苹果", "香蕉"]

    def tearDown(self):        # 钩子：每个用例执行后调用
        print("  钩子 tearDown：清理购物车")
        self.cart = None

    def test_add_item(self):
        self.cart.append("橘子")
        self.assertEqual(len(self.cart), 3)

    def test_remove_item(self):
        self.cart.remove("苹果")
        self.assertEqual(len(self.cart), 1)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(ShoppingCartTest)
result = unittest.TestResult()           # 只收集结果，不做进度输出
suite.run(result)

print("用例数：", result.testsRun)
print("失败数：", len(result.failures))
print("错误数：", len(result.errors))
print("全部通过：", result.wasSuccessful())
