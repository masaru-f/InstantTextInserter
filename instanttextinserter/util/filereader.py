# encoding: shift-jis

class FileReader:
    def __init__(self):
        return

    def read(self, filename):
        """
        @return �t�@�C�����e�̊e�s��v�f�Ƃ������X�g
        @exception IOError �t�@�C�����J���Ȃ�
        """
        fileobj = open(filename, "r")
        ret = fileobj.readlines()
        fileobj.close()
        return ret
