from decoders import generic
from decoders import p94
import struct

def load_file(filespec):
    try:
        f = open(filespec, 'rb')

    except IOError:
        print "Couldn't load file"

    code = get_product_code(f)

    if (code == 94):
        decoder = p94.p94()
        decoder.load(f)

    return decoder

def get_product_code(f):
    c = f.read(1)

    while (ord(c) != 0):
        c = f.read(1)

    f.seek(-1, 1)
    code = struct.unpack('>h', f.read(2))

    f.seek(0)
    return code[0]
