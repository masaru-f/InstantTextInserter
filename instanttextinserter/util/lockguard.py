# encoding: shift-jis

import threading

class Mutex:
    def __init__(self):
        self._mutex = threading.Lock()

    def lock(self):
        self._mutex.acquire()

    def unlock(self):
        self._mutex.release()

class LockGuard:
    """
    with statement �Ŏg�����Ƃ�O��.
    �����Ɠ����Ƀ��b�N��, �X�R�[�v���O���ƃA�����b�N.

    [example]
    mutex = Mutex()
    with LockGuard(mutex) as lockguard:
        # procedure
        # ...
    """
    def __init__(self, mutex):
        if not(isinstance(mutex, Mutex)):
            raise TypeError("The given mutex is not a type of Mutex.")
        self._mutex = mutex

    def __enter__(self):
        self._mutex.lock()

    def __exit__(self, type, value, trackback):
        self._mutex.unlock()


if __name__ == "__main__":
    """
    �蓮�e�X�g.
    �X���b�h������ lock �����s���邪,
    main �� lockguard �� unlock ����ƃX���b�h�̕������������.
    """
    from time import sleep

    def thread_body(mutex):
        print " / [threadbody]before locking, " + \
              "and waiting for locked from main."
        mutex.lock()
        print " / [threadbody]unlocked."
        mutex.unlock()

    mutex = Mutex()
    thread = threading.Thread(None, \
                              thread_body, \
                              "thread_name",\
                              (mutex,), \
                              {}  \
    )

    with LockGuard(mutex) as lockguard:
        print " / [main]locked with lockguard.",
        sleep(1)
        print " / [main]starting a thread...",
        thread.start()
        print " / [main]waiting until 3 sec...",
        sleep(3)

    print " / [main]unlocked bacause passing lockguard scope.",
    thread.join()
