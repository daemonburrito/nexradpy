import os

import unittest

TESTS_ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
FIXTURES_PATH = os.path.join(TESTS_ROOT_PATH, 'fixtures')


def get_fixture_path(filename):
    return os.path.join(FIXTURES_PATH, filename)



class NexradPyTest(unittest.TestCase):
    """Base test with convenience attributes."""
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass
