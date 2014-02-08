# encoding: shift-jis

import ctypes
import win32api
import win32con

import keycode

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

    def get_index(self):
        return self._index

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
class HotkeyManager:
    """
    複数のホットキー設定を管理.
    各設定は名前(key-value の key)で識別.
    """
    def __init__(self, hwnd):
        self._map = {}
        self._hwnd = hwnd
        self._max_index = 0 # 使用可能なホットキー識別子の下限

    def register_hotkey(self, name, modifier, key):
        """
        @todo エラー時の設計
        @retval False ホットキー登録に失敗
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

    def register_callback(self, name, callback):
        hotkey_config = None
        try:
            hotkey_config = self._map[name]
        except KeyError:
            return

        hotkey_config.set_callback(callback)

    def unregister_all(self):
        hotkey_config_list = self._map.keys()
        for hotkey_config in hotkey_config_list:
            hotkey_config.unregister_hotkey()

    def on_hotkey(self, hwnd, message, wparam, lparam):
        """
        ホットキー押下時のコールバック関数本体.
        押下されたホットキーに対応するコールバック関数を呼び出す.

        @param wparam ホットキーの識別子
        @param lparam 下位WORDはmodifier, 上位WORDはキーコード
        """
        pushee_index = wparam
        pushee_modifier = win32api.LOWORD(lparam)
        pushee_key = win32api.HIWORD(lparam)

        hotkey_config_list = self._map.keys()

        for hotkey_config in hotkey_config_list:
            index = hotkey_config.get_index()
            if index != pushee_index:
                continue

            callback = hotkey_config.get_callback()
            if not(callable(callback)):
                # 正しいコールバック関数が入ってないとここに来る.
                # これはプログラマ側のエラー.
                # @todo プログラムエラーであることがわかるようにしたい.
                # @todo コールバック関数の正しさはどこで検証する? \n
                #       ここ or セットするところ のいずれかだろう.
                return

            callback()

if __name__ == '__main__':
    pass
