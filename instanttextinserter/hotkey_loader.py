# encoding: shift-jis

import ctypes # for hotkey prototype
import win32con

import util_win.hotkey as hotkey
import util_win.keycode as keycode

import selfinfo
import util.filereader as filereader

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

class HotkeyEntry:
    """
    �ݒ�t�@�C������ǂݍ���, �z�b�g�L�[�ݒ���.
    """
    SEPARATOR = ","
    def __init__(self, line):
        # "a , b , c  " �� [a,b,c] ��.
        # ���X�g���Ɗe�v�f�̋󔒏���.
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
        'as' ���� MOD_ALT|MOD_SHIFT ��Ԃ�, �悤�Ȃ��.
        @retval 0 �w�蕶���񂪕s��
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
        'a' ���� 65 ��Ԃ�, �悤�Ȃ��.
        @retval 0 �w�蕶���񂪕s��
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
        @exception IOError �t�@�C�����J���Ȃ�
        """
        reader = filereader.FileReader()
        self._content = reader.read()


"""
���s�p.
"""
def func1():
    print "func1!"
def func2():
    print "func2! func2!!"

"""
���̓z�b�g�L�[���W���[���𓮂������߂̎��s�\�[�X.
���������Ă����Ⴒ���Ⴕ�Ă��.
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
