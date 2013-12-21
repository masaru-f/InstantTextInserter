# encoding: shift-jis

import unittest

from test_filereader import *
from test_lockguard import *
from test_log import *
from test_stack import *
from test_terminator_stack import *

suites = [\
unittest.TestLoader().loadTestsFromTestCase(FileReaderTest), \
unittest.TestLoader().loadTestsFromTestCase(LockGuardTest), \
unittest.TestLoader().loadTestsFromTestCase(LogTest), \
unittest.TestLoader().loadTestsFromTestCase(StackTest), \
unittest.TestLoader().loadTestsFromTestCase(TerminatorStackTest), \
]

testsuites = unittest.TestSuite(suites)

runner = unittest.TextTestRunner()
runner.run(testsuites)