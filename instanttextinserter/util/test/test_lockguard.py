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
            インクリメント後, 指定秒だけ待つカウンタ.
            待っている間にインクリメントが呼び出されたら待たせる.
            """
            def __init__(self, waitsec):
                self._count = 0
                self._waitsec = waitsec
                self._can_increment = True
                self._mutex = lockguard.Mutex()

            def increment(self):
                """
                もし lockguard 部分が無かったら同時 increment は機能しない.
                _can_increment で弾かれるから.

                ちゃんと排他制御ができていれば,
                弾かれること無く, 同時 increment の数だけ処理される.
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

        # 同時 increment は複数スレッドで実現する.
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
        # 各スレッドを開始.
        # つまりここで同時 increment が実行される.
        for threadelm in threadlist:
            threadelm.start()

        for threadelm in threadlist:
            threadelm.join()
        print "testing lockguard finished."

        # 排他制御が効いていれば
        # 同時 increment 数だけインクリメントされているはず.
        self.assertEqual(threadnum, counter.get())

if __name__ == "__main__":
    unittest.main()
