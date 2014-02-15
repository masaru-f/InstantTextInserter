# encoding: shift-jis

import os

import util.executer as executer

import commander_interface

import dialog_wrapper
import endhandler
import reloader
import selfinfo

CMD_OPEN_DIRECTORY = "dir"
CMD_SHOW_VERSION   = "version"
CMD_QUIT           = "quit"
CMD_RELOAD         = "reload"
CMD_OPEN_SNIPPET_DIRECTORY = "snippet_directory"

class StartingPointCommander(commander_interface.ICommander):
    """
    CoR チェインの始点として使うコマンダ.
    """
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        return False

    def _interpret(self, command):
        pass

class OpenDirectoryCommander(commander_interface.ICommander):
    """
    インストールフォルダを開く.
    """
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command==CMD_OPEN_DIRECTORY:
            return True
        return False

    def _interpret(self, command=None):
        _executer = executer.Executer()
        _executer.execute([selfinfo.PROGRAM_DIRECTORY])

class VersionCommander(commander_interface.ICommander):
    """
    バージョン情報を表示する.
    """
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command==CMD_SHOW_VERSION:
            return True
        return False

    def _interpret(self, command=None):
        dialog_wrapper.ok(selfinfo.PROGRAM_INFO, "バージョン情報")

class ExitCommander(commander_interface.ICommander):
    """
    プログラムを終了する.
    """
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command==CMD_QUIT:
            return True
        return False

    def _interpret(self, command=None):
        endhandler.inst.run()

class ReloadCommander(commander_interface.ICommander):
    """
    設定を再読込する.
    """
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command==CMD_RELOAD:
            return True
        return False

    def _interpret(self, command=None):
        reloader.inst.reload()

class OpenSnippetDirectoryCommander(commander_interface.ICommander):
    """
    スニペットフォルダを開く.
    """
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command==CMD_OPEN_SNIPPET_DIRECTORY:
            return True
        return False

    def _interpret(self, command=None):
        _executer = executer.Executer()
        _executer.execute([selfinfo.SNIPPETFOLDER_FULLPATH])

if __name__ == '__main__':
    """
    簡単なテスト.
    """
    def dummy_exit():
        print "dummy_exit"

    endhandler.inst.set(dummy_exit)

    exitcmd = ExitCommander()
    opendir = OpenDirectoryCommander(exitcmd)
    ver = VersionCommander(opendir)
    reloadcmd = ReloadCommander(ver)
    opensnidir = OpenSnippetDirectoryCommander(reloadcmd)
    sp = StartingPointCommander(opensnidir)

    #sp.run(CMD_OPEN_DIRECTORY)
    #sp.run(CMD_SHOW_VERSION)
    #sp.run(CMD_RELOAD)
    #sp.run(CMD_OPEN_SNIPPET_DIRECTORY)
    #sp.run(CMD_QUIT)
