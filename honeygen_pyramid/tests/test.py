from __future__ import absolute_import, print_function, unicode_literals

import unittest

from pyramid import testing


class MyTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def tests_ju(self):
        self.assertEqual(1, 1)
