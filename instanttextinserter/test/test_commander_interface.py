# encoding: shift-jis

import unittest

import commander_interface

class HogeCommander(commander_interface.ICommander):
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command=="hoge":
            return True
        return False

    def _interpret(self, command):
        print "i am hoge.",
        print command

class FugaCommander(commander_interface.ICommander):
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command=="fuga":
            return True
        return False

    def _interpret(self, command):
        print "i am fuga.",
        print command

class PiyoCommander(commander_interface.ICommander):
    def __init__(self, next_commander=None):
        commander_interface.ICommander.__init__(self, next_commander)

    def _can_interpret(self, command):
        if command=="piyo":
            return True
        return False

    def _interpret(self, command):
        print "i am piyo.",
        print command

class EndPointCommander(commander_interface.ICommander):
    def __init__(self):
        commander_interface.ICommander.__init__(self)

    def _can_interpret(self, command):
        return True

    def _interpret(self, command):
        print "your command was not interpreted by each commander."

class ICommanderTest(unittest.TestCase):
    """
    意図したコマンダが実行されていることを目視で確認するテスト.
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1chain(self):
        print "==== 1 chain test ===="
        hoge = HogeCommander()
        hoge.run("fuga")
        hoge.run("hoge")

    def test_chain(self):
        print "==== chain test ===="
        endpoint = EndPointCommander()
        piyo = PiyoCommander(endpoint)
        fuga = FugaCommander(piyo)
        hoge = HogeCommander(fuga)

        hoge.run("hoge")
        hoge.run("fuga")
        hoge.run("piyo")
        hoge.run("")
        hoge.run("don")
        hoge.run("ちゃちゃちゃ")


if __name__ == "__main__":
    unittest.main()
