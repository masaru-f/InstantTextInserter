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
        �������߂�΃J�[�\���ʒu(��\��������̕���)�ɗ��邩���v�Z.
        """
        paster = snippet_paster.SnippetPaster()
        testeefunc = paster.get_cursorbackcount
        cs = snippet_paster.SnippetPaster.CURSOR_STRING

        def test(testeefunc, testdata, expect):
            print "CASE:" + testdata
            self.assertEqual(expect, testeefunc(testdata))

        # �擪, ����, ������ 3 �p�^�[�����e�X�g.
        print "=== ascii only ==="
        test(testeefunc, "hogefuga", 0)
        test(testeefunc, "hog" + cs + "efuga", 5)
        test(testeefunc, cs + "hogefuga", 8)
        test(testeefunc, "hogefuga" + cs, 0)
        print "=== ascii + japanese ==="
        test(testeefunc, "�ӂ�hoge�҂��", 0)
        test(testeefunc, "�ӂ�hog" + cs + "e�҂��", 4)
        test(testeefunc, cs + "�ӂ�hoge�҂��", 9)
        test(testeefunc, "�ӂ�hoge�҂��" + cs, 0)
        # whitespace �̕��������z��ʂ�Ɍv�Z����Ă邱�Ƃ����m�F.
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
