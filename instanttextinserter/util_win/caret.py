# encoding: shift-jis

import win32process
import win32gui
import ctypes

class RECT(ctypes.Structure):
 _fields_ = [
     ("left", ctypes.c_ulong),
     ("top", ctypes.c_ulong),
     ("right", ctypes.c_ulong),
     ("bottom", ctypes.c_ulong)
 ]

class GUITHREADINFO(ctypes.Structure):
 _fields_ = [
     ("cbSize", ctypes.c_ulong),
     ("flags", ctypes.c_ulong),
     ("hwndActive", ctypes.c_ulong),
     ("hwndFocus", ctypes.c_ulong),
     ("hwndCapture", ctypes.c_ulong),
     ("hwndMenuOwner", ctypes.c_ulong),
     ("hwndMoveSize", ctypes.c_ulong),
     ("hwndCaret", ctypes.c_ulong),
     ("rcCaret", RECT)
 ]

class Caret:
    def __init__(self, hwnd):
        self._hwnd = hwnd

    def get_pos(self):
        """
        キャレットの位置をデスクトップ座標 [x,y] で返す.
        @retval 空リスト 取得に失敗した
        """
        threadid, processid = win32process.GetWindowThreadProcessId(
            self._hwnd
        )
        guithreadinfo = self._get_guithreadinfo(threadid)

        carethandle = guithreadinfo.hwndCaret
        if carethandle==0:
            return []

        point_from_client = win32gui.ClientToScreen(
            carethandle,
            (0, 0)
        )

        caretpos = [point_from_client[0] + guithreadinfo.rcCaret.left,
               point_from_client[1] + guithreadinfo.rcCaret.top]
        return [int(x) for x in caretpos]

    def _get_guithreadinfo(self, threadid):
        guithreadinfo = GUITHREADINFO(cbSize=ctypes.sizeof(GUITHREADINFO))
        is_ok = ctypes.windll.user32.GetGUIThreadInfo(
            0,
            ctypes.byref(guithreadinfo)
        )
        '''
        if not(is_ok):
            return None
        '''
        return guithreadinfo

if __name__ == '__main__':
    import time
    import ctypes

    time.sleep(2)
    h = ctypes.windll.user32.GetForegroundWindow()
    caret = Caret(h)
    print caret.get_pos()

