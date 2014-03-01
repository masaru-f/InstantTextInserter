# encoding: shift-jis

import threading
import time

import util.log as log

class IWatcherThread:
    """
    �X���b�h�{�̂� Template Method.
    �h���N���X�ł͏�����, �������[�v������, �����������������.
    """
    def __init__(self, name, loopsec):
        """
        @param name �X���b�h��
        @param loopsec �������[�v���̑ҋ@����(���������_�̕b)
        """
        self._name = name
        self._loopsec = loopsec

        self._endflag = False
        self._thread = None
        return

    def __enter__(self):
        return self

    def __exit__(self, type, value, trackback):
        self.stop()

    def start(self):
        self._thread = threading.Thread(None, \
                                       self._body, \
                                       self._name,\
                                       (), \
                                       {}  \
        )
        log.info("start thread:" + str(self._name))
        self._thread.start()

    def stop(self):
        self._endflag = True
        if self._thread:
            log.info("joining thread...:" + str(self._name))
            self._thread.join()
            log.info("stopthread:" + str(self._name))

    def _body(self):
        """
        �X���b�h�{��.
        Templete Method.
        """
        self._init()

        while True:
            if self._endflag:
                break

            self._procedure()

            time.sleep(self._loopsec)

        self._term()

    def _init(self):
        raise NotImplementedError

    def _procedure(self):
        raise NotImplementedError

    def _term(self):
        raise NotImplementedError

if __name__ == '__main__':
    pass
