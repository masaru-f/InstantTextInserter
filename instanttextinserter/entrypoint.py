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
            # gui の作成
            gui = trayicongui.MainWindow(
                selfinfo.WINDOWCLASSNAME,
                selfinfo.TRAYICON_TOOLTIP
            )
            gui.create()

            # 主要インスタンスの作成
            menuinst = menu.Menu()
            triggerwatcher = thread_trigger.TriggerThread()
            hotkeyloaderinst = hotkey_loader.HotkeyLoader(
                trayicongui.hwndinst.get()
            )
            reloader.inst.push(snippet_loader.inst)
            reloader.inst.push(hotkeyloaderinst)

            # gui のイベントハンドラへの登録
            gui.set_callback_on_right_click(menuinst.run)
            gui.set_callback_on_left_click(reloader.inst.reload)
            gui.set_callback_on_hotkey(hotkeyloaderinst.get_hotkey_callback())

            # 終了時に gui を破棄するための準備
            termstack.push(gui.destroy)
            endhandler.inst.set(gui.destroy)

            # 主要インスタンスの開始.
            # 終了時に解放を行わせるため TerminatorStack を使用.
            termstack.push(triggerwatcher.stop)
            triggerwatcher.start()
            termstack.push(hotkeyloaderinst.unregister_hotkeys)
            hotkeyloaderinst.load_and_register_hotkeys()

            # gui の開始.
            # gui ループに入る.
            log.info("start mainloop.")
            gui.start()
            log.info("end mainloop.")

if __name__ == '__main__':
    doublelaunch_checker.check_and_dispose()

    log.info("start entrypoint.")
    entrypoint = EntryPoint()
    log.info("end entrypoint.")
