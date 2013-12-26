import unittest

import nexradpy

import tests

class DecoderTest(tests.NexradPyTest):
    """Tests for the decoder module."""
    def setUp(self):
        self.p94 = tests.get_fixture_path('p94r0-kewx.bin')
        self.p94_class_str = 'nexradpy.decoders.p94.p94'

    def test_load_file(self):
        """Test that the module can load a specified file."""
        decoder = nexradpy.decoder.load_file(self.p94)

        self.assertEqual(self.p94_class_str, str(decoder.__class__),
                msg='Decoder'
                ' type not returned: {0}.'.format(decoder.__class__))

    def test_decode(self):
        """Test that the decode method returns a valid product."""
        decoder = nexradpy.decoder.load_file(self.p94)
        product = decoder.decode()

        self.assertEqual(product['message_header']['message_code'], 94,
                msg='Unexpected product message_code.')
