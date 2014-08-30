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
        期待値はテストデータの文字列から手動で計算.
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
        test(testeefunc, "hoge" + cs + S + "fuga", 4+1)
        test(testeefunc, "hoge" + cs + T + "fuga", 4+1)

        # cursor string の後にある crlf は 1 文字としてカウント.
        print "=== acsii + linefeed, and crlf 1count test ==="
        L_crlf = "\r\n"
        L_lf = "\n"
        L_cr = "\r"
        crlf_offset = 0
        test(testeefunc,
             "hoge" +  L_crlf + "fuga" + L_crlf + "piyo" + cs,
             0-crlf_offset)

        crlf_offset = 1
        test(testeefunc, "hoge" + cs + L_crlf + "fuga", 4+2-crlf_offset)
        test(testeefunc, "hoge" + cs + L_lf + "fuga", 4+1)
        test(testeefunc, "hoge" + cs + L_cr + "fuga", 4+1)

        crlf_offset = 2
        test(testeefunc,
             "ho" + cs + "ge" +  L_crlf + "fuga" + L_crlf + "piyo",
             14-crlf_offset)

        print "=== some cursorstring ==="
        # 最初に見つかった cursor string を基点にする
        test(testeefunc, "hoge" +cs + "fuga" + cs + "piyo", 8)

if __name__ == "__main__":
    unittest.main()
