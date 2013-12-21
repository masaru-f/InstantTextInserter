# encoding: shift-jis

import commander_system

class CommanderChain:
    """
    コマンダの CoR 生成と実行の口を与える.
    """
    def __init__(self):
        """
        チェイン生成方針.
        - 始点コマンダが最初.
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
