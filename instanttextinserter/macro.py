# encoding: shift-jis

import os

import util_win.clipboard as clipboard

class SystemMacro:
    """
    システムマクロ.
    何に展開するかを内部的に定めてあるマクロ.
    """
    def __init__(self):
        # @note value は文字列 or 文字列を返す引数無し関数にすること.
        self._dict = {
            "equal"     :"=",
            "="         :"=",
            "cb"        :self._get_clipboard,
            "clipboard" :self._get_clipboard
        }

    def get(self, key):
        """
        key に対応する値を返す.
        取得処理に失敗した場合は空文字列を返す.

        @exception KeyError 値が存在しない
        """
        value = self._dict[key]

        if callable(value):
            ret = ""
            try:
                ret = value()
            except:
                pass
            return ret
        return value

    def _get_clipboard(self):
        return clipboard.Clipboard.get()

class Macro:
    """
    マクロ.
    %hoge% を対応する文字列に展開する.
    """
    MARK = "%"

    def __init__(self):
        self.systemmacro = SystemMacro()

    def deploy(self, s):
        """
        文字列 s 中のマクロを全て展開する.
        """
        ret = s
        mark = Macro.MARK
        idx_start = 0

        while True:
            # 始点を探す. 無ければ終了.
            idx_start = ret.find(mark, idx_start)
            if idx_start==-1:
                return ret

            # 終点を探す. 無ければ終了.
            # 終点探索開始位置は始点から一つずらす(始点を含めないため)
            idx_end = ret.find(mark, idx_start+1)
            if idx_end==-1:
                return ret

            # 始点終点間をマクロ名とみなして展開し,
            # 次の探索開始位置を確定.
            macroname = ret[idx_start+1:idx_end]
            macrovalue = macroname
            try:
                macrovalue = str(self.systemmacro.get(macroname))
                ret = ret[0:idx_start] + \
                      macrovalue + \
                      ret[idx_end+1:]
                idx_start = idx_start + len(macrovalue)
                continue
            except KeyError:
                pass

            # 展開できなかったので諦めて次の位置から探索を継続.
            idx_start = idx_end + 1
