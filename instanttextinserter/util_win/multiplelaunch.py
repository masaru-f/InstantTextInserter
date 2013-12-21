# encoding: shift-jis

import ctypes
import win32api

def is_already_running(programname):
    """
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
