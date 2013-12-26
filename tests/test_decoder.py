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
        self.p94_class_str = 'nexradpy.decoders.p94.p94'

    def test_load_file(self):
        """Test that the module can load a specified file."""
        decoder = nexradpy.decoder.load_file(self.p94)

        self.assertEqual(self.p94_class_str, str(decoder.__class__),
                msg='Decoder'
                ' type not returned: {0}.'.format(decoder.__class__))
