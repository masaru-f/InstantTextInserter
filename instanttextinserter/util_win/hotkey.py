# encoding: shift-jis

import ctypes
import win32api
import win32con

import keycode

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
        self._parameters = None

    def register_hotkey(self, modifier, key):
        """
        �V�����z�b�g�L�[�o�^���s����, �ȑO�o�^���͏㏑�������.

        @param modifier win32con �� MOD_HOGE �̑g�ݍ��킹
        @param key ���z�L�[�R�[�h
        @retval False �o�^�Ɏ��s
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

    def get_index(self):
        return self._index

    def set_callback(self, callback, parameters=None):
        """
        �R�[���o�b�N�֐��ɓn���p�����[�^�͈������.
        �����̏���n�������Ȃ�, list �Ȃ� dict �Ȃ�ōH�v����.
        ���������̏ꍇ�͓n���Ȃ��Ă��悢.
        """
        self._callback = callback
        self._parameters = parameters

    def get_callback(self):
        return self._callback

    def get_parameters(self):
        return self._parameters

    def unregister_hotkey(self):
        could_unregister = ctypes.windll.user32.UnregisterHotKey(
            self._hwnd,
            self._index
        )
        if not(could_unregister):
            # �G���[�͖�������.
            pass

class HotkeyManager:
    """
    �����̃z�b�g�L�[�ݒ���Ǘ�.
    �e�ݒ�͖��O(key-value �� key)�Ŏ���.
    """
    def __init__(self, hwnd):
        self._map = {}
        self._hwnd = hwnd
        self._max_index = 0 # �g�p�\�ȃz�b�g�L�[���ʎq�̉���

    def register_hotkey(self, name, modifier, key):
        """
        @todo �G���[���̐݌v
        @retval False �z�b�g�L�[�o�^�Ɏ��s
        """
        hotkey_config = None
        try:
            hotkey_config = self._map[name]
        except KeyError:
            pass

        if hotkey_config:
            is_hotkey_valid = hotkey_config.register_hotkey(modifier, key)
            return is_hotkey_valid

        hotkey_config = HotkeyConfig(self._hwnd, self._max_index)
        self._max_index = self._max_index + 1

        is_hotkey_valid = hotkey_config.register_hotkey(modifier, key)
        if not(is_hotkey_valid):
            return False

        self._map[name] = hotkey_config
        return True

    def register_callback(self, name, callback, parameters=None):
        hotkey_config = None
        try:
            hotkey_config = self._map[name]
        except KeyError:
            return

        hotkey_config.set_callback(callback, parameters)

    def unregister_all(self):
        hotkey_config_list = self._map.values()
        for hotkey_config in hotkey_config_list:
            hotkey_config.unregister_hotkey()

    def on_hotkey(self, hwnd, message, wparam, lparam):
        """
        �z�b�g�L�[�������̃R�[���o�b�N�֐��{��.
        �������ꂽ�z�b�g�L�[�ɑΉ�����R�[���o�b�N�֐����Ăяo��.

        @param wparam �z�b�g�L�[�̎��ʎq
        @param lparam ����WORD��modifier, ���WORD�̓L�[�R�[�h
        """
        pushee_index = wparam
        pushee_modifier = win32api.LOWORD(lparam)
        pushee_key = win32api.HIWORD(lparam)

        hotkey_config_list = self._map.values()

        for hotkey_config in hotkey_config_list:
            index = hotkey_config.get_index()
            if index != pushee_index:
                continue

            callback = hotkey_config.get_callback()
            if not(callable(callback)):
                # �������R�[���o�b�N�֐��������ĂȂ��Ƃ����ɗ���.
                # ����̓v���O���}�̃~�X.
                raise RuntimeError(
                    "Callback function is not callable./" +
                    "type of callback object:" + type(callback) + "/" +
                    "pushee_index:" + pushee_index
                )

            callback_params = hotkey_config.get_parameters()
            callback(callback_params)

if __name__ == '__main__':
    pass
