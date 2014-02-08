# encoding: shift-jis

import ctypes # for hotkey prototype
import win32con

import util_win.hotkey as hotkey
import util_win.keycode as keycode

import selfinfo
import util.filereader as filereader

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

class HotkeyEntry:
    """
    設定ファイルから読み込んだ, ホットキー設定一つ分.
    """
    SEPARATOR = ","
    def __init__(self, line):
        # "a , b , c  " → [a,b,c] に.
        # リスト化と各要素の空白除去.
        ls = line.split(HotkeyEntry.SEPARATOR)
        ls = [elm.strip() for elm in ls]

        try:
            self._name = ls[0]
            self._modifier = self._to_interger_modifier(ls[1])
            self._keycode = self._to_interger_keycode(ls[2])
        except IndexError:
            raise

        return

    def _to_interger_modifier(self, modifier_string):
        """
        'as' から MOD_ALT|MOD_SHIFT を返す, ようなやつ.
        @retval 0 指定文字列が不正
        """
        query = modifier_string.lower()
        ret = 0
        if query.find("a") != -1:
            ret |= win32con.MOD_ALT
        if query.find("c") != -1:
            ret |= win32con.MOD_CONTROL
        if query.find("s") != -1:
            ret |= win32con.MOD_SHIFT
        if query.find("w") != -1:
            ret |= win32con.MOD_WIN
        return ret

    def _to_interger_keycode(self, key_string):
        """
        'a' から 65 を返す, ようなやつ.
        @retval 0 指定文字列が不正
        """
        ret = keycode.str2keycode(key_string.lower())

        if ret==keycode.INVALID:
            ret = 0

        return ret

class IniLoader:
    def __init__(self):
        self._content = None

    def read_all(self):
        """
        @exception IOError ファイルが開けない
        """
        reader = filereader.FileReader()
        self._content = reader.read()


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
