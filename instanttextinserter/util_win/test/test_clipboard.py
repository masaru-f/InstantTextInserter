# encoding: shift-jis

import unittest

import util_win.clipboard as clipboard

class ClipboardTest(unittest.TestCase):
    """
    �N���b�v�{�[�h�̒��g��ς��邱�Ƃɒ���.
    ������f�[�^�̏ꍇ�͈ꉞ���ɖ߂���,
    ���܂茵�����ɂ͂�������ĂȂ�.
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_clipboard_normal(self):
        # ���f�[�^��ޔ�
        # @note ������ȊO�̃f�[�^�������ꍇ�͂ǂ��Ȃ邩�m���.
        origin = clipboard.Clipboard.get()

        # �Z�b�g���s����
        testdata = "�ق��ӂ��҂� hogefugapiyo 123"
        self.assertTrue(clipboard.Clipboard.set(testdata))

        # �Z�b�g�������̂��Q�b�g�ł���
        self.assertEqual(testdata, clipboard.Clipboard.get())

        # �ޔ������f�[�^�����ɖ߂�
        self.assertTrue(clipboard.Clipboard.set(origin))

    def test_clipboard_error(self):
        origin = clipboard.Clipboard.get()

        # unicode string �͔�Ή�
        testdata = u"�ق��ӂ��҂� hogefugapiyo 123"
        self.assertFalse(clipboard.Clipboard.set(testdata))

        # �N���b�v�{�[�h�̒��g�͕ς���ĂȂ�
        self.assertEqual(origin, clipboard.Clipboard.get())

    def test_clipboard_repearly(self):
        origin = clipboard.Clipboard.get()

        # �A���Ŏg���邩����
        for i in range(1000):
            testdata = str(i*i*i)
            self.assertTrue(clipboard.Clipboard.set(testdata))
            self.assertEqual(testdata, clipboard.Clipboard.get())

        self.assertTrue(clipboard.Clipboard.set(origin))

if __name__ == "__main__":
    unittest.main()
