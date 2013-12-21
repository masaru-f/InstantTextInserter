# encoding: shift-jis

import unittest
import threading

import util.lockguard as lockguard

class LockGuardTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testlockguard(self):
        from time import sleep

        class ExclusiveWaitingCounter:
            """
            �C���N�������g��, �w��b�����҂J�E���^.
            �҂��Ă���ԂɃC���N�������g���Ăяo���ꂽ��҂�����.
            """
            def __init__(self, waitsec):
                self._count = 0
                self._waitsec = waitsec
                self._can_increment = True
                self._mutex = lockguard.Mutex()

            def increment(self):
                """
                ���� lockguard ���������������瓯�� increment �͋@�\���Ȃ�.
                _can_increment �Œe����邩��.

                �����Ɣr�����䂪�ł��Ă����,
                �e����邱�Ɩ���, ���� increment �̐��������������.
                """
                with lockguard.LockGuard(self._mutex) as lginst:
                    if not(self._can_increment):
                        return
                    self._can_increment = False
                    self._count += 1
                    sleep(self._waitsec)
                    self._can_increment = True

            def get(self):
                return self._count

        counter = ExclusiveWaitingCounter(0.2)

        # ���� increment �͕����X���b�h�Ŏ�������.
        threadlist = []
        threadnum = 10
        for i in range(threadnum):
            threadname = "thread_" + str(i)
            threadlist.append(
                threading.Thread(
                    None,
                    counter.increment,
                    threadname,
                    (),
                    {}
                )
            )

        print "testing lockguard..."
        # �e�X���b�h���J�n.
        # �܂肱���œ��� increment �����s�����.
        for threadelm in threadlist:
            threadelm.start()

        for threadelm in threadlist:
            threadelm.join()
        print "testing lockguard finished."

        # �r�����䂪�����Ă����
        # ���� increment �������C���N�������g����Ă���͂�.
        self.assertEqual(threadnum, counter.get())

if __name__ == "__main__":
    unittest.main()
