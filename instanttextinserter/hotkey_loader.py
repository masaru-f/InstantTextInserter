# encoding: shift-jis

import copy
import ctypes # for hotkey prototype
import os

import win32api
import win32con

import util.filereader as filereader

import util_win.hotkey as hotkey
import util_win.keycode as keycode

import dialog_wrapper
import selfinfo

class HotkeyEntry:
    """
    �ݒ�t�@�C������ǂݍ���, �z�b�g�L�[�ݒ���.
    """
    SEPARATOR = ","
    def __init__(self, line):
        """
        @param line "(name),(modifier),(key)" �Ȃ镶����
        @exception RuntimeError ���͕�����̌`�����s��
        """
        ls = line.split(HotkeyEntry.SEPARATOR)
        ls = [elm.strip() for elm in ls]

        try:
            self._name = ls[0]
            self._modifier = self._to_interger_modifier(ls[1])
            self._keycode = self._to_interger_keycode(ls[2])
        except IndexError:
            raise RuntimeError("list out of index.")

        if len(self._name)==0:
            raise RuntimeError("name is empty.")

        if self._modifier == 0:
            raise RuntimeError("modifier is invalid.")

        if self._keycode == 0:
            raise RuntimeError("keycode is invalid.")

    def get_name(self):
        return self._name

    def get_modifier(self):
        return self._modifier

    def get_keycode(self):
        return self._keycode

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
    """
    �z�b�g�L�[�p�ݒ�t�@�C����ǂݍ���.
    """
    def __init__(self):
        self._content = None

    def read_all(self):
        """
        @exception IOError �t�@�C�����J���Ȃ�
        """
        reader = filereader.FileReader()

        try:
            self._content = reader.read(selfinfo.HOTKEYCONFIG_FULLPATH)
        except IOError:
            raise IOError("Cannot read " + selfinfo.HOTKEYCONFIG_FULLPATH)

        # �����̉��s����菜��.
        # @todo util �����C�����������e���͈͂��ł���. �v����.
        for i in range(len(self._content)):
            self._content[i] = self._content[i].strip(os.linesep)

        # �������L���Ȑݒ�̂ݒ��o
        ret_list = []
        for line in self._content:
            hotkey_entry = None
            try:
                hotkey_entry = HotkeyEntry(line)
            except RuntimeError:
                # �������s���ȕ��͖���.
                continue
            ret_list.append(copy.deepcopy(hotkey_entry))

        return ret_list

class HotkeyLoader:
    """
    �z�b�g�L�[�̓o�^���s��.
    �ݒ�t�@�C���ǂݍ��݂�����ۂ̓o�^�܂ł̈�A�̏�����S��.

    �p�ӂ��鑀��͈ȉ��̓����.
    - �ݒ�t�@�C������S�ݒ��ǂݍ���œo�^����
    - �o�^����Ă���ݒ�S�Ă��N���A����
    """
    def __init__(self, hwnd):
        self._hwnd = hwnd
        self._hotkey_manager = hotkey.HotkeyManager(hwnd)
        self._iniloader= IniLoader()

    def load_and_register_hotkeys(self):
        hotkey_entries = None
        try:
            hotkey_entries = self._iniloader.read_all()
        except IOError as e:
            dialog_wrapper.ok("�ݒ�t�@�C���̓Ǎ��Ɏ��s./" + str(e))
            return

        if not(hotkey_entries):
            return

        import hotkey_callback_map
        for hotkey_entry in hotkey_entries:
            name = hotkey_entry.get_name()
            modifier = hotkey_entry.get_modifier()
            keycode = hotkey_entry.get_keycode()

            # �Ή����� name �̃R�[���o�b�N�֐���������Ζ���.
            # �܂� callback_map �ɓo�^���� name �݂̂��L��.
            callback = None
            try:
                callback = hotkey_callback_map.callback_map[name]
            except KeyError:
                print name # @note �f�o�b�O�p�r�Ȃ̂ŗp���ς񂾂����.
                continue

            is_valid_hotkey = self._hotkey_manager.register_hotkey(
                name, modifier, keycode
            )
            # ���ɕʂ̃z�b�g�L�[���o�^����Ă���ꍇ�ȂǂɎ��s����.
            # ����������ʂ�P�[�X�͏��Ȃ����낤����,
            # ����� dialog ���o�ăE�U�����Ă��Ƃ͖����Ǝv��.
            if not(is_valid_hotkey):
                dialog_wrapper.ok(
                    "�z�b�g�L�[ " + name + " �̓o�^�Ɏ��s���܂���." +
                    os.linesep + "ErrorCode:" + str(win32api.GetLastError())
                )
                continue

            self._hotkey_manager.register_callback(name, callback)

    def unregister_hotkeys(self):
        print "START UnregisterHotkey" # @note �f�o�b�O�p. �p�ς񂾂����.
        self._hotkey_manager.unregister_all()

    def get_hotkey_callback(self):
        return self._on_hotkey

    def _on_hotkey(self, hwnd, message, wparam, lparam):
        self._hotkey_manager.on_hotkey(hwnd, message, wparam, lparam)

if __name__ == '__main__':
    pass
