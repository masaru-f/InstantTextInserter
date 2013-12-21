# encoding: shift-jis

import sys

import util.terminator_stack as terminator_stack
import util.log as log

import util_win.trayicongui as trayicongui

import endhandler
import menu
import thread_trigger

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
            gui = trayicongui.MainWindow()
            menuinst = menu.Menu()
            triggerwatcher = thread_trigger.TriggerThread()
            #hotkeywatcher = KeyWatcher()

            gui.set_callback_on_right_click(menuinst.run)
            gui.set_callback_on_left_click(gui.destroy)

            termstack.push(gui.destroy)
            endhandler.inst.set(gui.destroy)

            termstack.push(triggerwatcher.stop)
            triggerwatcher.start()
            #termstack.push(hotkeywatcher.stop)
            #hotkeywatcher.start()

            gui.create_and_start()

if __name__ == '__main__':
    # ��d�N���`�F�b�N
    # ���s�t�@�C���ɂ���Ɖ��̂���ɓ�d�N���Ƃ݂Ȃ���Ă��܂�����
    # �R�����g�A�E�g��
    #@todo ��ɓ�d�N���Ƃ݂Ȃ���錴���𒲍�
    #doublelaunch_checker.check_and_dispose()

    log.info("start entrypoint.")
    entrypoint = EntryPoint()
    log.info("end entrypoint.")
