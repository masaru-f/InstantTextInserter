# encoding: shift-jis

import ctypes
import win32con

import keycode

"""
hotkeyconfig in util.win
- hwnd
- index
- modifier
- key
- callback
- ctor(hwnd, index)
- register_hotkey(modifier, key)
 - RegisterHotkey ���Ăяo��
 - ����������, ���g�̃����o�ϐ����X�V
- set_callback(callback)
- unregister_hotkey()
 - UnregisterHotkey ���Ăяo��
"""
class HotkeyConfig:
    """
    �z�b�g�L�[����̐ݒ���ƐU�镑��������.

    """
    def __init__(self, hwnd, index):
        self._hwnd = hwnd
        self._index = index
        self._modifier = None
        self._key = None
        self._callback = None

    def register_hotkey(self, modifier, key):
        """
        �V�����z�b�g�L�[�o�^���s����, �ȑO�o�^���͏㏑�������.

        @param modifier win32con �� MOD_HOGE �̑g�ݍ��킹
        @param key ���z�L�[�R�[�h
        @retval false �o�^�Ɏ��s
        """
        is_hotkey_valid = ctypes.windll.user32.RegisterHotKey(
            self._hwnd,
            self._index,
            modifier,
            key
        )
        if not(is_hotkey_valid):
            # �Ƃ肠�����G���[�ڍ�(win32api.GetLastError())�͌��Ȃ�.
            # �K�v�����Ȃ�܂��Ή�����.
            return False
        # �z�b�g�L�[�o�^������ɍX�V����.
        self._modifier = modifier
        self._key = key

        return True

    def set_callback(self, callback):
        self._callback = callback

    def get_callback(self):
        return self._callback

    def unregister_hotkey(self):
        could_unregister = ctypes.windll.user32.UnregisterHotKey(
            self._hwnd,
            self._index
        )
        if not(could_unregister):
            # �G���[�͖�������.
            pass

"""
hotkeymanager in util.win
- map
- hwnd
- maxindex
 - �����l1. ��� hotkeyconfig ����邽�тɃC���N�������g.
- ctor(hwnd)
 - map["reload"] = new HotkeyConfig(hwnd, 1)
 - map["open_snippet_folder"] = new HotkeyConfig(hwnd, 2)
 - �c
- register_hotkey(name, modifier, key)
 - map[name] ��������ΐV�K, ����΂�����g��.
- register_callback(name, callback)
- unregister_all()
- on_hotkey(hwnd, message, wparam, lparam)
 - @note �������Ԉ����Ă��������� on_hotkey(index, modifier, key)
 - index �ɊY������ callback ��T��, ��������s
"""
class IniLoader:
    def __init__(self):
        return

if __name__ == '__main__':
    pass
