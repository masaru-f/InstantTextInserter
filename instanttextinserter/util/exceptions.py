# encoding: shift-jis

class ProgrammersMistake(Exception):
    """
    コードのミスにより発生するエラー.
    プログラマは正しくコードを修正しなければならない.
    原則ユーザから見えることはない.
    """
    def __init__(self, msg):
        self._msg = msg
        return
    def __str__(self):
        return self._msg

if __name__ == '__main__':
    pass
