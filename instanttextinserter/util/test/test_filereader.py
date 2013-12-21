# encoding: shift-jis

import unittest
import os.path
import inspect # for getting like __LINE__

import util.filereader as filereader

def line():
    """
    �Ăяo�����ʒu�̍s�ԍ���Ԃ�.
    """
    return inspect.currentframe(1).f_lineno

def to_abs(filename):
    """
    �e�X�g�R�[�h���ǂ�����ł����s�ł���悤��΃p�X�ɂ���.
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

        # ���݂��Ȃ��t�@�C���͓ǂݍ��߂Ȃ�
        self.assertFalse(
            is_read_ok(reader, "no_existence.hoge")
        )

        # ���݂���t�@�C����ǂݍ��ރe�X�g�Ƃ���
        # ���̃t�@�C�����g���w��.
        this_filename = to_abs(__file__)
        if this_filename[-3:]=="pyc":
            # ���̃f�B���N�g������{�e�X�g�����s������,
            # ���ڈȍ~�� __file__ �� pyc �t�@�C�����w���̂�
            # �Ӑ}�I�� pyc �� py �ɖ߂��Ă���.
            this_filename = this_filename[:-1]

        # �ǂݍ��߂�
        content = reader.read(this_filename)
        # ���Ȃ��Ƃ������̍s�ԍ����͑����̍s�������Ă���
        self.assertLess(line(), len(content))

        return

if __name__ == "__main__":
    unittest.main()
