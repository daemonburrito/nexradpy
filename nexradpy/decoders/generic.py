import struct, sys, os, pprint

class Generic():
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

    message_header_format = '>2h2i3h'
    product_description_format = '>2x2i7hihi4xh48x2b3i'

    def __init__(self):
        self.product = {}
        self.product['header'] = ''

    def load(self, f):
        self.handle = f

        c = f.read(1)
        while (ord(c) != 0):
            self.product['header'] += c
            c = f.read(1)

        self.message_header_offset = f.tell() - 1

    def load_file(self, filespec):
        try:
            self.handle = open(filespec, 'rb')
            f = self.handle

            c = f.read(1)

            while (ord(c) != 0):
                self.product['header'] += c
                c = f.read(1)

            self.message_header_offset = f.tell() - 1

        except IOError:
            print "Couldn't load file"

    def decode(self):
        self.decode_message_header()

        self.decode_product_description()

        if (self.product['description']['offset_to_symbology'] != 0) :
            self.decode_symbology()
        if (self.product['description']['offset_to_graphic'] != 0) :
            self.decode_graphic()
        if (self.product['description']['offset_to_tabular'] != 0) :
            self.decode_tabular()

        return self.product

    def decode_message_header(self):
        self.product['message_header'] = self.read_section(self.message_header_offset, self.message_header_format, self.message_header_fields)

        self.product_description_offset = self.handle.tell()

    def decode_product_description(self):
        self.product['description'] = self.read_section(self.product_description_offset, self.product_description_format, self.product_description_fields)

        if (self.product['description']['offset_to_symbology'] != 0):
            self.symbology_offset = (self.product['description']['offset_to_symbology'] * 2) + self.message_header_offset
        
        if (self.product['description']['offset_to_graphic'] != 0):
            self.graphic_offset = (self.product['description']['offset_to_graphic'] * 2) + self.message_header_offset

        if (self.product['description']['offset_to_tabular'] != 0):
            self.tabular_offset = (self.product['description']['offset_to_tabular'] * 2) + self.message_header_offset

    def decode_symbology(self):
        pass
    def decode_graphic(self):
        pass
    def decode_tabular(self):
        pass

    def read_section(self, offset, format_str, fields, **kwargs):
        container = {}
        size = struct.calcsize(format_str)

        handle = kwargs.get('handle', self.handle)
        string = kwargs.get('string', False)

        if (not(string)):
            f = handle
            f.seek(offset)
            s = f.read(size)
            d = struct.unpack(format_str, s)
        else:
            d = struct.unpack(format_str, string[offset:size+offset])

        for a, b in zip(fields, d):
            container[a] = b

        return container

    def close(self):
        self.handle.close()
