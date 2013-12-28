# encoding: shift-jis

import sys

import util.terminator_stack as terminator_stack
import util.log as log

import util_win.trayicongui as trayicongui

import doublelaunch_checker
import endhandler
import menu
import selfinfo
import thread_trigger

# デフォルトエンコーディングの設定
# 通常 sys.setdefaultencoding は存在しない(sitecustomizeで設定する)が,
# py2exe で生成した実行ファイル経由だと
#  - sitecustomize が効かない
#  - sys.setdefaultencoding が存在する
# ので, ここで設定してやる必要がある.
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
            menuinst = menu.Menu()
            triggerwatcher = thread_trigger.TriggerThread()
            #hotkeywatcher = KeyWatcher()

            gui.set_callback_on_right_click(menuinst.run)
            # @note 即終了するのはとりあえず. リロードあたりに変えたいかな.
            gui.set_callback_on_left_click(gui.destroy)

            termstack.push(gui.destroy)
            endhandler.inst.set(gui.destroy)

            termstack.push(triggerwatcher.stop)
            triggerwatcher.start()
            #termstack.push(hotkeywatcher.stop)
            #hotkeywatcher.start()

            gui.create_and_start()

if __name__ == '__main__':
    doublelaunch_checker.check_and_dispose()

    log.info("start entrypoint.")
    entrypoint = EntryPoint()
    log.info("end entrypoint.")
