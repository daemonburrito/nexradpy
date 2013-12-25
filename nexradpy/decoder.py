"""Nexradpy Decoder.
Returns appropriate decoder for file type."""
from nexradpy.decoders import generic
from nexradpy.decoders import p94, p58
import struct
import logging

logging.basicConfig(filename='nexradpy-decoder.log', level=logging.DEBUG)
logging.info('Started decoder')

def load_file(filespec):
    """Load a file. Returns decoder."""
    try:
        fh = open(filespec, 'rb')

    except IOError:
        print "Couldn't load file"

    code = get_product_code(fh)

    if (code == 94):
        decoder = p94.p94()
    elif (code == 58):
        decoder = p58.p58()
    else:
        decoder = generic.Generic()

    logging.info('Loading decoder {0}.'.format(decoder.__class__))
    decoder.load(fh)

    return decoder

def get_product_code(fh):
    """Given a file handle, determines product type."""
    char = fh.read(1)

    while (ord(char) != 0):
        char = fh.read(1)

    fh.seek(-1, 1)
    code = struct.unpack('>h', fh.read(2))

    fh.seek(0)
    return code[0]
