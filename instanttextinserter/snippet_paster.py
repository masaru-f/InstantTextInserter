# encoding: shift-jis

import os
from time import sleep

import util.log as log

import util_win.clipboard as clipboard
import util_win.keysimulator as keysimulator

import macro

class UnsupportedDecodeError(Exception):
    """
    �T�|�[�g���Ă��Ȃ������R�[�h�� decode ���鎞�ɓ������O.
    """
    def __init__(self, msg):
        self._msg = msg
        return
    def __str__(self):
        return self._msg

class SnippetPaster:
    # �}�N�����߃��[�`��������Ȃ��悤��
    # '%' �ň͂񂾕�����ɂ���,
    CURSOR_STRING = macro.Macro.MARK + "cursor" + macro.Macro.MARK

    def __init__(self):
        self._macro = macro.Macro()

    def paste(self, abbr, phrase):
        deployed_phrase = self._macro.deploy(phrase)
        try:
            clipboard.Clipboard.set(
                self._get_phrase_for_copy(deployed_phrase)
            )
        except Exception as e:
            log.warning(e)
            log.warning('failed setting fixed-phrase')
            # �����Ȃ��Ă͒�^���\�t�͍s���Ȃ�����, �����͒��f.
            return

        ks = keysimulator.KeySimulator()

        # �Z�k�`���͕��� BS �ŏ�������.
        # �Z�k�`�� ascii �����z�肵�ĂȂ�����, decode �͍s��Ȃ�.
        abbrlength = len(abbr)
        for i in range(abbrlength):
            ks.backspace()

        ks.ctrl_v()

        # �J�[�\���ʒu�ɖ߂邽�߂̕��������v�Z����,
        # ���̕����� Left key �ňړ�����.
        backcount = 0
        try:
            backcount = self.get_cursorbackcount(deployed_phrase)
        except (UnicodeDecodeError, UnsupportedDecodeError) as e:
            # �����������[�U�Ɍx������Ƃ���������
            # �����ĉ������Ȃ�.
            # �������������e�L�X�g�����̂܂ܓ\��t�����邱�ƂɂȂ�.
            log.warning("get_cursorbackcount() failed.\n" +
                        "abbr=%s, phrase=%s\n" % (abbr, phrase) +
                        "exception=%s" % str(e))
            pass
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
        @exception UnicodeDecodeError �f�R�[�h�Ɏ��s
        """
        # �������v�Z�𐳂����s������ unicode string �Ōv�Z����.
        # �擪�� cursorstring �̈ʒu�����߂�.
        u_container = self._flexible_decode(container)
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

    def _flexible_decode(self, src):
        """
        src �� decode �������̂�Ԃ�.
        windows �A�v������, �T�|�[�g����̂� shift-jis �݂̂�����j.
        @exception UnicodeDecodeError �f�R�[�h�Ɏ��s
        @exception UnsupportedDecodeError ���T�|�[�g�̕����R�[�h���f�R�[�h
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
