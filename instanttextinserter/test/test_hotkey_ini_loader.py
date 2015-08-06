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
        ���Ƀe�X�g�ς̑����W���[�����痬�p���Ă邽��,
        �e�X�g�͒���������ɗ��߂Ă���.
        ��肪�o������߂Ēǉ�����\��.
        """

        def assert_entry(line, exp_name, exp_mod, exp_key):
            hotkey_entry = hotkey_ini_loader.HotkeyEntry(line)
            self.assertEqual(hotkey_entry.get_name(), exp_name)
            self.assertEqual(hotkey_entry.get_modifier(), exp_mod)
            self.assertEqual(hotkey_entry.get_keycode(), exp_key)

        testname = "hoge"

        # �e�C���L�[�𐳂����ϊ��ł���
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

        # �C���L�[�̑g�ݍ��킹�𐳂����ϊ��ł���
        # ���ł�, �啶�����������Ȃ����Ƃ�, �󔒗L���Ă��ǂ����Ƃ��m�F.
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

        # �ُ�n
        try:
            # �C���L�[�̎w�肪�����ƃG���[
            hotkey_ini_loader.HotkeyEntry("name")
            self.assertTrue(False)
        except RuntimeError:
            pass
        try:
            # �����L�[�̎w�肪�����ƃG���[
            hotkey_ini_loader.HotkeyEntry("name,as")
            self.assertTrue(False)
        except RuntimeError:
            pass
        try:
            # �󕶎����^����ƃG���[
            hotkey_ini_loader.HotkeyEntry("")
            self.assertTrue(False)
        except RuntimeError:
            pass
        try:
            # �C���L�[���������ƃG���[
            hotkey_ini_loader.HotkeyEntry("name,qqq,k")
            self.assertTrue(False)
        except RuntimeError:
            pass
        try:
            # �����L�[���������ƃG���[
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
        �}�W�b�N�i���o�[��,
        �e�X�g�p�ݒ�t�@�C���̓��e�����ߑł����Ă��镪.
        """
        loader = hotkey_ini_loader.HotkeyIniLoader()
        content = loader.read_all()

        def assert_entry(hotkey_entry, exp_name, exp_mod, exp_key):
            self.assertEqual(hotkey_entry.get_name(), exp_name)
            self.assertEqual(hotkey_entry.get_modifier(), exp_mod)
            self.assertEqual(hotkey_entry.get_keycode(), exp_key)

        # �ݒ茏���̊m�F
        self.assertEqual(5, len(content))

        # �e�ݒ�̒��g���m�F,
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
