# encoding: shift-jis

import unittest

import util_win.clipboard as clipboard

class ClipboardTest(unittest.TestCase):
    """
    クリップボードの中身を変えることに注意.
    文字列データの場合は一応元に戻すが,
    あまり厳密性にはこだわってない.
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_clipboard_normal(self):
        # 元データを退避
        # @note 文字列以外のデータだった場合はどうなるか知らん.
        origin = clipboard.Clipboard.get()

        # セットが行える
        testdata = "ほげふがぴよ hogefugapiyo 123"
        self.assertTrue(clipboard.Clipboard.set(testdata))

        # セットしたものをゲットできる
        self.assertEqual(testdata, clipboard.Clipboard.get())

        # 退避したデータを元に戻す
        self.assertTrue(clipboard.Clipboard.set(origin))

    def test_clipboard_error(self):
        origin = clipboard.Clipboard.get()

        # unicode string は非対応
        testdata = u"ほげふがぴよ hogefugapiyo 123"
        self.assertFalse(clipboard.Clipboard.set(testdata))

        # クリップボードの中身は変わってない
        self.assertEqual(origin, clipboard.Clipboard.get())

    def test_clipboard_repearly(self):
        origin = clipboard.Clipboard.get()

        # 連続で使えるか試す
        for i in range(1000):
            testdata = str(i*i*i)
            self.assertTrue(clipboard.Clipboard.set(testdata))
            self.assertEqual(testdata, clipboard.Clipboard.get())

        self.assertTrue(clipboard.Clipboard.set(origin))

if __name__ == "__main__":
    unittest.main()
