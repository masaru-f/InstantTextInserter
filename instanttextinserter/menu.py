# encoding: shift-jis

import win32api

import util.log as log

import util_win.popupmenu as popupmenu
import util_win.trayicongui as trayicongui

import commander_chain
import commander_system

class Menu:
    """
    プログラム独自のポップアップメニューの作成と表示.
    """
    def __init__(self):
        self._commanderchain = commander_chain.CommanderChain()

    def run(self):
        """
        トレイアイコン上にメニューを表示する.
        """
        creator = popupmenu.Creator()
        creator.append("Reload", commander_system.CMD_RELOAD)
        creator.append(
            "Open snippet folder",
            commander_system.CMD_OPEN_SNIPPET_DIRECTORY
        )
        #creator.append("Open snippet [hoge]", "currentsnippet")
        creator.append_separator()
        creator.append("Open InstallDir", commander_system.CMD_OPEN_DIRECTORY)
        creator.append("Version", commander_system.CMD_SHOW_VERSION)
        creator.append("Quit", commander_system.CMD_QUIT)

        menudata = None
        try:
            menudata = creator.get_menudata()
        except ValueError as e:
            log.critical("Programmer's mistake. " + str(e))
            creator.destroy() # @todo with 使って RAII したい
            return

        tracker = popupmenu.Tracker(trayicongui.hwndinst.get())
        command = None
        mouseposx, mouseposy = win32api.GetCursorPos()
        try:
            command = tracker.track(menudata, mouseposx, mouseposy)
            log.debug("tracked command:" + str(command))
        except popupmenu.MenuTrackError as e:
            log.debug(str(e))

        creator.destroy()

        self._commanderchain.run(command)

if __name__ == '__main__':
    """
    簡単に動作確認.
    """
    def on_rightclick():
        menu = Menu()
        menu.run()

    with trayicongui.MainWindow(classname="hogewndclass") as mainwindow:
        def on_leftclick():
            mainwindow.stop()

        mainwindow.set_callback_on_left_click(on_leftclick)
        mainwindow.set_callback_on_right_click(on_rightclick)
        mainwindow.create_and_start()