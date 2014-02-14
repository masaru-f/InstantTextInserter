# encoding: shift-jis

import util.log as log

class Reloader:
    """
    シングルトン.
    push されたリローダを順番にリロードする duck typing.
    push されたリローダの重複チェックは行っていないことに注意.
    """
    def __init__(self):
        self._reload_targets = []

    def push(self, reload_target):
        self._reload_targets.append(reload_target)

    def reload(self):
        for reload_target in self._reload_targets:
            try:
                reload_target.reload()
            except AttributeError as e:
                log.debug(
                    "the reload target is invalid./" +
                    str(e)
                )
# シングルトンインスタンス
inst = Reloader()

if __name__ == '__main__':
    pass
