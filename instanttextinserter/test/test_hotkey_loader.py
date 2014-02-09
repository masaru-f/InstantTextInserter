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
        ����n�͊ȒP�Ƀe�X�g. �]�͂���Ίϓ_��ǉ�����Ƃ���.
        """
        testname = "hoge"

        # �e�C���L�[�𐳂����ϊ��ł���
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

        # �C���L�[�̑g�ݍ��킹�𐳂����ϊ��ł���
        # ���ł�, �啶�����������Ȃ����Ƃ�, �󔒗L���Ă��ǂ����Ƃ��m�F.
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

        # �ُ�n
        try:
            # �C���L�[�̎w�肪�����ƃG���[
            hotkey_loader.HotkeyEntry("name")
            self.assertTrue(False)
        except RuntimeError:
            pass
        try:
            # �����L�[�̎w�肪�����ƃG���[
            hotkey_loader.HotkeyEntry("name,as")
            self.assertTrue(False)
        except RuntimeError:
            pass
        try:
            # �󕶎����^����ƃG���[
            hotkey_loader.HotkeyEntry("")
            self.assertTrue(False)
        except RuntimeError:
            pass
        try:
            # �C���L�[���������ƃG���[
            hotkey_loader.HotkeyEntry("name,qqq,k")
            self.assertTrue(False)
        except RuntimeError:
            pass
        try:
            # �����L�[���������ƃG���[
            hotkey_loader.HotkeyEntry("name,sc,invalidname")
            self.assertTrue(False)
        except RuntimeError:
            pass

    def test_IniLoader(self):
        """
        �}�W�b�N�i���o�[��,
        �e�X�g�p�ݒ�t�@�C���̓��e�����ߑł����Ă��镪.
        """
        loader = hotkey_loader.IniLoader()
        content = loader.read_all()

        def assert_entry(hotkey_entry, exp_name, exp_mod, exp_key):
            self.assertEqual(hotkey_entry._name, exp_name)
            self.assertEqual(hotkey_entry._modifier, exp_mod)
            self.assertEqual(hotkey_entry._keycode, exp_key)

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
