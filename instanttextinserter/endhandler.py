# encoding: shift-jis

class EndHandler:
    """
    �I���n���h��.
    �ǂ�����ł��v���O�������I���ł���悤�ɂ���d�g��.

    [�g����]
    �G���g���|�C���g�ɂďI���p�֐���o�^��,
    �I���������ꏊ������s����.
    """
    def __init__(self):
        self._handler = None

    def set(self, handler):
        self._handler = handler

    def run(self):
        if not(callable(self._handler)):
            raise RuntimeError("EndHandler is not initialized")
        self._handler()
# �V���O���g���C���X�^���X
inst = EndHandler()
