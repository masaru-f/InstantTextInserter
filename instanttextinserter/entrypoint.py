# encoding: shift-jis

import sys

import util.terminator_stack as terminator_stack
import util.log as log

import util_win.trayicongui as trayicongui

import doublelaunch_checker
import endhandler
import menu
import reloader
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
            # gui �̍쐬
            gui = trayicongui.MainWindow(
                selfinfo.WINDOWCLASSNAME,
                selfinfo.TRAYICON_TOOLTIP
            )
            gui.create()

            # ��v�C���X�^���X�̍쐬
            menuinst = menu.Menu()
            triggerwatcher = thread_trigger.TriggerThread()
            hotkeyloaderinst = hotkey_loader.HotkeyLoader(
                trayicongui.hwndinst.get()
            )
            reloader.inst.push(snippet_loader.inst)
            reloader.inst.push(hotkeyloaderinst)

            # gui �̃C�x���g�n���h���ւ̓o�^
            gui.set_callback_on_right_click(menuinst.run)
            gui.set_callback_on_left_click(reloader.inst.reload)
            gui.set_callback_on_hotkey(hotkeyloaderinst.get_hotkey_callback())

            # �I������ gui ��j�����邽�߂̏���
            termstack.push(gui.destroy)
            endhandler.inst.set(gui.destroy)

            # ��v�C���X�^���X�̊J�n.
            # �I�����ɉ�����s�킹�邽�� TerminatorStack ���g�p.
            termstack.push(triggerwatcher.stop)
            triggerwatcher.start()
            termstack.push(hotkeyloaderinst.unregister_hotkeys)
            hotkeyloaderinst.load_and_register_hotkeys()

            # gui �̊J�n.
            # gui ���[�v�ɓ���.
            log.info("start mainloop.")
            gui.start()
            log.info("end mainloop.")

if __name__ == '__main__':
    doublelaunch_checker.check_and_dispose()

    log.info("start entrypoint.")
    entrypoint = EntryPoint()
    log.info("end entrypoint.")
