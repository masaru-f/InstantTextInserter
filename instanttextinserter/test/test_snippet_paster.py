# encoding: shift-jis

import os
import unittest

import snippet_paster

class SnippetPasterTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_cursorbackcount(self):
        """
        何文字戻ればカーソル位置(を表す文字列の部分)に来るかを計算.
        """
        paster = snippet_paster.SnippetPaster()
        testeefunc = paster.get_cursorbackcount
        cs = snippet_paster.SnippetPaster.CURSOR_STRING

        def test(testeefunc, testdata, expect):
            print "CASE:" + testdata
            self.assertEqual(expect, testeefunc(testdata))

        # 先頭, 末尾, 文中の 3 パターンをテスト.
        print "=== ascii only ==="
        test(testeefunc, "hogefuga", 0)
        test(testeefunc, "hog" + cs + "efuga", 5)
        test(testeefunc, cs + "hogefuga", 8)
        test(testeefunc, "hogefuga" + cs, 0)
        print "=== ascii + japanese ==="
        test(testeefunc, "ふがhogeぴよよ", 0)
        test(testeefunc, "ふがhog" + cs + "eぴよよ", 4)
        test(testeefunc, cs + "ふがhogeぴよよ", 9)
        test(testeefunc, "ふがhogeぴよよ" + cs, 0)
        # whitespace の文字数が想定通りに計算されてることだけ確認.
        print "=== ascii + whitespace ==="
        S = " "        # space
        T = "\t"       # tab
        L = os.linesep # linesep
        test(testeefunc, "hoge" + cs + S + "fuga", 4+1)
        test(testeefunc, "hoge" + cs + T + "fuga", 4+1)
        test(testeefunc, "hoge" + cs + L + "fuga", 4+2)

        print "=== some cursorstring ==="
        test(testeefunc, "hoge" +cs + "fuga" + cs + "piyo", 8)

if __name__ == "__main__":
    unittest.main()
