import unittest

import nexradpy


class NexradPyTest(unittest.TestCase):
    """Base test with convenience attributes."""
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

class DecoderTest(NexradPyTest):
    """Tests for the decoder module."""
    def setUp(self):
        import tests
        self.p94 = tests.get_fixture_path('p94r0-kewx.bin')

    def test_load_file(self):
        """Test that the module can load a specified file."""
        nexradpy.decoder.load_file(self.p94)
