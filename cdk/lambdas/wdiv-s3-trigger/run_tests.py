#!/usr/bin/env python

import os
import sys
import unittest

if __name__ == "__main__":
    dirname = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()
    tests = loader.discover(os.path.abspath(os.path.join(dirname, "tests")))
    runner = unittest.runner.TextTestRunner()
    result = runner.run(tests)
    sys.exit(not result.wasSuccessful())
