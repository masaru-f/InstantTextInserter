# encoding: shift-jis

import copy

import util_win.keygetter as keygetter

import snippet_manager
import snippet_observer
import snippet_loader
import thread_interface

"""
�p���`

�Z�k�`(abbr)        :
��^��(phrase)      :
�X�j�y�b�g(snippet) : �Z�k�`�ƒ�^���̑g

"""

class TriggerThread(
    thread_interface.IWatcherThread,
    snippet_observer.IObserver
):
    """
    �Z�k�`�̓��͂��Ď�����X���b�h.
    ���͂��ꂽ��Ή������^����}������.

    �X�j�y�b�g�f�[�^���X�V���ꂽ���ɒʒm���Ăق����̂�,
    Observer ���g���Ď������Ă���.
    """

    # �X���b�h���[�v�̑ҋ@����.
    # 0.05 ���ƃ��[�v���̂��x���ăL�[���͂̕ߑ��R�ꂪ�N����.
    # 0.01 ���ƃ��[�v���̂���������CPU���S���傫��.
    # 0.03 ���Ώ��Ö@�I�ȍœK�l.
    INTERVAL_SEC = 0.03

    def __init__(self):
        thread_interface.IWatcherThread.__init__(
            self,
            "trigger thread",
            TriggerThread.INTERVAL_SEC
        )

    # implement the thread interface
    # --------------------------------

    def _init(self):
        self._getter = keygetter.KeyGetter()
        self._manager = snippet_manager.SnippetManager()

        # �����[�h���Ă��ǂ��ꍇ�ɗ���.
        # �����[�h��͍~�낷.
        self._can_reload = False

        # �ʒm���ꂽ�X�j�y�b�g�f�[�^�����Ă����̈�.
        self._snippet_container = None

        snippet_loader.inst.attach(self)
        # �X�j�y�b�g�f�[�^�̏��񎞓ǂݍ���.
        snippet_loader.inst.reload()

    def _procedure(self):
        # �ʒm����Ă���΍ēǍ�����.
        if self._can_reload:
            self._reload()
            self._can_reload = False

        for i in snippet_manager.SnippetManager.supported_keycode_list:
            if self._getter.is_pushed_once(i):
                self._manager.input(i)

    def _term(self):
        pass

    # implement the observer interface
    # --------------------------------

    def notify(self, snippet_container):
        # ���ꂾ�Ƒ��� ovserver �ɒʒm���ꂽ snippet_container
        # ���ύX���Ă��܂�(�Q�Ɠn���Ȃ̂�)���ꂪ���邽��
        # �O�̂��� deepcopy �ɂ���.
        # @todo ���N���X���ŏ�肢���Ə����ł��Ȃ�������?
        #self._snippet_container = snippet_container
        self._snippet_container = copy.deepcopy(snippet_container)
        self._can_reload = True

    # private methos
    # --------------------------------

    def _reload(self):
        """
        �X�j�y�b�g�f�[�^���ēǍ�����.
        """
        # ���ݓo�^����Ă���e���N���A����.
        # ���ꂵ�Ȃ��ƍēǍ��ł͂Ȃ� append �ɂȂ��Ă��܂�.
        self._manager.clear()

        # container ����X�j�y�b�g���ꌏ�����o���Ēǉ�.
        # @todo container �̌^���R�[�h����킩��ɂ����̂ŉ��Ƃ�������.
        for key in self._snippet_container.keys():
            abbr = key
            phrase = self._snippet_container[key]
            self._manager.add(abbr, phrase)

if __name__ == '__main__':
    from time import sleep

    def start(continuesec):
        """
        with�����甲���邽�߂Ɋ֐��ɂ��Ă���.
        �֐�������� return �Ŕ�������.

        @param continuesec ���b�ԓ�������.
        """
        with TriggerThread() as watcher:
            watcher.start()
            sleep(continuesec)
    start(15)

