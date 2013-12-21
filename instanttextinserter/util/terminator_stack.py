# encoding: shift-jis

import stack

class TerminatorStack:
    def __init__(self, do_ignore=False):
        self._stack = stack.Stack()
        self._do_ignore = do_ignore

    def __enter__(self):
        return self

    def __exit__(self, type, value, trackback):
        self._terminate_all()

    def push(self, func):
        self._stack.push(func)

    def _terminate_all(self):
        while not(self._stack.is_empty()):
            func = self._stack.pop()

            # �G���[�𖳎����Ȃ��ꍇ
            if not(self._do_ignore):
                func()
                continue

            # �G���[�𖳎�����ꍇ
            try:
                func()
            except:
                pass
