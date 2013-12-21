# encoding: shift-jis

class EndHandler:
    """
    終了ハンドラ.
    どこからでもプログラムを終了できるようにする仕組み.

    [使い方]
    エントリポイントにて終了用関数を登録し,
    終了したい場所から実行する.
    """
    def __init__(self):
        self._handler = None

    def set(self, handler):
        self._handler = handler

    def run(self):
        if not(callable(self._handler)):
            raise RuntimeError("EndHandler is not initialized")
        self._handler()
# シングルトンインスタンス
inst = EndHandler()
