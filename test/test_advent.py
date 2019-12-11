#!/usr/local/bin/python3

import unittest
import doctest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

files = []
root_dir = 'advent'

for root, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename[-3:] != '.py':
            continue
        f = os.path.join(root, filename)
        f = f.replace('/', '.')
        f = f[:-3]
        files.append(f)

suite = unittest.TestSuite()
for module in files:
    suite.addTest(doctest.DocTestSuite(module))
unittest.TextTestRunner(verbosity=1).run(suite)