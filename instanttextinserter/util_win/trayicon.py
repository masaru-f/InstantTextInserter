# encoding: shift-jis

import win32api
import win32gui
import win32con
import pywintypes

class TrayIcon:
    def __init__(self, hwnd, callback_message, hovertext):
        """
        @param hwnd 所有者ウィンドウのハンドル
        @param callback_message イベント発生時に所有者に投げるメッセージ
        """
        self.hwnd = hwnd
        self.callback_message = callback_message
        self.hovertext = hovertext

        self.hicon = None

        self._create()

    def _create(self):
        # param1 に NULL(0) を指定すると
        # 現在のプロセスを作成するために使われたファイルのパスを取得.
        self_filename = win32api.GetModuleFileName(0)

        self.hicon = win32gui.ExtractIconEx(self_filename, 0, 1)[0][0]

        # param2 は扱うアイコンの識別子.
        # 扱うアイコンは 1 つなので適当にした.
        notifyicondata = (
            self.hwnd,
            0,
            win32gui.NIF_MESSAGE | win32gui.NIF_ICON | win32gui.NIF_TIP,
            self.callback_message,
            self.hicon,
            self.hovertext
        )
        win32gui.Shell_NotifyIcon(
            win32gui.NIM_ADD,
            notifyicondata
        )

    def destroy(self):
        notifyicondata = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, notifyicondata)

        win32gui.DestroyIcon(self.hicon)
