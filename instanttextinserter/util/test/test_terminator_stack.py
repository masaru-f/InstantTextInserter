# encoding: shift-jis

import unittest

import util.terminator_stack as terminator_stack

# 検査で使用する値.
# 本当はテストケース内に定義したかったが,
# そうすると plus1 関数等からアクセスできなかったので
# 仕方なくグローバルに置いた.
g_testdata = 0

class TerminatorStackTest(unittest.TestCase):
    """
    終了処理としてテストデータを書き換える関数を使用してテスト.
    @todo 実行順序を試すテストが無いので追加する.
    """
    def setUp(self):
        global g_testdata
        g_testdata = 0

    def tearDown(self):
        pass

    def test_terminator_case_default(self):
        """
        終了中にエラーが起きない場合.
        """
        def plus1():
            global g_testdata
            g_testdata += 1

        def multiple2():
            global g_testdata
            g_testdata *= 2

        with terminator_stack.TerminatorStack() as termstack:
            termstack.push(plus1)
            termstack.push(multiple2)
            termstack.push(plus1)
            termstack.push(plus1)

        global g_testdata
        self.assertEqual(5, g_testdata)

    def test_terminator_case_not_ignoring(self):
        """
        終了中にエラーが起きる場合で, エラーを無視しない場合.
        """
        def plus1():
            global g_testdata
            g_testdata += 1

        def raiser():
            raise RuntimeError("raised by raiser.")

        try:
            with terminator_stack.TerminatorStack(False) as termstack:
                termstack.push(plus1)
                termstack.push(plus1)
                termstack.push(raiser)
                termstack.push(plus1)
                termstack.push(plus1)
        except RuntimeError:
            pass

        global g_testdata
        # エラーが起きたところまでが実行されている.
        self.assertEqual(2, g_testdata)

    def test_terminator_case_ignoring(self):
        """
        終了中にエラーが起きる場合で, エラーを無視する場合.
        """
        def plus1():
            global g_testdata
            g_testdata += 1

        def raiser():
            raise RuntimeError("raised by raiser.")

        with terminator_stack.TerminatorStack(True) as termstack:
            termstack.push(plus1)
            termstack.push(raiser)
            termstack.push(plus1)
            termstack.push(raiser)
            termstack.push(raiser)
            termstack.push(plus1)
            termstack.push(plus1)

        global g_testdata
        # 全ての終了処理が実行されている.
        self.assertEqual(4, g_testdata)

    def test_terminator_no_element(self):
        """
        エラーが起きないことを確かめているだけ.
        """
        with terminator_stack.TerminatorStack() as termstack:
            pass

        with terminator_stack.TerminatorStack(True) as termstack:
            pass

        with terminator_stack.TerminatorStack(False) as termstack:
            pass

if __name__ == "__main__":
    unittest.main()
