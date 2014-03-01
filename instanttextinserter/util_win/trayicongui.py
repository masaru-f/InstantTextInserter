# encoding: shift-jis

#import ctypes # for hotkey prototype
import win32gui
import win32con
import win32api

import util_win.trayicon as trayicon

"""
[使い方]
- MainWindow クラスを使って GUI を構築する.
- ウィンドウハンドルが欲しい場合は Hwnd シングルトンクラスを使う.
"""

class MainLoop:
    """
    GUI ループの開始と停止を行う.
    MainWindow から呼び出すことを想定.
    """
    def __init__(self):
        self._can_running = True

    def start(self):
        while self._can_running:
            b, msg = win32gui.GetMessage(0, 0, 0)
            if not(msg):
                break
            win32gui.TranslateMessage(msg)
            win32gui.DispatchMessage(msg)

    def stop(self, hwnd):
        """
        @param hwnd 終了メッセージの送信先ウィンドウハンドル
        """
        self._can_running = False

        # PostQuitMessage だと他スレッドからの実行時に終了できない.
        # そのため, あえて hwnd を明示的に指定できる PostMessage を使用.
        #win32api.PostQuitMessage(0)
        win32api.PostMessage(
            hwnd,
            win32con.WM_QUIT
        )

def _incrementer():
    """
    MainWindow 用のインクリメントカウンタ.
    本当はカプセル化したかったが, インクリメントカウンタは
    グローバルスコープに置かないと動かないため仕方なくここに配置.
    """
    _incrementer.count += 1
    return _incrementer.count
_incrementer.count = 0

class Hwnd:
    """
    ウィンドウハンドルを格納したシングルトンクラス.
    利用者はこれを使ってウィンドウハンドルを取得する.

    set するのは MainWindow のみ.
    setter を作っちゃうと利用者側から見えちゃうため,
    set する際は直接メンバ変数をいじるようにする.
    """
    def __init__(self):
        self._hwnd = None

    def get(self):
        return self._hwnd
# シングルトンインスタンス
hwndinst = Hwnd()

class MainWindow:
    """
    非表示ウィンドウ + トレイアイコンを作成する.
    @note 終了時は destroy を呼びださなければならない.
    """

    # ユーザ定義メッセージ.
    # WM_APP から 1 ずつ増やして定義.
    WM_BASE = win32con.WM_APP
    WM_TRAYICON_EVENT = WM_BASE + _incrementer()

    def __init__(self, classname="window", tooltip=""):
        """
        @param classname ウィンドウクラス名
        """
        self._can_destroy = True

        self._hwnd = None
        self._classname = classname
        self._classatom = None
        self._hinst = None

        self._trayicon = None
        self._tooltip = tooltip

        self._mainloop = MainLoop()

        self._callback_on_destroy = None
        self._callback_on_hotkey = None
        self._callback_on_left_click = None
        self._callback_on_right_click = None
        self._callback_on_middle_click = None

        self._message_map = {
            win32con.WM_DESTROY          : self._on_destroy,
            MainWindow.WM_TRAYICON_EVENT : self._on_tray,
            win32con.WM_HOTKEY           : self._on_hotkey,
        }

    def __enter__(self):
        return self

    def __exit__(self, type, value, trackback):
        self.destroy()

    def set_callback_on_destroy(self, callback):
        """
        ウィンドウ破棄時に実行するコールバック関数を登録する.
        """
        self._callback_on_destroy = callback

    def set_callback_on_hotkey(self, callback):
        self._callback_on_hotkey = callback

    def set_callback_on_left_click(self, callback):
        self._callback_on_left_click = callback

    def set_callback_on_right_click(self, callback):
        self._callback_on_right_click = callback

    def set_callback_on_middle_click(self, callback):
        self._callback_on_middle_click = callback

    def create(self):
        """
        ウィンドウを作成する.
        """
        if self._hwnd:
            return self._hwnd

        # ウィンドウクラスを登録
        wc = win32gui.WNDCLASS()
        self._hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = self._classname
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = self._message_map
        self._classatom = win32gui.RegisterClass(wc)

        # ウィンドウを生成
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        windowpos = (0, 0)
        windowsize = (1, 1)
        self._hwnd = win32gui.CreateWindow(
            self._classatom,
            self._classname,
            style,
            windowpos[0],
            windowpos[1],
            windowsize[0],
            windowsize[1],
            0,
            0,
            self._hinst,
            None,
        )
        hwndinst._hwnd = self._hwnd # 利用者参照先にも入れる.

        win32gui.UpdateWindow(self._hwnd)

        # ウィンドウはウィンドウメッセージを扱うために作ったものなので
        # 利用者には見せない
        win32gui.ShowWindow(self._hwnd, win32con.SW_HIDE)

        self._trayicon = trayicon.TrayIcon(
            self._hwnd,
            MainWindow.WM_TRAYICON_EVENT,
            self._tooltip
        )

    def start(self):
        """
        GUIループに入る.
        先に craate() でウィンドウを生成しておく必要がある.
        @exception RuntimeError ウィンドウが未だ生成されていない
        """
        if not(self._hwnd):
            raise RuntimeError("Main window is not created.")

        self._mainloop.start() # blocking.

    def stop(self):
        """
        GUI ループから抜ける.
        @note ウィンドウを作成したスレッドと別のスレッドから呼び出してもよい.
        """
        self._mainloop.stop(self._hwnd)

    def destroy(self):
        """
        GUIの破棄と, 破棄時コールバックの実行.
        @note ウィンドウを作成したスレッドと同じスレッドから呼び出すこと.
        """
        if not(self._can_destroy):
            return
        self._can_destroy = False

        self.stop()

        if callable(self._callback_on_destroy):
            self._callback_on_destroy()

        try:
            self._trayicon.destroy()
        except Exception as e:
            # 他の終了処理もあるのでとりあえず続行.
            pass

        try:
            win32gui.DestroyWindow(self._hwnd)
        except Exception as e:
            # 他の終了処理もあるのでとりあえず続行.
            pass

        try:
            win32gui.UnregisterClass(self._classatom, self._hinst)
        except Exception as e:
            # 他の終了処理もあるのでとりあえず続行.
            pass

    def _on_hotkey(self, hwnd, message, wparam, lparam):
        if callable(self._callback_on_hotkey):
            self._callback_on_hotkey(hwnd, message, wparam, lparam)

    def _on_destroy(self, hwnd, message, wparam, lparam):
        self.destroy()

    def _on_tray(self, hwnd, message, wparam, lparam):
        """
        @param wparam マウスイベントが発生したタスクバーアイコンのID
        @param lparam 発生したイベントに関連するメッセージコード
        """
        if lparam==win32con.WM_RBUTTONUP:
            if callable(self._callback_on_right_click):
                self._callback_on_right_click()
        elif lparam==win32con.WM_LBUTTONUP:
            if callable(self._callback_on_left_click):
                self._callback_on_left_click()
        elif lparam==win32con.WM_MBUTTONUP:
            if callable(self._callback_on_middle_click):
                self._callback_on_middle_click()


if __name__ == '__main__':
    """
    簡単な動作確認.
    ウィンドウを作って 3 秒後に終了する.
    """
    import threading
    import time

    def stopthreadbody(mainwindowinst):
        time.sleep(3)
        mainwindowinst.stop()

    with MainWindow(classname="hogewndclass") as mainwindow:
        stopthread = threading.Thread(
            None,
            stopthreadbody,
            "thread name",
            (mainwindow,),
            {},
        )
        stopthread.start()

        mainwindow.create()
        mainwindow.stop()

        stopthread.join()

