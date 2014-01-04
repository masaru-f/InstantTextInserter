# encoding: shift-jis

import os

class SystemMacro:
    """
    �V�X�e���}�N��.
    ���ɓW�J���邩������I�ɒ�߂Ă���}�N��.
    """
    def __init__(self):
        # @note value �͕����� or �������Ԃ����������֐��ɂ��邱��.
        self._dict = {
            "equal"     :"=",
            "="         :"=",
        }

    def get(self, key):
        """
        key �ɑΉ�����l��Ԃ�.
        �擾�����Ɏ��s�����ꍇ�͋󕶎����Ԃ�.

        @exception KeyError �l�����݂��Ȃ�
        """
        value = self._dict[key]

        if callable(value):
            ret = ""
            try:
                ret = value()
            except:
                pass
            return ret
        return value

class Macro:
    """
    �}�N��.
    %hoge% ��Ή����镶����ɓW�J����.
    """
    MARK = "%"

    def __init__(self):
        self.systemmacro = SystemMacro()

    def deploy(self, s):
        """
        ������ s ���̃}�N����S�ēW�J����.
        """
        ret = s
        mark = Macro.MARK
        idx_start = 0

        while True:
            # �n�_��T��. ������ΏI��.
            idx_start = ret.find(mark, idx_start)
            if idx_start==-1:
                return ret

            # �I�_��T��. ������ΏI��.
            # �I�_�T���J�n�ʒu�͎n�_�������炷(�n�_���܂߂Ȃ�����)
            idx_end = ret.find(mark, idx_start+1)
            if idx_end==-1:
                return ret

            # �n�_�I�_�Ԃ��}�N�����Ƃ݂Ȃ��ēW�J��,
            # ���̒T���J�n�ʒu���m��.
            macroname = ret[idx_start+1:idx_end]
            macrovalue = macroname
            try:
                macrovalue = str(self.systemmacro.get(macroname))
                ret = ret[0:idx_start] + \
                      macrovalue + \
                      ret[idx_end+1:]
                idx_start = idx_start + len(macrovalue)
                continue
            except KeyError:
                pass

            # �W�J�ł��Ȃ������̂Œ��߂Ď��̈ʒu����T�����p��.
            idx_start = idx_end + 1
