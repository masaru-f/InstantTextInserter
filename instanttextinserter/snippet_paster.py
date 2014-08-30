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

        offset_for_crlf = self._get_offset_for_crlf(u_container)

        # cursorstring を除去する
        u_container = u_container.replace(SnippetPaster.CURSOR_STRING, "")

        return len(u_container)-cursorstring_position-offset_for_crlf

    def _get_offset_for_crlf(self, u_container):
        """
        CRLF の長さは unicode string では 2 文字として計算されるが,
        エディタ上では一文字分として計算される.
        そのためカーソルをバックさせる際に CRLF が n 個あったら
        n 文字分バックする位置がずれてしまう.
        これを防ぐために, バックする際に CRLF を何個通るかを計算し,
        その個数(これを求める)分だけバックカウントから引いてやる.
        """
        crlflist = u_container.split('\r\n')
        num_crlf = len(crlflist) # 1-origin. CRLFが一つもないなら 1
        for curlineno_0org in range(num_crlf):
            elm = crlflist[curlineno_0org]
            if elm.find(SnippetPaster.CURSOR_STRING)==-1:
            	continue
            # 最初に見つかった cursor string を使う.
            #
            # num_crlf の 1-origin を使って差分を計算.
            return num_crlf - (curlineno_0org + 1)
        return 0

if __name__ == '__main__':
    pass
