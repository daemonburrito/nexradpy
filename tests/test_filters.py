import unittest

import nexradpy.decoder
import nexradpy.filter.output.png

import tests


class FiltersTest(tests.NexradPyTest):
    """Tests for filter modules."""
    pass


class PNGFilterTest(FiltersTest):
    """Test the PNG output filter."""
    def setUp(self):
        self.p94 = tests.get_fixture_path('p94r0-kewx.bin')
        self.decoder = nexradpy.decoder.load_file(self.p94)
        self.product = self.decoder.decode()

    def test_filter(self):
        im = nexradpy.filter.output.png.PNG().filter(self.product)
        im.save(tests.get_fixture_path('p94-test.png'))
