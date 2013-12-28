# encoding: shift-jis

import os
from time import sleep

import util_win.clipboard as clipboard
import util_win.keysimulator as keysimulator

import macro

class SnippetPaster:
    # マクロ解釈ルーチンが狂わないように
    # '%' で囲んだ文字列にする,
    CURSOR_STRING = macro.Macro.MARK + "cursor" + macro.Macro.MARK

    def __init__(self):
        self._macro = macro.Macro()

    def paste(self, abbr, phrase):
        deployed_phrase = self._macro.deploy(phrase)

        clipboard.Clipboard.set(
            self._get_phrase_for_copy(deployed_phrase)
        )

        ks = keysimulator.KeySimulator()

        # 短縮形入力分を BS で消去する.
        # 文字列の長さを正しく求めるため unicode string で計算する.
        # abbr として ascii しか許してないが, まあ念のため.
        abbrlength = len(abbr.decode())
        for i in range(abbrlength):
            ks.backspace()

        ks.ctrl_v()

        # カーソル位置に戻るための文字数を計算して,
        # その分だけ Left key で移動する.
        backcount = self.get_cursorbackcount(deployed_phrase)
        for i in range(backcount):
            ks.left()

    def _get_phrase_for_copy(self, phrase):
        """
        クリップボードにコピーする用の phrase を返す.
        """
        # cursor string を除去
        return phrase.replace(SnippetPaster.CURSOR_STRING, "")

    def get_cursorbackcount(self, container):
        """
        cursor string 位置にカーソルを持ってくるために
        何文字分戻ればいいかを返す.
        戻る必要が無ければ 0.

        @param container cursorstring を含む文字列
        """
        # 文字数計算を正しく行うため unicode string で計算する.
        # 先頭の cursorstring の位置を求める.
        u_container = container.decode()
        cursorstring_position = u_container.find(SnippetPaster.CURSOR_STRING)

        # 見つからない
        if cursorstring_position==-1:
            return 0

        # cursorstring を除去する
        u_container = u_container.replace(SnippetPaster.CURSOR_STRING, "")

        return len(u_container)-cursorstring_position

if __name__ == '__main__':
    pass
