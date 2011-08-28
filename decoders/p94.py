import decoder, struct, bz2
import pprint
import Image, ImageDraw

class p94(decoder.Decoder):
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

    layers = []

    product_description_format = '>2x2i7hihi4x5h26xh6xhi2b3i'

    symbology_fields = ['block_id',
            'block_length',
            'layers_number',
            'layer_length']

    symbology_format = '>xxhihxxi'

    packet_fields = ['packet_code',
            'first_bin_index',
            'number_bins',
            'center_i',
            'center_j',
            'elevation_cosine',
            'number_radials',
            'bytes_per_radial',
            'start_angle',
            'delta_angle',
            'level']

    packet_format = '>10hb'

    def decode_symbology(self):
        f = self.handle

        f.seek(self.symbology_offset)

        product_size = self.product['message_header']['message_length'] \
                - struct.calcsize(self.message_header_format) \
                - struct.calcsize(self.product_description_format)

        compressed = f.read(product_size)
        s = bz2.decompress(compressed)

        self.symbology_block = self.read_section(0, self.symbology_format, self.symbology_fields, s)

        #layer_length = s[12:16]

        #print struct.unpack('>i', layer_length)

        packet_code = s[16:18]
        print struct.unpack('>h', packet_code)

        print struct.calcsize(self.packet_format)

        pprint.pprint(self.read_section(16, self.packet_format, self.packet_fields, s))
