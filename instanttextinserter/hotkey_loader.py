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
    ホットキーの登録を行う.
    設定ファイル読み込みから実際の登録までの一連の処理を担当.

    用意する操作は以下の二つだけ.
    - 設定ファイルから全設定を読み込んで登録する
    - 登録されている設定全てをクリアする
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
