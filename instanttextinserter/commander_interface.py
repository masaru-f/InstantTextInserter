# encoding: shift-jis

class ICommander:
    """
    コマンダ(与えられたコマンドに対する処理を行うクラス)のインタフェース.
    CoR パターン.
    派生クラスは 解釈できるか否か と 解釈処理 の二つを実装すること.
    """
    def __init__(self, next_commander=None):
        self._next_commander = next_commander

    def run(self, command):
        # 解釈できるなら解釈しておわり.
        if self._can_interpret(command):
            self._interpret(command)
            return

        # 解釈できないなら委譲先に任せる.
        # 委譲先が無ければそこでおわり.
        if not(self._next_commander):
            return
        self._next_commander.run(command)

    def _can_interpret(self, command):
        raise NotImplementedError("implement _can_interpret!")

    def _interpret(self, command):
        raise NotImplementedError("implement _interpret!")

'''
class HogeCommander(Icommander):
    def __init__(self, next_commander=None):
        ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command=="hoge":
            return True
        return False

    def _interpret(self, command):
        # implement!
        pass
'''
