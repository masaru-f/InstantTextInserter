# encoding: shift-jis

import ctypes
import win32api

'''
def is_already_running(programname):
    """
    Mutex を使うと開放処理が面倒くさいのでやめた.

    二重起動されているかどうかを返す.
    @param programname 二重起動の判定に使われる識別子文字列
    """
    ctypes.windll.kernel32.CreateMutexA(
        0,
        0,
        "DoubleLaunchGuard " + str(programname)
    )
    # ERROR_ALREADY_EXISTS = 183
    if win32api.GetLastError()==183:
        return True
    return False
'''

def is_already_running(classname):
    """
    二重起動されているかどうかを返す.
    @param classname 二重起動の判定に使われるウィンドウクラス名
    """
    windowname = 0
    hwnd = ctypes.windll.user32.FindWindowA(
        str(classname),
        windowname
    )
    if hwnd==0:
        return False
    return True
