# encoding: shift-jis

import util_win.dialog as dialog
import util_win.trayicongui as trayicongui
import util_win.windowutil as windowutil

import selfinfo

def ok(message, title=None):
    if title==None:
        title=selfinfo.PROGRAM_NAME

    # ���E�B���h�E���A�N�e�B�u�ɂ���.
    # ���̃E�B���h�E�ɖ�����ă_�C�A���O���B���̂�h������.
    windowutil.ActivateWindow(trayicongui.hwndinst.get())

    dialog.ok(message, title)
