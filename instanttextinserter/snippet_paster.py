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

        offset_for_crlf = self._get_offset_for_crlf(u_container)

        # cursorstring ����������
        u_container = u_container.replace(SnippetPaster.CURSOR_STRING, "")

        return len(u_container)-cursorstring_position-offset_for_crlf

    def _get_offset_for_crlf(self, u_container):
        """
        CRLF �̒����� unicode string �ł� 2 �����Ƃ��Čv�Z����邪,
        �G�f�B�^��ł͈ꕶ�����Ƃ��Čv�Z�����.
        ���̂��߃J�[�\�����o�b�N������ۂ� CRLF �� n ��������
        n �������o�b�N����ʒu������Ă��܂�.
        �����h�����߂�, �o�b�N����ۂ� CRLF �����ʂ邩���v�Z��,
        ���̌�(��������߂�)�������o�b�N�J�E���g��������Ă��.
        """
        crlflist = u_container.split('\r\n')
        num_crlf = len(crlflist) # 1-origin. CRLF������Ȃ��Ȃ� 1
        for curlineno_0org in range(num_crlf):
            elm = crlflist[curlineno_0org]
            if elm.find(SnippetPaster.CURSOR_STRING)==-1:
            	continue
            # �ŏ��Ɍ������� cursor string ���g��.
            #
            # num_crlf �� 1-origin ���g���č������v�Z.
            return num_crlf - (curlineno_0org + 1)
        return 0

if __name__ == '__main__':
    pass
