# encoding: shift-jis

import os
from time import sleep

import util.log as log

import util_win.clipboard as clipboard
import util_win.keysimulator as keysimulator

import macro

class UnsupportedDecodeError(Exception):
    """
    サポートしていない文字コードを decode する時に投げる例外.
    """
    def __init__(self, msg):
        self._msg = msg
        return
    def __str__(self):
        return self._msg

class SnippetPaster:
    # マクロ解釈ルーチンが狂わないように
    # '%' で囲んだ文字列にする,
    CURSOR_STRING = macro.Macro.MARK + "cursor" + macro.Macro.MARK

    def __init__(self):
        self._macro = macro.Macro()

    def paste(self, abbr, phrase):
        # 元々あったクリップボード内容を退避しておき,
        # paste 後に元に戻す.
        original_clipboardstr = clipboard.Clipboard.get()

        deployed_phrase = self._macro.deploy(phrase)
        clipboard.Clipboard.set(
            self._get_phrase_for_copy(deployed_phrase)
        )

        ks = keysimulator.KeySimulator()

        # 短縮形入力分を BS で消去する.
        # 短縮形は ascii しか想定してないため, decode は行わない.
        abbrlength = len(abbr)
        for i in range(abbrlength):
            ks.backspace()

        ks.ctrl_v()

        # カーソル位置に戻るための文字数を計算して,
        # その分だけ Left key で移動する.
        backcount = 0
        try:
            backcount = self.get_cursorbackcount(deployed_phrase)
        except (UnicodeDecodeError, UnsupportedDecodeError) as e:
            # いちいちユーザに警告するとうざいため
            # あえて何もしない.
            # 文字化けしたテキストがそのまま貼り付けられることになる.
            log.warning("get_cursorbackcount() failed.\n" +
                        "abbr=%s, phrase=%s\n" % (abbr, phrase) +
                        "exception=%s" % str(e))
            pass
        for i in range(backcount):
            ks.left()

        # ここで退避内容を元に戻すのだが...即座に戻してしまうと,
        # ctrl+v 貼り付けが実行される前に戻ってしまい,
        # 常に「ただの ctrl+v で貼り付けた」挙動になってしまう.
        #
        # 原因は keybd_event の仕様.
        # keybd_event はキーボード入力確定後に次に進むわけではない.
        #
        # 暫定対処として少しだけ sleep を入れる.
        # @todo sleep対処療法じゃない方法が欲しい...
        #
        # [値の試行結果]
        # 0.0  -> sleep無しだと, 常に退避内容がpasteされる.
        # 0.01 -> 常に Access Denied エラーが出る.
        # 0.1  -> 連続で定型文挿入した時にもたつくことがある
        sleep(0.05)
        self._retry_clipboard_set(original_clipboardstr)

    def _retry_clipboard_set(self, s):
        """
        win32clipboard.OpenClipboard で error=5 Access Denied 例外が出る.
        原因は不明だが, keybd_event と sleep と OpenClipboard の複合?
        とりあえず何回か試行してみる.
        それでもダメならエラーは無視, つまり set 失敗を容認する.
        """
        interval = 0.01
        max_count = 10
        for i in range(max_count):
            try:
                clipboard.Clipboard.set(s)
                break
            except Exception as e:
                log.warning(e)
                log.warning('interval:%d[s], count:(%d/%d)' \
                            % (interval*1000, i+1, max_count))
                log.warning('failed in _retry_clipboard_set.')
            sleep(interval)
        return

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
        @exception UnicodeDecodeError デコードに失敗
        """
        # 文字数計算を正しく行うため unicode string で計算する.
        # 先頭の cursorstring の位置を求める.
        u_container = self._flexible_decode(container)
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

    def _flexible_decode(self, src):
        """
        src を decode したものを返す.
        windows アプリだし, サポートするのは shift-jis のみする方針.
        @exception UnicodeDecodeError デコードに失敗
        @exception UnsupportedDecodeError 未サポートの文字コードをデコード
        """
        #codename_list = ['shift-jis', 'utf-8', 'cp932', 'euc-jp']
        codename_list = ['shift-jis']
        for elm in codename_list:
            try:
                ret = src.decode(elm)
                return ret
            except UnicodeDecodeError:
                continue

        raise UnsupportedDecodeError('Your charset is not supported.')

if __name__ == '__main__':
    pass
