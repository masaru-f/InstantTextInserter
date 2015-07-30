# encoding: shift-jis

import copy
import os

import win32con

import util.filereader as filereader

import util_win.keycode as keycode

import selfinfo

class HotkeyEntry:
    """
    設定ファイルから読み込んだ, ホットキー設定一つ分.
    """
    SEPARATOR = ","
    def __init__(self, line):
        """
        @param line "(name),(modifier),(key)" なる文字列
        @exception RuntimeError 入力文字列の形式が不正
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
        if self._name[0] == ';':
            raise RuntimeError("this name is comment.")

        if self._modifier == 0:
            raise RuntimeError("modifier is invalid.")

        if self._keycode == 0:
            raise RuntimeError("keycode is invalid.")

        self._callback_parameter = None
        try:
            self._callback_parameter = ls[3]
        except IndexError:
            # コールバックに渡すパラメータは無くてもよい.
            pass

    def get_name(self):
        return self._name

    def get_modifier(self):
        return self._modifier

    def get_keycode(self):
        return self._keycode

    def get_callback_parameter(self):
        return self._callback_parameter

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

class HotkeyIniLoader:
    """
    ホットキー用設定ファイルを読み込む.
    """
    def __init__(self):
        self._content = None

    def read_all(self):
        """
        @exception IOError ファイルが開けない
        """
        reader = filereader.FileReader()

        try:
            self._content = reader.read(selfinfo.HOTKEYCONFIG_FULLPATH)
        except IOError:
            raise IOError("Cannot read " + selfinfo.HOTKEYCONFIG_FULLPATH)

        # 末尾の改行を取り除く.
        # @todo util 側を修正したいが影響範囲がでかい. 要精査.
        for i in range(len(self._content)):
            self._content[i] = self._content[i].strip(os.linesep)

        # 書式が有効な設定のみ抽出
        ret_list = []
        for line in self._content:
            hotkey_entry = None
            try:
                hotkey_entry = HotkeyEntry(line)
            except RuntimeError:
                # 書式が不正な分は無視.
                continue
            ret_list.append(copy.deepcopy(hotkey_entry))

        return ret_list

if __name__ == '__main__':
    pass
