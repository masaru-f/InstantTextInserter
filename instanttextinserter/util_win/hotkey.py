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
 - RegisterHotkey を呼び出す
 - 成功したら, 自身のメンバ変数を更新
- set_callback(callback)
- unregister_hotkey()
 - UnregisterHotkey を呼び出す
"""
class HotkeyConfig:
    """
    ホットキー一つ分の設定情報と振る舞いを持つ.

    """
    def __init__(self, hwnd, index):
        self._hwnd = hwnd
        self._index = index
        self._modifier = None
        self._key = None
        self._callback = None

    def register_hotkey(self, modifier, key):
        """
        新しいホットキー登録を行うと, 以前登録分は上書きされる.

        @param modifier win32con の MOD_HOGE の組み合わせ
        @param key 仮想キーコード
        @retval false 登録に失敗
        """
        is_hotkey_valid = ctypes.windll.user32.RegisterHotKey(
            self._hwnd,
            self._index,
            modifier,
            key
        )
        if not(is_hotkey_valid):
            # とりあえずエラー詳細(win32api.GetLastError())は見ない.
            # 必要そうならまた対応する.
            return False
        # ホットキー登録成功後に更新する.
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
            # エラーは無視する.
            pass

"""
hotkeymanager in util.win
- map
- hwnd
- maxindex
 - 初期値1. 一つ hotkeyconfig を作るたびにインクリメント.
- ctor(hwnd)
 - map["reload"] = new HotkeyConfig(hwnd, 1)
 - map["open_snippet_folder"] = new HotkeyConfig(hwnd, 2)
 - …
- register_hotkey(name, modifier, key)
 - map[name] が無ければ新規, あればそれを使う.
- register_callback(name, callback)
- unregister_all()
- on_hotkey(hwnd, message, wparam, lparam)
 - @note も少し間引いてもいいかも on_hotkey(index, modifier, key)
 - index に該当する callback を探し, それを実行
"""
class IniLoader:
    def __init__(self):
        return

if __name__ == '__main__':
    pass
