# encoding: shift-jis

import win32api

import util.log as log
import util.exceptions as exceptions

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
        creator.append("&Reload", commander_system.CMD_RELOAD)
        creator.append(
            "Open &Snippet Folder",
            commander_system.CMD_OPEN_SNIPPET_DIRECTORY
        )
        creator.append(
            "Open &Hotkey Config File",
            commander_system.CMD_OPEN_HOTKEY_CONFIG
        )
        creator.append_separator()
        creator.append("Open &Install Directory",
                       commander_system.CMD_OPEN_DIRECTORY)
        creator.append("&Version", commander_system.CMD_SHOW_VERSION)
        creator.append("&Quit", commander_system.CMD_QUIT)

        menudata = None
        try:
            menudata = creator.get_menudata()
        except ValueError as e:
            creator.destroy() # @todo with 使って RAII したい
            exceptions.ProgrammersMistake(str(e))

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
    pass
