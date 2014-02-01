# encoding: shift-jis

import sys

import util.terminator_stack as terminator_stack
import util.log as log

import util_win.trayicongui as trayicongui

import doublelaunch_checker
import endhandler
import menu
import selfinfo
import snippet_loader
import thread_trigger

import hotkey_loader

# �f�t�H���g�G���R�[�f�B���O�̐ݒ�
# �ʏ� sys.setdefaultencoding �͑��݂��Ȃ�(sitecustomize�Őݒ肷��)��,
# py2exe �Ő����������s�t�@�C���o�R����
#  - sitecustomize �������Ȃ�
#  - sys.setdefaultencoding �����݂���
# �̂�, �����Őݒ肵�Ă��K�v������.
if hasattr(sys, 'setdefaultencoding'):
    import locale
    lang, enc = locale.getdefaultlocale()
    sys.setdefaultencoding(enc or 'shift-jis')
    del sys.setdefaultencoding

class EntryPoint:
    def __init__(self):
        with terminator_stack.TerminatorStack() as termstack:
            gui = trayicongui.MainWindow(
                selfinfo.WINDOWCLASSNAME,
                selfinfo.TRAYICON_TOOLTIP
            )
            gui.create()

            menuinst = menu.Menu()
            triggerwatcher = thread_trigger.TriggerThread()
            hotkeyloaderinst = hotkey_loader.HotkeyLoader(
                trayicongui.hwndinst.get()
            )

            gui.set_callback_on_right_click(menuinst.run)
            gui.set_callback_on_left_click(snippet_loader.inst.reload)
            gui.set_callback_on_hotkey(hotkeyloaderinst.get_hotkey_callback())

            termstack.push(gui.destroy)
            endhandler.inst.set(gui.destroy)

            termstack.push(triggerwatcher.stop)
            triggerwatcher.start()

            termstack.push(hotkeyloaderinst.unregister_hotkey)
            hotkeyloaderinst.register_hotkey()

            gui.start()

if __name__ == '__main__':
    doublelaunch_checker.check_and_dispose()

    log.info("start entrypoint.")
    entrypoint = EntryPoint()
    log.info("end entrypoint.")
