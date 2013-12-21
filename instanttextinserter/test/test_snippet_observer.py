# encoding: shift-jis

import os
import unittest

import snippet_observer

class SnippetObserverTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        """
        snippet_container として数値が渡されることを想定.
        もし IObserver 側で型チェックをするならこのテストは無効.
        """
        class Observer1(snippet_observer.IObserver):
            def __init__(self):
                self._count = 0

            def notify(self, snippet_container):
                self._count += snippet_container*1

        class Observer10(snippet_observer.IObserver):
            def __init__(self):
                self._count = 0

            def notify(self, snippet_container):
                self._count += snippet_container*10

        ob1 = Observer1()
        ob10 = Observer10()
        subject = snippet_observer.Subject()

        subject.attach(ob1)
        subject.attach(ob10)
        subject.attach(ob10) # 重複登録が除外されることの確認用

        subject.notify_all(1)
        subject.notify_all(2)
        subject.notify_all(3)

        # 通知された値を自分の処理に従って計算できている.
        self.assertEqual(ob1._count, 6)
        self.assertEqual(ob10._count, 60)

if __name__ == "__main__":
    unittest.main()
