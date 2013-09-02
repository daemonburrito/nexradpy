class NexradpyError(Exception):
    pass

class OutputFilter:
    """Base class for output filters."""

    def filter(self, p):
        pass
