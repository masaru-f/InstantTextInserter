# encoding: shift-jis

import os
from time import sleep

import util_win.clipboard as clipboard
import util_win.keysimulator as keysimulator

import macro

class SnippetPaster:
    # �}�N�����߃��[�`��������Ȃ��悤��
    # '%' �ň͂񂾕�����ɂ���,
    CURSOR_STRING = macro.Macro.MARK + "cursor" + macro.Macro.MARK

    def __init__(self):
        self._macro = macro.Macro()

    def paste(self, abbr, phrase):
        deployed_phrase = self._macro.deploy(phrase)

        clipboard.Clipboard.set(
            self._get_phrase_for_copy(deployed_phrase)
        )

        ks = keysimulator.KeySimulator()

        # �Z�k�`���͕��� BS �ŏ�������.
        # ������̒����𐳂������߂邽�� unicode string �Ōv�Z����.
        # abbr �Ƃ��� ascii ���������ĂȂ���, �܂��O�̂���.
        abbrlength = len(abbr.decode())
        for i in range(abbrlength):
            ks.backspace()

        ks.ctrl_v()

        # �J�[�\���ʒu�ɖ߂邽�߂̕��������v�Z����,
        # ���̕����� Left key �ňړ�����.
        backcount = self.get_cursorbackcount(deployed_phrase)
        for i in range(backcount):
            ks.left()

    def _get_phrase_for_copy(self, phrase):
        """
        �N���b�v�{�[�h�ɃR�s�[����p�� phrase ��Ԃ�.
        """
        # cursor string ������
        return phrase.replace(SnippetPaster.CURSOR_STRING, "")

    def get_cursorbackcount(self, container):
        """
        cursor string �ʒu�ɃJ�[�\���������Ă��邽�߂�
        ���������߂�΂�������Ԃ�.
        �߂�K�v��������� 0.

        @param container cursorstring ���܂ޕ�����
        """
        # �������v�Z�𐳂����s������ unicode string �Ōv�Z����.
        # �擪�� cursorstring �̈ʒu�����߂�.
        u_container = container.decode()
        cursorstring_position = u_container.find(SnippetPaster.CURSOR_STRING)

        # ������Ȃ�
        if cursorstring_position==-1:
            return 0

        # cursorstring ����������
        u_container = u_container.replace(SnippetPaster.CURSOR_STRING, "")

        return len(u_container)-cursorstring_position

if __name__ == '__main__':
    pass
