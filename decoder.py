import struct, sys, os
import decoders.p94

class Decoder():
    message_offset = 0
    message_header_fields = ['message_code',
            'message_date',
            'message_time',
            'message_length',
            'source_id',
            'destination_id',
            'blocks_number']

    product_description_fields = ['latitude',
            'longitude',
            'height_ft',
            'product_code',
            'operational_mode',
            'vol_cov_pattern',
            'seq_number',
            'vol_scan_number',
            'vol_scan_date',
            'vol_scan_time',
            'generation_date',
            'generation_time',
            'elevation_number',
            'version',
            'spot_blank',
            'offset_to_symbology',
            'offset_to_graphic',
            'offset_to_tabular']

    header_format = '>2h2i3h'
    product_description_format = '>2x2i7hihi4xh48x2b3i'

    def __init__(self):
        self.header = ''

    def load_file(self, filespec):
        try:
            self.handle = open(filespec, 'rb')
            f = self.handle

            c = f.read(1)

            while (ord(c) != 0):
                self.header += c
                c = f.read(1)

            self.message_offset = (f.tell() - 1)

        except IOError:
            print "Couldn't load file"

    def decode(self):
        self.decode_message_header()

        if self.message_header['message_code'] == 94:

            self.__class__ = decoders.p94.p94

        self.decode_product_description()

    def decode_message_header(self):
        f = self.handle
        f.seek(self.message_offset)
        s = f.read(struct.calcsize(self.header_format))
        d = struct.unpack(self.header_format, s)

        self.message_header = {}
        for a, b in zip(self.message_header_fields, d):
            self.message_header[a] = b

    def decode_product_description(self):
        f = self.handle

        s = f.read(struct.calcsize(self.product_description_format))
        d = struct.unpack(self.product_description_format, s)

        self.product_description = {}
        for a, b in zip(self.product_description_fields, d):
            self.product_description[a] = b

        self.symbology_offset = (self.product_description['offset_to_symbology'] + self.message_offset) * 2

    def close(self):
        self.handle.close()

if __name__ == "__main__":
    decoder = Decoder()
    decoder.load_file(sys.argv[1])
    decoder.decode()

    print decoder.header

    print decoder.message_header

    print decoder.product_description

    decoder.close()
