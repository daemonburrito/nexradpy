from . import OutputFilter, NexradpyError
import numpy
try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image, ImageDraw

class PNG(OutputFilter):
    """Outputs a PNG from a decoded product."""
    p = None
    radial_matrix = None

    output_dimensions = None

    def _create_radial_matrix(self):
        """From a Product, create a Numpy matrix from radials."""
        pass

    def _radial_to_bitmap(self):
        pass

    def filter(self, p):
        """Takes a product and returns a PNG."""
        self.p = p

        l = []
        try:
            for radial in p['symbology']['layers'][0]['data']['radials']:
                l.append(radial['levels'])

            self.radial_matrix = numpy.matrix(l)

        except Exception as ex:
            raise NexradpyError(ex)

        # for simplicity, make the diameter no_of_bins * 2
        r = p['symbology']['layers'][0]['data']['number_bins']
        d =  r * 2
        self.output_dimensions = (d, d)
        self.center = (r, r)

    def _draw_radial(self, start_angle, delta_angle, levels):
        pass
