# encoding: shift-jis

import unittest

import util_win.multiplelaunch as multiplelaunch

class MultipleLaunchTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_already_running(self):
        programname = "hogehoge"

        # 初回起動時
        self.assertFalse(multiplelaunch.is_already_running(programname))

        # 既に起動されている.
        self.assertTrue(multiplelaunch.is_already_running(programname))
        self.assertTrue(multiplelaunch.is_already_running(programname))

if __name__ == "__main__":
    unittest.main()
