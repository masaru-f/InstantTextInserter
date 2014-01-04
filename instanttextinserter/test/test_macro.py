# encoding: shift-jis

import unittest

import macro

class MacroTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSystemMacro(self):
        sm = macro.SystemMacro()

        testdatalist = [
            ["equal", "="],
            ["=", "="],
        ]

        # 存在しないキーを渡すとエラー.
        try:
            sm.get("not_exist_key")
            self.assertTrue(False)
        except KeyError:
            pass
        except:
            self.assertTrue(False)

        print "==== system macro / embedded chars ===="
        for i in range(len(testdatalist)):
            elm = testdatalist[i]
            expect = elm[1]
            actual = sm.get(elm[0])
            print str(i) + "'s deployment test"
            self.assertEqual(expect, actual)

    def testMacro(self):
        m = macro.Macro()

        # とりあえず実装したかった, 行頭に = を書く分,
        if 1:
            testdata1 = "%=%======="
            testdata2 = "%equal%======="
            expect = "========"
            self.assertEqual(expect, m.deploy(testdata1))
            self.assertEqual(expect, m.deploy(testdata2))

        # 合致しないマクロは展開されない.
        if 1:
            testdata = "hoge%fuga%piyo"
            expect = testdata
            self.assertEqual(expect, m.deploy(testdata))

if __name__ == "__main__":
    unittest.main()
