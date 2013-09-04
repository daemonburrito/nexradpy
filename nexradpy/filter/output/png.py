import math
from . import OutputFilter, NexradpyError
import numpy
import math

try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image, ImageDraw

class PNG(OutputFilter):
    """Outputs a PNG from a decoded product."""
    p = None
    output_dimensions = None

    # ImageDraw instance
    draw = None

    # Image instance
    im = None

    def filter(self, p):
        """Takes a product and returns a PNG."""
        self.p = p

        # for simplicity, make the diameter no_of_bins * 2
        r = p['symbology']['layers'][0]['data']['number_bins']
        d =  r * 2
        self.output_dimensions = (d, d)
        self.center = (r, r)

        self.im = Image.new('RGBA', self.output_dimensions)
        self.draw = ImageDraw.Draw(self.im)

        for radial in p['symbology']['layers'][0]['data']['radials']:
            self._draw_radial((radial['start_angle'] / 10, radial['delta_angle'] / 10),
                    radial['levels'])

        return self.im

    def _levels(self, value):
        """Return a RGB tuple based on value."""
        if value == 0:
            return (0,0,0,0)
        else:
            return (value, value, value)

    def _draw_radial(self, angle_tuple_deg, bins):
        """Draws a radial. First value of angle tuple is start angle, second
        value is angle delta.
        x = r*cos(t) + h
        y = r*sin(t) + k
        """
        start_angle = math.radians(angle_tuple_deg[0])
        end_angle = math.radians(angle_tuple_deg[0] + angle_tuple_deg[1])

        point_a = ()
        point_b = ()
        r = 1
        for bn in bins:
            # first bin
            if r == 1:
                points = [self.center]

                points.append( (self.center[0] + math.cos(start_angle),
                    self.center[1] + math.sin(start_angle)) )

                points.append( (self.center[0] + math.cos(end_angle),
                    self.center[1] + math.sin(end_angle)) )

                self.draw.polygon(points, outline=self._levels(bn), fill=self._levels(bn))

                point_a = points[1]
                point_b = points[2]
                r += 1
            else:
                # we just need two more points to draw the next bin
                points = []
                points.append(
                    (self.center[0] + ((r + 1) * math.cos(start_angle)),
                    self.center[1] + ((r + 1) * math.sin(start_angle)) )
                )

                points.append(
                    (self.center[0] + ((r + 1) * math.cos(end_angle)),
                    self.center[1] + ((r + 1) * math.sin(end_angle)) )
                )

                points.append( point_a )
                points.append( point_b )
                self.draw.polygon(points, outline=self._levels(bn), fill=self._levels(bn))
                r += 1

                point_a = points[0]
                point_b = points[1]
