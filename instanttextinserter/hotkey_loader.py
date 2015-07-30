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
import hotkey_ini_loader
import selfinfo

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
        self._iniloader= hotkey_ini_loader.HotkeyIniLoader()

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
            callback_parameter = hotkey_entry.get_callback_parameter()

            # �Ή����� name �̃R�[���o�b�N�֐���������Ζ���.
            #
            # �R�[���o�b�N�֐���������Ȃ��p�^�[��
            # - name �� callback_map �ɑΉ����Ă��Ȃ�(�����Ȗ��O)
            # - name ���R�����g
            callback = None
            try:
                callback = hotkey_callback_map.callback_map[name]
            except KeyError:
                # ���󃆁[�U�����̌x���͏o���Ȃ����Ƃɂ���.
                # �R�����g�Ȃ̂���Ή�name�Ȃ̂��̋�ʂ����Ȃ�����.
                # @todo �R�����g���͌x���o���Ȃ��悤�ɏC������?
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

            self._hotkey_manager.register_callback(name, callback, callback_parameter)

    def unregister_hotkeys(self):
        print "START UnregisterHotkey" # @note �f�o�b�O�p. �p�ς񂾂����.
        self._hotkey_manager.unregister_all()

    def reload(self):
        """
        �z�b�g�L�[���ēo�^����.
        ���݂̓o�^���e���������, �ݒ�ǂݒ�����, �o�^������.
        """
        self.unregister_hotkeys()
        self.load_and_register_hotkeys()

    def get_hotkey_callback(self):
        return self._on_hotkey

    def _on_hotkey(self, hwnd, message, wparam, lparam):
        self._hotkey_manager.on_hotkey(hwnd, message, wparam, lparam)

if __name__ == '__main__':
    pass
