# encoding: shift-jis

class Stack:
    """
    RAII�͓��ڂ��Ă��Ȃ��̂�,
    �����I�ȉ�����K�v�ȗv�f��push���Ȃ�����.
    """
    def __init__(self):
        self.stack = []

    def push(self, elm):
        self.stack.append(elm)

    def pop(self):
        """
        @exception IndexError �X�^�b�N����
        """
        return self.stack.pop()

    def is_empty(self):
        if self.get_count()==0:
            return True
        return False

    def get_count(self):
        """
        �ʏ�͎g��Ȃ��Ǝv��.
        �f�o�b�O�p�ɗp�ӂ���.
        """
        return len(self.stack)
