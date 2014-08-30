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
        ���Ғl�̓e�X�g�f�[�^�̕����񂩂�蓮�Ōv�Z.
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
        test(testeefunc, "hoge" + cs + S + "fuga", 4+1)
        test(testeefunc, "hoge" + cs + T + "fuga", 4+1)

        # cursor string �̌�ɂ��� crlf �� 1 �����Ƃ��ăJ�E���g.
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
        # �ŏ��Ɍ������� cursor string ����_�ɂ���
        test(testeefunc, "hoge" +cs + "fuga" + cs + "piyo", 8)

if __name__ == "__main__":
    unittest.main()
