# encoding: shift-jis

import unittest

import util.stack as stack

class StackTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testpush_and_pop(self):
        s = stack.Stack()
        testdata = [1, "2", "hoge", [1,2], {"a":"A"}]
        testdatalen = len(testdata)

        # 最初は空
        self.assertTrue(s.is_empty())

        # push
        for i in range(testdatalen):
            s.push(testdata[i])
        self.assertEqual(testdatalen, s.get_count())

        # 後からpushした順番でpopできる
        for i in range(testdatalen):
            self.assertEqual(s.pop(), testdata[testdatalen-1-i])

        # 空スタックをpopすると例外が出る
        def is_thrown(s):
            try:
                s.pop()
                return False
            except IndexError:
                return True
        self.assertTrue(is_thrown(s))

        return

if __name__ == "__main__":
    unittest.main()
