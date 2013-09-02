from generic import Generic
import struct, bz2, tempfile
import pprint
import numpy

class p94(Generic):
    product_description_fields = ['latitude', # i
            'longitude', # i
            'height_ft', # h
            'product_code', # h
            'operational_mode', # h
            'vol_cov_pattern', # h
            'seq_number', # h
            'vol_scan_number', # h
            'vol_scan_date', # h
            'vol_scan_time', # i
            'generation_date', # h
            'generation_time', # i
            # 4x
            'elevation_number', # h
            'elevation_angle', # h
            'threshold_minimum', # h
            'threshold_increment', # h
            'threshold_levels', # h
            # 26x
            'max_reflectivity', # h
            # 6x
            'compression_method', # h
            'uncompressed_data_size', # i
            'version', # b
            'spot_blank', # b
            'offset_to_symbology', # i
            'offset_to_graphic', # i
            'offset_to_tabular'] # i
    product_description_format = '>2x2i7hihi4x5h26xh6xhi2b3i'

    symbology_fields = ['block_id',
            'block_length',
            'layers_number']
    symbology_format = '>xxhih'

    layer_fields = ['length']
    layer_format = '>i'

    data_fields = ['packet_code',
            'first_bin_index',
            'number_bins',
            'center_i',
            'center_j',
            'elevation_cosine',
            'number_radials']
    data_format = '>7h'

    radial_fields = ['number_bytes', 'start_angle', 'delta_angle']
    radial_format = '>3h'

    def decode_symbology(self):
        f = self.handle

        f.seek(self.symbology_offset)

        product_size = self.product['message_header']['message_length'] \
                - struct.calcsize(self.message_header_format) \
                - struct.calcsize(self.product_description_format)
        
        self.tmp_handle = tempfile.TemporaryFile()

        self.tmp_handle.write(bz2.decompress(f.read(product_size)))

        f = self.tmp_handle

        f.flush()

        self.product['symbology'] = self.read_section(0, self.symbology_format, self.symbology_fields, handle=f)

        self.product['symbology']['layers'] = []

        layer_offset = 12
        layer_format_size = struct.calcsize(self.layer_format)

        for i in range(self.product['symbology']['layers_number']):
            layer = self.read_section(layer_offset, self.layer_format, self.layer_fields, handle=f)

            layer['data'] = self.read_section(f.tell(), self.data_format, self.data_fields, handle=f)
            layer['data']['radials'] = []


            #todo make a 2d array from radials and levels, store angle data in matching list
            for j in range(layer['data']['number_radials']):
                radial = self.read_section(f.tell(), self.radial_format, self.radial_fields, handle=f)

                radial['levels'] = numpy.ndarray(shape=(radial['number_bytes'],), dtype=numpy.dtype('int8'), buffer=f.read(radial['number_bytes']))
                layer['data']['radials'].append(radial)

            self.product['symbology']['layers'].append(layer)

    def close(self):
        self.handle.close()
        self.tmp_handle.close()
