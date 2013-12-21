# encoding: shift-jis

"""
snippet data に関する Observer パターン.
通知する/されるデータは snippet container を想定しているが,
テストや汎用化のため型チェックは実装していない.
"""

class IObserver:
    """
    通知されたデータをどうするかは派生クラス次第.
    通知されたデータに編集を加える場合, 派生クラス側で deepcopy すること.
    """
    def notify(self, snippet_container):
        raise NotImplementedError

class Subject:
    """
    observer の登録方法と通知方法は共通しているので共通化.
    何を通知するかは利用者側が決める.
    """
    def __init__(self):
        self._observerlist = []

    def attach(self, observer):
        if observer in self._observerlist:
            # 既に登録されていれば無視する
            return
        self._observerlist.append(observer)

    def notify_all(self, snippet_container):
        for observer in self._observerlist:
            observer.notify(snippet_container)
