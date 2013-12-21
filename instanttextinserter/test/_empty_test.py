# encoding: shift-jis

import unittest

#import hoge #テスト対象モジュール

class HogeTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testhoge(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
