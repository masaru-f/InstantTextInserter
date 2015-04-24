# encoding: shift-jis

import ctypes
import win32clipboard
import win32con

class Clipboard:
    """
    ������̂� CF_TEXT �̂�.
    ��X���b�h�Z�[�t�Ȃ̂Ń}���`�X���b�h�Ŏg��Ȃ�����.
    static �ł̎����͂Ƃ肠������, ��肠��Ȃ�ς���\��.
    """
    @staticmethod
    def get():
        """
        �N���b�v�{�[�h�̒��g��Ԃ�.
        @retval �󕶎��� �擾�Ɏ��s or ���������ĂȂ�
        """
        if not(Clipboard._open()):
            return ""

        if not(Clipboard._is_available()):
            return ""

        ret = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        Clipboard._close()
        return ret

    @staticmethod
    def set(s):
        """
        �w�肵����������N���b�v�{�[�h�Ɋi�[����.
        �N���b�v�{�[�h�ւ̃R�s�[�̓O���[�o���q�[�v���g���K�v������.
        """
        if not(isinstance(s, str)):
            return False

        # �O���[�o���q�[�v�̈���m��
        hMem = ctypes.windll.kernel32.GlobalAlloc(
            win32con.GMEM_MOVEABLE,
            len(s)+1
        )
        if hMem==0:
            return False
        # �m�ۂ����̈�����b�N.
        pMemBlock = ctypes.windll.kernel32.GlobalLock(hMem)
        if pMemBlock==0:
            return False
        # �m�ۂ����̈�ɃR�s�[����f�[�^����������.
        pBuffer = ctypes.windll.kernel32.lstrcpy(
            ctypes.c_char_p(pMemBlock),
            s
        )
        if pBuffer==0:
            ctypes.windll.kernel32.GlobalUnlock(hMem)
            return False
        ctypes.windll.kernel32.GlobalUnlock(hMem)

        # �N���b�v�{�[�h���J��.
        if not(Clipboard._open()):
            return False
        # �N���b�v�{�[�h�Ɏc���Ă���f�[�^������.
        # ��������Ȃ��Ə�肭�R�s�[����Ȃ����Ƃ�����.
        win32clipboard.EmptyClipboard()

        # �m�ۂ����̈�ɏ������񂾓��e���N���b�v�{�[�h�ɏ�������.
        ret = True
        try:
            win32clipboard.SetClipboardData(win32con.CF_TEXT, hMem)
        except:
            ret = False

        Clipboard._close()
        return ret

    @staticmethod
    def _open():
        """
        �N���b�v�{�[�h�����ɊJ���Ă��邩�ǂ�����Ԃ�.
        �J���ĂȂ���ΊJ��.
        �J����Ă����, �V���ɊJ����������͕̂���.
        """
        ret = win32clipboard.OpenClipboard()
        if(ret==None):
            return True
        Clipboard._close()
        return False

    @staticmethod
    def _close():
        # �J���ĂȂ����Ɏ��s����Ƃ�������̂ŋz��.
        try:
            win32clipboard.CloseClipboard()
        except:
            pass
        return

    @staticmethod
    def _is_available():
        ret = win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT)
        if(ret!=0):
            return True
        Clipboard._close()
        return False

if __name__ == '__main__':
    print Clipboard.set("hoge�ق����[")
    print Clipboard.get()
    pass

