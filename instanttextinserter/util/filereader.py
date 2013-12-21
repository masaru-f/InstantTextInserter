# encoding: shift-jis

class FileReader:
    def __init__(self):
        return

    def read(self, filename):
        """
        @return ファイル内容の各行を要素としたリスト
        @exception IOError ファイルが開けない
        """
        fileobj = open(filename, "r")
        ret = fileobj.readlines()
        fileobj.close()
        return ret
