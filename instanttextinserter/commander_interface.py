# encoding: shift-jis

class ICommander:
    """
    �R�}���_(�^����ꂽ�R�}���h�ɑ΂��鏈�����s���N���X)�̃C���^�t�F�[�X.
    CoR �p�^�[��.
    �h���N���X�� ���߂ł��邩�ۂ� �� ���ߏ��� �̓���������邱��.
    """
    def __init__(self, next_commander=None):
        self._next_commander = next_commander

    def run(self, command):
        # ���߂ł���Ȃ���߂��Ă����.
        if self._can_interpret(command):
            self._interpret(command)
            return

        # ���߂ł��Ȃ��Ȃ�Ϗ���ɔC����.
        # �Ϗ��悪������΂����ł����.
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
