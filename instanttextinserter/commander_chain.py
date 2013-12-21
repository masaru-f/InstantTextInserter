# encoding: shift-jis

import commander_system

class CommanderChain:
    """
    �R�}���_�� CoR �����Ǝ��s�̌���^����.
    """
    def __init__(self):
        """
        �`�F�C���������j.
        - �n�_�R�}���_���ŏ�.
        """
        self.commander = commander_system.StartingPointCommander(
            commander_system.OpenDirectoryCommander(
            commander_system.VersionCommander(
            commander_system.ExitCommander(
            commander_system.ReloadSnippetCommander(
            )
            )
            )
            )
        )

    def run(self, command):
        self.commander.run(command)

if __name__ == '__main__':
    pass
