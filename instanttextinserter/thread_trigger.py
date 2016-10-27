# encoding: shift-jis

import copy

import util_win.keygetter as keygetter

import snippet_manager
import snippet_observer
import snippet_loader
import thread_interface

""" [用語定義]
- 短縮形(abbr)
- 定型文(phrase)
- スニペット(snippet) : 短縮形と定型文の組 """

class TriggerThread(
    thread_interface.IWatcherThread,
    snippet_observer.IObserver
):
    """ 短縮形の入力を監視するスレッド.
    入力されたら対応する定型文を挿入する.

    スニペットデータが更新された時に通知してほしいので,
    Observer を使って実現している. """

    # スレッドループ待機時間とCPU負担の関係.
    # 測定日: 15/05/07(Thu), 環境: Win7(32bit)
    # (sec) (cpu usage)
    # 0.01 : 1.3-2.0
    # 0.02 : 0.6-1.1
    # 0.03 : 0.5-0.7
    # 0.05 : 0.3-0.5
    # 0.05でも捕捉漏れはほとんど発生せず. 従来通り0.03で様子見る.
    INTERVAL_SEC = 0.03

    def __init__(self):
        thread_interface.IWatcherThread.__init__(
            self,
            "trigger thread",
            TriggerThread.INTERVAL_SEC
        )

    # implement the thread interface
    # ------------------------------

    def _init(self):
        self._getter = keygetter.KeyGetter()
        self._manager = snippet_manager.SnippetManager()

        # リロードしても良い場合に立つ.
        # リロード後は降ろす.
        self._can_reload = False

        # 通知されたスニペットデータを入れておく領域.
        self._snippet_container = None

        snippet_loader.inst.attach(self)
        # スニペットデータの初回時読み込み.
        snippet_loader.inst.reload()

    def _procedure(self):
        # 通知されていれば再読込する.
        if self._can_reload:
            self._reload()
            self._can_reload = False

        # 修飾キーが押されていた場合は照合を無視する.
        # これをしないと abbr=(space)(semicolon) が (space)(plus) でも
        # ひっかかるようになって煩わしい.
        for i in snippet_manager.SnippetManager.modifier_keycode_list:
            if self._getter.is_pushed(i):
                return

        for i in snippet_manager.SnippetManager.supported_keycode_list:
            if self._getter.is_pushed_once(i):
                self._manager.input(i)

    def _term(self):
        pass

    # implement the observer interface
    # --------------------------------

    def notify(self, snippet_container):
        # これだと他の ovserver に通知された snippet_container
        # も変更してしまう(参照渡しなので)恐れがあるため
        # 念のため deepcopy にする.
        #self._snippet_container = snippet_container
        self._snippet_container = copy.deepcopy(snippet_container)
        self._can_reload = True

    # private methods
    # ---------------

    def _reload(self):
        """ スニペットデータを再読込する. """
        # 現在登録されてる内容をクリアする.
        # これしないと再読込ではなく append になってしまう.
        self._manager.clear()

        # container からスニペットを一件ずつ取り出して追加.
        for key in self._snippet_container.keys():
            abbr = key
            phrase = self._snippet_container[key]
            self._manager.add(abbr, phrase)

if __name__ == '__main__':
    pass
