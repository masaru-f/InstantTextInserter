# encoding: shift-jis

import ctypes
import win32api
import win32con
import win32file
import win32gui
import win32process

def GetForegroundWindow():
    """
    Windows API に則った GetForegroundWindow.
    """
    return ctypes.windll.user32.GetForegroundWindow()

def WindowFromPoint():
    """
    マウスカーソル位置にあるウィンドウのハンドルを取得.
    取得するのは親ウィンドウであることに注意.
    """
    mx, my = win32api.GetCursorPos()
    return ctypes.windll.user32.GetAncestor(
        win32gui.WindowFromPoint((mx, my)),
        win32con.GA_ROOT
    )

def ActivateWindow(hwnd):
    """
    指定ウィンドウをアクティブにする.
    """
    foreground_threadid, processid = \
        win32process.GetWindowThreadProcessId(
            GetForegroundWindow()
        )
    current_threadid = win32api.GetCurrentThreadId()

    # foreground なスレッドにアタッチする
    if foreground_threadid != current_threadid:
        try:
            # @note たまに error:87 が起きるので吸収.
            # @todo error:87 の原因調査
            win32process.AttachThreadInput(
                current_threadid,
                foreground_threadid,
                True
            )
        except:
            pass

    try:
        # ウィンドウハンドルが無効だとエラーになる(code:1400)ので
        # ここで吸収.
        win32gui.SetForegroundWindow(hwnd)
    except:
        pass

    # アタッチしていればデタッチする..
    if foreground_threadid != current_threadid:
        try:
            win32process.AttachThreadInput(
                current_threadid,
                foreground_threadid,
                False
            )
        except:
            pass

def GetProcessImageFileName(hprocess, max_path):
    """
    64bitアプリに対応した, プロセスのファイルパス取得.
    プロセスのイメージ名を取得し,
    イメージ名に含まれるデバイス名をドライブレターに置換している.
    """

    # device name > drive letter 変換テーブルの作成
    # 1. drive letter list
    ldstrings = win32api.GetLogicalDriveStrings().split("\\0")[0]
    drivelist = [elm.strip("\\") for elm in ldstrings.split("\0")]
    drivelist.remove("")
    # 2. device name list
    devicelist = [
        win32file.QueryDosDevice(elm).split("\0\0")[0]
        for elm in drivelist
    ]
    # 3. convertion table
    device2driveletter = {}
    for i in range(len(drivelist)):
        device2driveletter[devicelist[i]] = drivelist[i]

    imagefilename = (ctypes.c_char*Windowproperty.MAX_PATH)()
    len_imagefilename = ctypes.windll.psapi.GetProcessImageFileNameA(
        hprocess,
        imagefilename,
        max_path
    )

    # 取得失敗. イメージ名が空か, 取得処理に失敗した.
    if len_imagefilename==0:
        return ""

    # イメージ名に対して各デバイス名で replace を試みる.
    # replace できた = 対応するドライブレターに置換された.
    beforestr = imagefilename.value
    for i in range(len(drivelist)):
        devicename = devicelist[i]
        afterstr = beforestr.replace(
            devicename,
            device2driveletter[devicename]
        )
        if beforestr!=afterstr:
            return afterstr

    # 取得失敗. 対応するドライブレターが見つからなかった.
    return ""

class Windowproperty:
    """
    指定ウィンドウの諸情報を取得する.
    取得失敗は吸収する(空の値を返すようにする).
    ただし API が元々吸収してくれる場合は吸収処理は入れてない.
    """

    # 値は適当. これくらいあればまあ足りるでしょ, という程度.
    MAX_PATH = 2048

    def __init__(self, hwnd):
        self.hwnd = hwnd
        return

    def get_caption(self):
        return win32gui.GetWindowText(self.hwnd)

    def get_classname(self):
        try:
            return win32gui.GetClassName(self.hwnd)
        except Exception as e:
            pass
        return ""

    def get_hwnd(self):
        return self.hwnd

    def get_path(self):
        threadid, processid = \
            win32process.GetWindowThreadProcessId(self.hwnd)
        processhandle = win32api.OpenProcess(\
            win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, \
            0, \
            processid
        )
        if processhandle==0:
            return ""

        ret = ""
        try:
            # @note 戻り値が unicode string であることに注意
            ret = win32process.GetModuleFileNameEx(processhandle, 0)
        except:
            # 64bitアプリだと成功しないので
            # GetProcessImageFileName を試す.
            return GetProcessImageFileName(
                processhandle.__int__(),
                Windowproperty.MAX_PATH
            )

        processhandle.close()
        return ret

    def get_windowpos(self):
        try:
            left, top, right, bottom = win32gui.GetWindowRect(
                self.hwnd
            )
            return [left, top]
        except Exception as e:
            pass
        return [0, 0]

    def get_windowsize(self):
        try:
            left, top, right, bottom = win32gui.GetWindowRect(
                self.hwnd
            )
            return [right-left, bottom-top]
        except Exception as e:
            pass
        return [0, 0]

if __name__ == '__main__':
    from time import sleep

    ActivateWindow(0)

    sleep(2)
    print "=== frompoint ==="
    wp_frompoint = Windowproperty(WindowFromPoint())
    print wp_frompoint.get_caption()
    print wp_frompoint.get_classname()
    print wp_frompoint.get_hwnd()
    print wp_frompoint.get_path()
    print "=== foreground ==="
    wp = Windowproperty(GetForegroundWindow())
    print wp.get_caption()
    print wp.get_classname()
    print wp.get_hwnd()
    print wp.get_path()
    s = wp.get_path()
    print isinstance(s, str)
    print isinstance(s, unicode)