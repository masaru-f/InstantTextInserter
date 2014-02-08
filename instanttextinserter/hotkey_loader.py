# encoding: shift-jis

import ctypes # for hotkey prototype
import win32con

import util_win.hotkey as hotkey

"""
- content
- name, modifier, key に変換して返す
 - as > MOD_ALT & MOD_SHIFT への変換
 - z > 仮想キーコード への変換
- read_all
 - iniファイルを読み込む
 - 読み込んだ内容を name, modifier, key に変換
 - 変換した奴等を何らかの形式で返却
"""
class IniLoader:
    def __init__(self):
        self._content = None

    def read_all():
        return


"""
試行用.
"""
def func1():
    print "func1!"
def func2():
    print "func2! func2!!"

"""
今はホットキーモジュールを動かすための試行ソース.
したがってごちゃごちゃしてるよ.
"""
class HotkeyLoader:
    def __init__(self, hwnd):
        self._hwnd = hwnd
        self._hotkey_manager = hotkey.HotkeyManager(hwnd)

    def register_hotkey(self):
        name1 = "test-L"
        is_valid_hotkey = self._hotkey_manager.register_hotkey(
            name1,
            win32con.MOD_CONTROL | win32con.MOD_SHIFT,
            76 # L
        )
        if not(is_valid_hotkey):
            print name1 + " failed."
            print "GetLastError:" + str(win32api.GetLastError())
            return
        self._hotkey_manager.register_callback(name1, func1)

        name2 = "test-M"
        is_valid_hotkey = self._hotkey_manager.register_hotkey(
            name2,
            win32con.MOD_CONTROL | win32con.MOD_SHIFT,
            77 # M
        )
        if not(is_valid_hotkey):
            print name2 + " failed."
            print "GetLastError:" + str(win32api.GetLastError())
            return
        self._hotkey_manager.register_callback(name2, func2)

    def unregister_hotkey(self):
        print "START UnregisterHotkey"
        self._hotkey_manager.unregister_all()

    def on_hotkey(self, hwnd, message, wparam, lparam):
        self._hotkey_manager.on_hotkey(hwnd, message, wparam, lparam)

    def get_hotkey_callback(self):
        return self.on_hotkey

if __name__ == '__main__':
    pass
