# encoding: shift-jis

import ctypes # for hotkey prototype
import win32con

class HotkeyLoader:
    def __init__(self, hwnd):
        self._hwnd = hwnd
        return

    def register_hotkey(self):
        canHotkey = ctypes.windll.user32.RegisterHotKey(
            self._hwnd,
            1234, # 識別子. 値はとりあえず適当.
            win32con.MOD_CONTROL | win32con.MOD_SHIFT,
            76 # L
        )
        if not(canHotkey):
            print "RegisterHotkey1 failed."
            print "GetLastError:" + str(win32api.GetLastError())

    def unregister_hotkey(self):
        try:
            couldUnregister = ctypes.windll.user32.UnregisterHotKey(
                self._hwnd,
                1234,
            )
            if not(couldUnregister):
                print "unregister hotkey1 failed..."
        except:
            pass

    def on_hotkey(self, hwnd, message, wparam, lparam):
        print "from hotkeyloader, " + str(self)
        print "hwnd:" + str(hwnd)
        print "message:" + str(message)
        print "wparam:" + str(wparam)
        print "lparam:" + str(lparam)

    def get_hotkey_callback(self):
        return self.on_hotkey

if __name__ == '__main__':
    pass
