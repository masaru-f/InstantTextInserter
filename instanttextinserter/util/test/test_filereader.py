# encoding: shift-jis

import unittest
import os.path
import inspect # for getting like __LINE__

import util.filereader as filereader

def line():
    """
    呼び出した位置の行番号を返す.
    """
    return inspect.currentframe(1).f_lineno

def to_abs(filename):
    """
    テストコードをどこからでも実行できるよう絶対パスにする.
    """
    _path = os.path.abspath(__file__)
    _dir = os.path.dirname(_path)
    return os.path.join(_dir, filename)

class FileReaderTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        reader = filereader.FileReader()

        def is_read_ok(reader, filename):
            try:
                ls = reader.read(filename)
                return True
            except IOError:
                return False

        # 存在しないファイルは読み込めない
        self.assertFalse(
            is_read_ok(reader, "no_existence.hoge")
        )

        # 存在するファイルを読み込むテストとして
        # このファイル自身を指定.
        this_filename = to_abs(__file__)
        if this_filename[-3:]=="pyc":
            # 他のディレクトリから本テストを実行した際,
            # 二回目以降は __file__ が pyc ファイルが指すので
            # 意図的に pyc → py に戻している.
            this_filename = this_filename[:-1]

        # 読み込める
        content = reader.read(this_filename)
        # 少なくともここの行番号よりは多くの行を持っている
        self.assertLess(line(), len(content))

        return

if __name__ == "__main__":
    unittest.main()
