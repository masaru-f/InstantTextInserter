# encoding: shift-jis

import ctypes
import win32api

def is_already_running(programname):
    """
    ��d�N������Ă��邩�ǂ�����Ԃ�.
    @param programname ��d�N���̔���Ɏg���鎯�ʎq������
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
