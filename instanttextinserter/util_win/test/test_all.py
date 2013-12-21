# encoding: shift-jis

import unittest

from test_clipboard import *
from test_multiplelaunch import *

suites = [\
unittest.TestLoader().loadTestsFromTestCase(ClipboardTest), \
unittest.TestLoader().loadTestsFromTestCase(MultipleLaunchTest), \
]

testsuites = unittest.TestSuite(suites)

runner = unittest.TextTestRunner()
runner.run(testsuites)