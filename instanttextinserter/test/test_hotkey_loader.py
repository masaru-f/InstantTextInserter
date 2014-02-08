# encoding: shift-jis

import os
import unittest

import win32con

import util_win.keycode as keycode

import hotkey_loader

class HotkeyEntryTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assertEntry(self, line, exp_name, exp_mod, exp_key):
        hotkey_entry = hotkey_loader.HotkeyEntry(line)
        self.assertEqual(hotkey_entry._name, exp_name)
        self.assertEqual(hotkey_entry._modifier, exp_mod)
        self.assertEqual(hotkey_entry._keycode, exp_key)

    def test_HotkeyEntry(self):
        """
        正常系は簡単にテスト. 余力あらば観点を追加するといい.
        """
        testname = "hoge"

        # 各修飾キーが正しく変換できる
        self.assertEntry(
            testname + "," + "a, k",
            testname, win32con.MOD_ALT, keycode.K
        )
        self.assertEntry(
            testname + "," + "c, insert",
            testname, win32con.MOD_CONTROL, keycode.INSERT
        )
        self.assertEntry(
            testname + "," + "s, enter",
            testname, win32con.MOD_SHIFT, keycode.ENTER
        )
        self.assertEntry(
            testname + "," + "w, esc",
            testname, win32con.MOD_WIN, keycode.ESC
        )

        # 修飾キーの組み合わせが正しく変換できる
        # ついでに, 大文字小文字問わないことと, 空白有っても良いことも確認.
        self.assertEntry(
            testname + "," + "cs, k", testname,
            win32con.MOD_CONTROL|win32con.MOD_SHIFT,
            keycode.K
        )
        self.assertEntry(
            testname + "," + "   \t cWa   \t , k \t\t  ", testname,
            win32con.MOD_CONTROL|win32con.MOD_WIN|win32con.MOD_ALT,
            keycode.K
        )
        self.assertEntry(
            testname + "," + "aSCw, k", testname,
            win32con.MOD_SHIFT|win32con.MOD_CONTROL| \
            win32con.MOD_WIN|win32con.MOD_ALT,
            keycode.K
        )

        # 異常系
        # @todo どういう場合に許さない, とするのか考えてから TDD しようか.
        # 例)名前が空はダメ, modifier無しはダメ, key無しはダメ, etc...

if __name__ == "__main__":
    unittest.main()
