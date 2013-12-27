# encoding: shift-jis

import unittest

from test_commander_interface import *
from test_macro import *
from test_snippet_observer import *
from test_snippet_loader import *
from test_snippet_paster import *

suites = [\
unittest.TestLoader().loadTestsFromTestCase(ICommanderTest), \
unittest.TestLoader().loadTestsFromTestCase(MacroTest), \
unittest.TestLoader().loadTestsFromTestCase(SnippetObserverTest), \
unittest.TestLoader().loadTestsFromTestCase(SnippetLoadertTest), \
unittest.TestLoader().loadTestsFromTestCase(SnippetPasterTest), \
]

testsuites = unittest.TestSuite(suites)

runner = unittest.TextTestRunner()
runner.run(testsuites)