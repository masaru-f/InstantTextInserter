# encoding: shift-jis

class Stack:
    """
    RAIIは搭載していないので,
    明示的な解放が必要な要素はpushしないこと.
    """
    def __init__(self):
        self.stack = []

    def push(self, elm):
        self.stack.append(elm)

    def pop(self):
        """
        @exception IndexError スタックが空
        """
        return self.stack.pop()

    def is_empty(self):
        if self.get_count()==0:
            return True
        return False

    def get_count(self):
        """
        通常は使わないと思う.
        デバッグ用に用意した.
        """
        return len(self.stack)
