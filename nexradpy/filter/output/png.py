from . import OutputFilter, NexradpyError

class PNG(OutputFilter):
    """Outputs a PNG from a decoded product."""

    def filter(self, p):
        """Takes a product and returns a PNG."""
        try:
            for radial in p['symbology']['layers'][0]['data']['radials']:
                print radial['levels']
        except Exception as ex:
            raise NexradpyError(ex)
