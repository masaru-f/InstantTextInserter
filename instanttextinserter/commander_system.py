# encoding: shift-jis

import os

import util.executer as executer

import commander_interface

import dialog_wrapper
import endhandler
import selfinfo
import snippet_loader

CMD_OPEN_DIRECTORY = "dir"
CMD_SHOW_VERSION   = "version"
CMD_QUIT           = "quit"
CMD_RELOAD_SNIPPET = "reload_snippet"
CMD_OPEN_SNIPPET_DIRECTORY = "snippet_directory"

class StartingPointCommander(commander_interface.ICommander):
    """
    CoR �`�F�C���̎n�_�Ƃ��Ďg���R�}���_.
    """
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        return False

    def _interpret(self, command):
        pass

class OpenDirectoryCommander(commander_interface.ICommander):
    """
    �C���X�g�[���t�H���_���J��.
    """
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command==CMD_OPEN_DIRECTORY:
            return True
        return False

    def _interpret(self, command):
        _executer = executer.Executer()
        _executer.execute([selfinfo.PROGRAM_DIRECTORY])

class VersionCommander(commander_interface.ICommander):
    """
    �o�[�W��������\������.
    """
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command==CMD_SHOW_VERSION:
            return True
        return False

    def _interpret(self, command):
        dialog_wrapper.ok(selfinfo.PROGRAM_INFO, "�o�[�W�������")

class ExitCommander(commander_interface.ICommander):
    """
    �v���O�������I������.
    """
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command==CMD_QUIT:
            return True
        return False

    def _interpret(self, command):
        endhandler.inst.run()

class ReloadSnippetCommander(commander_interface.ICommander):
    """
    �X�j�y�b�g�f�[�^���ēǍ�����.
    """
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command==CMD_RELOAD_SNIPPET:
            return True
        return False

    def _interpret(self, command):
        snippet_loader.inst.reload()

class OpenSnippetDirectoryCommander(commander_interface.ICommander):
    """
    �C���X�g�[���t�H���_���J��.
    """
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command==CMD_OPEN_SNIPPET_DIRECTORY:
            return True
        return False

    def _interpret(self, command):
        _executer = executer.Executer()
        _executer.execute([selfinfo.SNIPPETFOLDER_FULLPATH])

if __name__ == '__main__':
    """
    �ȒP�ȃe�X�g.
    """
    def dummy_exit():
        print "dummy_exit"

    endhandler.inst.set(dummy_exit)

    exitcmd = ExitCommander()
    opendir = OpenDirectoryCommander(exitcmd)
    ver = VersionCommander(opendir)
    reloadsnippet = ReloadSnippetCommander(ver)
    opensnidir = OpenSnippetDirectoryCommander(reloadsnippet)
    sp = StartingPointCommander(opensnidir)

    #sp.run(CMD_OPEN_DIRECTORY)
    #sp.run(CMD_SHOW_VERSION)
    #sp.run(CMD_RELOAD_SNIPPET)
    #sp.run(CMD_OPEN_SNIPPET_DIRECTORY)
    #sp.run(CMD_QUIT)
