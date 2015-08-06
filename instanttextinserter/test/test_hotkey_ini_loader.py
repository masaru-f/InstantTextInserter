# encoding: shift-jis

import os
import unittest

import win32con

import util_win.keycode as keycode

import hotkey_ini_loader

class HotkeyEntryTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_HotkeyEntry(self):
        """
        既にテスト済の他モジュールから流用してるため,
        テストは超ざっくりに留めてある.
        問題が出たら改めて追加する予定.
        """

        def assert_entry(line, exp_name, exp_mod, exp_key):
            hotkey_entry = hotkey_ini_loader.HotkeyEntry(line)
            self.assertEqual(hotkey_entry.get_name(), exp_name)
            self.assertEqual(hotkey_entry.get_modifier(), exp_mod)
            self.assertEqual(hotkey_entry.get_keycode(), exp_key)

        testname = "hoge"

        # 各修飾キーを正しく変換できる
        assert_entry(
            testname + "," + "a, k",
            testname, win32con.MOD_ALT, keycode.K
        )
        assert_entry(
            testname + "," + "c, insert",
            testname, win32con.MOD_CONTROL, keycode.INSERT
        )
        assert_entry(
            testname + "," + "s, enter",
            testname, win32con.MOD_SHIFT, keycode.ENTER
        )
        assert_entry(
            testname + "," + "w, esc",
            testname, win32con.MOD_WIN, keycode.ESC
        )

        # 修飾キーの組み合わせを正しく変換できる
        # ついでに, 大文字小文字問わないことと, 空白有っても良いことも確認.
        assert_entry(
            testname + "," + "cs, k", testname,
            win32con.MOD_CONTROL|win32con.MOD_SHIFT,
            keycode.K
        )
        assert_entry(
            testname + "," + "   \t cWa   \t , k \t\t  ", testname,
            win32con.MOD_CONTROL|win32con.MOD_WIN|win32con.MOD_ALT,
            keycode.K
        )
        assert_entry(
            testname + "," + "aSCw, k", testname,
            win32con.MOD_SHIFT|win32con.MOD_CONTROL| \
            win32con.MOD_WIN|win32con.MOD_ALT,
            keycode.K
        )

        # 異常系
        try:
            # 修飾キーの指定が無いとエラー
            hotkey_ini_loader.HotkeyEntry("name")
            self.assertTrue(False)
        except RuntimeError:
            pass
        try:
            # 文字キーの指定が無いとエラー
            hotkey_ini_loader.HotkeyEntry("name,as")
            self.assertTrue(False)
        except RuntimeError:
            pass
        try:
            # 空文字列を与えるとエラー
            hotkey_ini_loader.HotkeyEntry("")
            self.assertTrue(False)
        except RuntimeError:
            pass
        try:
            # 修飾キーが無効だとエラー
            hotkey_ini_loader.HotkeyEntry("name,qqq,k")
            self.assertTrue(False)
        except RuntimeError:
            pass
        try:
            # 文字キーが無効だとエラー
            hotkey_ini_loader.HotkeyEntry("name,sc,invalidname")
            self.assertTrue(False)
        except RuntimeError:
            pass

    def test_HotkeyEntry_SpecialNames(self):
        def assert_entry(line, id_, exp_name):
            hotkey_entry = hotkey_ini_loader.HotkeyEntry(line, id_)
            self.assertEqual(hotkey_entry.get_name(), exp_name)

        def create_linestr(name):
            return '%s,cs,a' % name
        assert_entry(create_linestr("open"), 1, "open1")
        assert_entry(create_linestr("open"), 10, "open10")
        assert_entry(create_linestr("open"), 100, "open100")

    def test_IniLoader(self):
        """
        マジックナンバーは,
        テスト用設定ファイルの内容を決め打ちしている分.
        """
        loader = hotkey_ini_loader.HotkeyIniLoader()
        content = loader.read_all()

        def assert_entry(hotkey_entry, exp_name, exp_mod, exp_key):
            self.assertEqual(hotkey_entry.get_name(), exp_name)
            self.assertEqual(hotkey_entry.get_modifier(), exp_mod)
            self.assertEqual(hotkey_entry.get_keycode(), exp_key)

        # 設定件数の確認
        self.assertEqual(5, len(content))

        # 各設定の中身を確認,
        assert_entry(
            content[0],
            "correct_1_modifier",win32con.MOD_SHIFT,keycode.A
        )
        assert_entry(
            content[1],
            "correct_2_modifier",
            win32con.MOD_CONTROL|win32con.MOD_ALT,
            keycode.A
        )
        assert_entry(
            content[2],
            "correct_3_modifier",
            win32con.MOD_WIN|win32con.MOD_SHIFT|win32con.MOD_CONTROL,
            keycode.A
        )
        assert_entry(
            content[3],
            "correct_4_modifier",
            win32con.MOD_ALT|win32con.MOD_WIN| \
            win32con.MOD_SHIFT|win32con.MOD_CONTROL,
            keycode.A
        )
        assert_entry(
            content[4], "correct_many_spaces",win32con.MOD_ALT,keycode.A
        )

if __name__ == "__main__":
    unittest.main()
