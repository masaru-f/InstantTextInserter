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

class HotkeyLoader:
    """
    ホットキーの登録を行う.
    設定ファイル読み込みから実際の登録までの一連の処理を担当.

    用意する操作は以下の二つだけ.
    - 設定ファイルから全設定を読み込んで登録する
    - 登録されている設定全てをクリアする
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
            dialog_wrapper.ok("設定ファイルの読込に失敗./" + str(e))
            return

        if not(hotkey_entries):
            return

        import hotkey_callback_map
        for hotkey_entry in hotkey_entries:
            name = hotkey_entry.get_name()
            modifier = hotkey_entry.get_modifier()
            keycode = hotkey_entry.get_keycode()

            # 対応する name のコールバック関数が無ければ無効.
            # つまり callback_map に登録した name のみが有効.
            callback = None
            try:
                callback = hotkey_callback_map.callback_map[name]
            except KeyError:
                print name # @note デバッグ用途なので用が済んだら消す.
                continue

            is_valid_hotkey = self._hotkey_manager.register_hotkey(
                name, modifier, keycode
            )
            # 既に別のホットキーが登録されている場合などに失敗する.
            # そう何回も通るケースは少ないだろうから,
            # 何回も dialog が出てウザいってことは無いと思う.
            if not(is_valid_hotkey):
                dialog_wrapper.ok(
                    "ホットキー " + name + " の登録に失敗しました." +
                    os.linesep + "ErrorCode:" + str(win32api.GetLastError())
                )
                continue

            self._hotkey_manager.register_callback(name, callback)

    def unregister_hotkeys(self):
        print "START UnregisterHotkey" # @note デバッグ用. 用済んだら消す.
        self._hotkey_manager.unregister_all()

    def get_hotkey_callback(self):
        return self._on_hotkey

    def _on_hotkey(self, hwnd, message, wparam, lparam):
        self._hotkey_manager.on_hotkey(hwnd, message, wparam, lparam)

if __name__ == '__main__':
    pass
