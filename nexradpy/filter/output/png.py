import math
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
    bb = None

    # ImageDraw instance
    draw = None

    def __init__(self):
        self.im = Image.open()
        self.draw = ImageDraw(self.im)

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

    def _levels(self, value):
        """Return a RGB tuple based on value."""
        return value

    def _draw_radial(self, angle_tuple_deg, bins):
        """Draws a radial. First value of angle tuple is start angle, second
        value is angle delta."""
        start_angle = 0
        end_angle = 0

        start_angle = math.radians(angle_tuple_deg[0])
        end_angle = math.radians(angle_tuple_deg[0] + angle_tuple_deg[1])

        last_coord = self.center
        for bn in bins:
            # first bin
            if n == 0:
                points = [self.center]
                points[1] = self.center[0] + (n + 1) * Math.cos(start_angle),
                    self.center[1] + (n + 1) * Math.sin(start_angle)
                points[2] = self.center[0] + (n + 1) * Math.cos(end_angle),
                    self.center[1] + (n + 1) * Math.sin(end_angle)

                self.draw.polygon(points, fill=_levels(bn))
