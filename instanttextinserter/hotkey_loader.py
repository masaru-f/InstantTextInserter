# encoding: shift-jis

import ctypes # for hotkey prototype
import win32con

import util_win.hotkey as hotkey

"""
- content
- name, modifier, key �ɕϊ����ĕԂ�
 - as > MOD_ALT & MOD_SHIFT �ւ̕ϊ�
 - z > ���z�L�[�R�[�h �ւ̕ϊ�
- read_all
 - ini�t�@�C����ǂݍ���
 - �ǂݍ��񂾓��e�� name, modifier, key �ɕϊ�
 - �ϊ������z�������炩�̌`���ŕԋp
"""
class IniLoader:
    def __init__(self):
        self._content = None

    def read_all():
        return

class HotkeyLoader:
    def __init__(self, hwnd):
        self._hwnd = hwnd
        self._hotkey_config = hotkey.HotkeyConfig(hwnd, 1234) # �l�͓K��.

    def register_hotkey(self):
        is_valid_hotkey = self._hotkey_config.register_hotkey(
            win32con.MOD_CONTROL | win32con.MOD_SHIFT,
            76 # L
        )
        if not(is_valid_hotkey):
            print "RegisterHotkey1 failed."
            print "GetLastError:" + str(win32api.GetLastError())

    def unregister_hotkey(self):
        self._hotkey_config.unregister_hotkey()

    def on_hotkey(self, hwnd, message, wparam, lparam):
        print "from hotkeyloader, " + str(self)
        print "hwnd:" + str(hwnd)
        print "message:" + str(message)
        print "wparam:" + str(wparam)
        print "lparam:" + str(lparam)

    def get_hotkey_callback(self):
        return self.on_hotkey

if __name__ == '__main__':
    pass
