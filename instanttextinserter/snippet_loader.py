# encoding: shift-jis

"""
利用者はシングルトンインスタンスを使うこと.
それ以外は補助クラスなので原則使うことはない.
"""

import os

import util.filereader as filereader

import dialog_wrapper
import selfinfo
import snippet_observer

def _load_and_merge():
    """
    snippet files 達を読み込んでリスト化する.

    @exception IOError ファイルを読み込めなかった
    @return 一要素に一行分の内容が入ったリスト

    """
    # ファイル一覧を取得.
    try:
        target_filelist = os.listdir(selfinfo.SNIPPETFOLDER_FULLPATH)
    except WindowsError as e:
        # ここに来た場合, プログラマ側のミスが原因かもしれない.
        # ->フォルダを用意していない等.
        # @todo 他にここに来る原因があるか調査(アクセス権無かった場合とか?).
        raise IOError(str(e))

    # 各ファイル内容を一つのリストにマージ.
    reader = filereader.FileReader()
    ret = []
    for f in target_filelist:
        ret += reader.read(
            os.path.join(selfinfo.SNIPPETFOLDER_FULLPATH, f)
        )

    # 各要素の末尾にある改行を取り除く.
    for i in range(len(ret)):
        ret[i] = ret[i].rstrip(os.linesep)

    return ret

def _convert_to_snippetdict(file_content_list):
    """
    マージされたスニペットファイル内容をパースして
    スニペット辞書("短縮形と定型文の組" の辞書)を作って返す.
    辞書を採用しているのは重複値を除くため.

    アルゴリズム.
    1. 全てのスニペットの開始(行)位置を取得しておく.
       この位置に短縮形も書いてあるので, 併せて取り出しておく.
    2. スニペット i の定型文は
       "スニペット i の開始位置" から "スニペット i+1 の開始位置"
       の間にあるので, これを取り出して定型文とする.

    @param [in] file_content_list ファイル内容一行が一要素に入ったリスト

    """
    ABBRNAME_SURROUNDING_MARK = "="

    # スニペット位置リストを構築
    # ただし行数は Zero Origin.
    # snippet_position_list = [
    #   ["sig@", 0]  短縮形 sgnt のスニペットは 0 行目から始まる
    #   ["for@", 3]  短縮形 for@ のスニペットは 3 行目から始まる
    #   …
    # ]
    snippet_position_list =[]
    for i in range(len(file_content_list)):
        _line = file_content_list[i]
        _len_line = len(_line)

        # 空行である or 開始行でないなら飛ばす
        if _len_line == 0:
            continue
        if _line[0] != ABBRNAME_SURROUNDING_MARK:
            continue

        _abbrname = _line.strip(ABBRNAME_SURROUNDING_MARK)

        snippet_position_list.append([_abbrname, i])

    # 末尾にダミーアイテムを追加
    # これをしないと最後のスニペットを取り出せない.
    snippet_position_list.append(["dummy", len(file_content_list)])

    # スニペット位置リストからスニペット辞書を構築
    dict_for_return = {}
    for i in range(len(snippet_position_list)):
        # ダミーは処理しない(out of rangeになる)
        if i==len(snippet_position_list)-1:
            break

        _snippet = snippet_position_list[i]
        _abbrname = _snippet[0]
        _snippetpos = _snippet[1]
        _next_snippetpos = snippet_position_list[i+1][1]

        _phrase = ""
        for j in range(_snippetpos+1, _next_snippetpos):
            _phrase = _phrase + \
                      file_content_list[j].rstrip(os.linesep) + \
                      os.linesep

        # 直前の連結処理により最後だけ余分な改行が入るので
        # それを取り除く.
        #
        # strip は使わないこと.
        # strip は複数個の改行を全て取り除いてしまうため
        # ユーザが意図して記述した定型文末尾の改行も無くなってしまう.
        _phrase = _phrase[0:-1*len(os.linesep)]

        dict_for_return[_abbrname] = _phrase

    return dict_for_return


class SnippetLoader:
    """
    シングルトン.

    読み込んだデータを通知するために Observer パターンを使用.
    ただし Subject は包含している.
    """
    def __init__(self):
        self._snippet_subject = snippet_observer.Subject()

    def attach(self, observer):
        self._snippet_subject.attach(observer)

    def reload(self):
        """
        スニペットを再読込した後, observer 達に再読込したデータを通知する.

        @note 必要なら排他制御すること.
        """
        file_content_list = []
        try:
            file_content_list = _load_and_merge()
        except IOError as e:
            dialog_wrapper.ok(
                "スニペットを読み込むことができません." + os.linesep +
                selfinfo.SNIPPETFOLDER_FULLPATH +
                " を確認してください."
            )
            return

        snippetdict = _convert_to_snippetdict(file_content_list)

        self._notify_all(snippetdict)

    def _notify_all(self, data_for_notify):
        self._snippet_subject.notify_all(
            data_for_notify
        )

#シングルトンインスタンス
inst = SnippetLoader()

if __name__ == '__main__':
    pass
