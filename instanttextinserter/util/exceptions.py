# encoding: shift-jis

class ProgrammersMistake(Exception):
    """
    �R�[�h�̃~�X�ɂ�蔭������G���[.
    �v���O���}�͐������R�[�h���C�����Ȃ���΂Ȃ�Ȃ�.
    �������[�U���猩���邱�Ƃ͂Ȃ�.
    """
    def __init__(self, msg):
        self._msg = msg
        return
    def __str__(self):
        return self._msg

if __name__ == '__main__':
    pass
