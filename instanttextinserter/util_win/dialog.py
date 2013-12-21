# encoding: shift-jis

import ctypes
import win32con

"""
選択肢[キャンセル]は用意しない方針.
"""

def MessageBox(message, title, mbtype):
    return ctypes.windll.user32.MessageBoxA(
        0, #NULL
        str(message),
        str(title),
        mbtype
    )

def ok(message, title):
    MessageBox(message, title, win32con.MB_OK)

def is_ok(message, title):
    ret = MessageBox(message, title, win32con.MB_OKCANCEL)
    if ret==win32con.IDOK:
        return True
    return False

def is_yes(message, title):
    ret = MessageBox(message, title, win32con.MB_YESNO)
    if ret==win32con.IDYES:
        return True
    return False

def is_retry(message, title):
    ret = MessageBox(message, title, win32con.MB_RETRYCANCEL)
    if ret==win32con.IDRETRY:
        return True
    return False

if __name__ == '__main__':
    print ok("okですね", "キャンセルはありません")
    print is_ok("okですか?", "たいとるです")
    print is_yes("yesですか? タイトルは無しにしてます", "")
    print is_retry("retryします?", "retry dialog test")
