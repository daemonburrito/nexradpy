from generic import Generic
import struct, bz2, tempfile
import pprint
import numpy

class p58(Generic):
    data_fields = ['packet_code',
            'block_length',
            'i',
            'j']
    data_format = '>4h'

    def decode_symbology(self):
        f = self.handle

        f.seek(self.symbology_offset)

        product_size = self.product['message_header']['message_length'] \
                - struct.calcsize(self.message_header_format) \
                - struct.calcsize(self.product_description_format)

        self.product['symbology'] = self.read_section(self.symbology_offset, self.symbology_format, self.symbology_fields, handle=f)

        self.product['symbology']['layers'] = []

        layer_offset = self.symbology_offset + 12
        layer_format_size = struct.calcsize(self.layer_format)

        for i in range(self.product['symbology']['layers_number']):
            layer = self.read_section(layer_offset, self.layer_format, self.layer_fields, handle=f)

            layer['data'] = self.read_section(f.tell(), self.data_format, self.data_fields, handle=f)
            layer['data']['data_packets'] = []

            print f.tell()

            for j in range(layer['data']['block_length']):
                layer['data']['data_packets'].append(f.read(1))
            #todo make a 2d array from radials and levels, store angle data in matching list
            #for j in range(layer['data']['number_radials']):
            #    radial = self.read_section(f.tell(), self.radial_format, self.radial_fields, handle=f)

            #    radial['levels'] = numpy.ndarray(shape=(radial['number_bytes'],), dtype=numpy.dtype('int8'), buffer=f.read(radial['number_bytes']))
            #    layer['data']['radials'].append(radial)

            self.product['symbology']['layers'].append(layer)

    def decode_graphic(self):
        pass

    def decode_tabular(self):
        pass
