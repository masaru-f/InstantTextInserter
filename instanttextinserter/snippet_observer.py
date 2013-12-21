# encoding: shift-jis

"""
snippet data �Ɋւ��� Observer �p�^�[��.
�ʒm����/�����f�[�^�� snippet container ��z�肵�Ă��邪,
�e�X�g��ėp���̂��ߌ^�`�F�b�N�͎������Ă��Ȃ�.
"""

class IObserver:
    """
    �ʒm���ꂽ�f�[�^���ǂ����邩�͔h���N���X����.
    �ʒm���ꂽ�f�[�^�ɕҏW��������ꍇ, �h���N���X���� deepcopy ���邱��.
    """
    def notify(self, snippet_container):
        raise NotImplementedError

class Subject:
    """
    observer �̓o�^���@�ƒʒm���@�͋��ʂ��Ă���̂ŋ��ʉ�.
    ����ʒm���邩�͗��p�ґ������߂�.
    """
    def __init__(self):
        self._observerlist = []

    def attach(self, observer):
        if observer in self._observerlist:
            # ���ɓo�^����Ă���Ζ�������
            return
        self._observerlist.append(observer)

    def notify_all(self, snippet_container):
        for observer in self._observerlist:
            observer.notify(snippet_container)
