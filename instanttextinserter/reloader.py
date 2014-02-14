# encoding: shift-jis

import util.log as log

class Reloader:
    """
    �V���O���g��.
    push ���ꂽ�����[�_�����ԂɃ����[�h���� duck typing.
    push ���ꂽ�����[�_�̏d���`�F�b�N�͍s���Ă��Ȃ����Ƃɒ���.
    """
    def __init__(self):
        self._reload_targets = []

    def push(self, reload_target):
        self._reload_targets.append(reload_target)

    def reload(self):
        for reload_target in self._reload_targets:
            try:
                reload_target.reload()
            except AttributeError as e:
                log.debug(
                    "the reload target is invalid./" +
                    str(e)
                )
# �V���O���g���C���X�^���X
inst = Reloader()

if __name__ == '__main__':
    pass
