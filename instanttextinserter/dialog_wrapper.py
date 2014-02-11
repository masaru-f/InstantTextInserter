# encoding: shift-jis

import util_win.dialog as dialog
import util_win.trayicongui as trayicongui
import util_win.windowutil as windowutil

import selfinfo

def ok(message, title=None):
    """
    title 省略時は PROGRAM_NAME を入れる.
    """
    if title==None:
        title=selfinfo.PROGRAM_NAME

    # 自ウィンドウをアクティブにする.
    # 他のウィンドウに埋もれてダイアログが隠れるのを防ぐため.
    windowutil.ActivateWindow(trayicongui.hwndinst.get())

    dialog.ok(message, title)
