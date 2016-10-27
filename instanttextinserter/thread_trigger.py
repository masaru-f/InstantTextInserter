# encoding: shift-jis

import copy

import util_win.keygetter as keygetter

import snippet_manager
import snippet_observer
import snippet_loader
import thread_interface

""" [�p���`]
- �Z�k�`(abbr)
- ��^��(phrase)
- �X�j�y�b�g(snippet) : �Z�k�`�ƒ�^���̑g """

class TriggerThread(
    thread_interface.IWatcherThread,
    snippet_observer.IObserver
):
    """ �Z�k�`�̓��͂��Ď�����X���b�h.
    ���͂��ꂽ��Ή������^����}������.

    �X�j�y�b�g�f�[�^���X�V���ꂽ���ɒʒm���Ăق����̂�,
    Observer ���g���Ď������Ă���. """

    # �X���b�h���[�v�ҋ@���Ԃ�CPU���S�̊֌W.
    # �����: 15/05/07(Thu), ��: Win7(32bit)
    # (sec) (cpu usage)
    # 0.01 : 1.3-2.0
    # 0.02 : 0.6-1.1
    # 0.03 : 0.5-0.7
    # 0.05 : 0.3-0.5
    # 0.05�ł��ߑ��R��͂قƂ�ǔ�������. �]���ʂ�0.03�ŗl�q����.
    INTERVAL_SEC = 0.03

    def __init__(self):
        thread_interface.IWatcherThread.__init__(
            self,
            "trigger thread",
            TriggerThread.INTERVAL_SEC
        )

    # implement the thread interface
    # ------------------------------

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

        # �C���L�[��������Ă����ꍇ�͏ƍ��𖳎�����.
        # ��������Ȃ��� abbr=(space)(semicolon) �� (space)(plus) �ł�
        # �Ђ�������悤�ɂȂ��Ĕς킵��.
        for i in snippet_manager.SnippetManager.modifier_keycode_list:
            if self._getter.is_pushed(i):
                return

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
        #self._snippet_container = snippet_container
        self._snippet_container = copy.deepcopy(snippet_container)
        self._can_reload = True

    # private methods
    # ---------------

    def _reload(self):
        """ �X�j�y�b�g�f�[�^���ēǍ�����. """
        # ���ݓo�^����Ă���e���N���A����.
        # ���ꂵ�Ȃ��ƍēǍ��ł͂Ȃ� append �ɂȂ��Ă��܂�.
        self._manager.clear()

        # container ����X�j�y�b�g���ꌏ�����o���Ēǉ�.
        for key in self._snippet_container.keys():
            abbr = key
            phrase = self._snippet_container[key]
            self._manager.add(abbr, phrase)

if __name__ == '__main__':
    pass
