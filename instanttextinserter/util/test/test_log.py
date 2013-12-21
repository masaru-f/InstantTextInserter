# encoding: shift-jis

import unittest

import util.log as log

class LogTest(unittest.TestCase):
    """
    文字列として出力された時にカウンタを増やすクラスを作り,
    それをログとして出力させた後,
    そのカウンタを数えることで, ログ出力回数を測っている.
    """
    def setUp(self):
        class CounterMessage:
            def __init__(self, msg):
                self._msg = msg
                self._counter = 0

            def __str__(self):
                self._counter += 1
                return self._msg

            def get_count(self):
                return self._counter

        self.dmsg = CounterMessage("debug message")
        self.imsg = CounterMessage("info message")
        self.wmsg = CounterMessage("warning message")
        self.emsg = CounterMessage("error message")
        self.cmsg = CounterMessage("critical message")

        self.loginst = log.Log()

    def tearDown(self):
        pass

    def output(self):
        self.loginst.debug(self.dmsg)
        self.loginst.info(self.imsg)
        self.loginst.warning(self.wmsg)
        self.loginst.error(self.emsg)
        self.loginst.critical(self.cmsg)

    def assert_output(self, expect_list):
        actual = [
            self.dmsg.get_count(),
            self.imsg.get_count(),
            self.wmsg.get_count(),
            self.emsg.get_count(),
            self.cmsg.get_count(),
        ]
        self.assertEqual(expect_list, actual)

    def test_log_default_level(self):
        # デフォルトレベル以上は全部出る.
        self.output()
        self.assert_output([0, 1, 1, 1, 1])

    def test_log_selected_level(self):
        # 指定レベル以上は全部出る.
        self.loginst.set_filteringlv(log.LEVEL.error)
        self.output()
        self.assert_output([0, 0, 0, 1, 1])

    def test_log_min_level(self):
        # 全レベルのログが出る
        self.loginst.set_filteringlv(log.LEVEL.minlevel)
        self.output()
        self.assert_output([1, 1, 1, 1, 1])

    def test_log_max_level(self):
        # 最大レベルのログのみ出る
        self.loginst.set_filteringlv(log.LEVEL.maxlevel)
        self.output()
        self.assert_output([0, 0, 0, 0, 1])

    def test_log_level_range_error(self):
        # 範囲外のレベル指定時はエラー
        def is_thrown(func, arg):
            try:
                func(arg)
            except ValueError:
                return True
            return False

        self.assertTrue(
            is_thrown(
                self.loginst.set_filteringlv,
                log.LEVEL.lower_limit
            )
        )
        self.assertTrue(
            is_thrown(
                self.loginst.set_filteringlv,
                log.LEVEL.upper_limit
            )
        )

if __name__ == "__main__":
    unittest.main()
