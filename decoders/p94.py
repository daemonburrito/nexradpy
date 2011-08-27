import decoder, struct, bz2

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
            'layers_number']

    symbology_format = '>xxhih'

    def decode_symbology(self):
        #self.product_symbology = self.read_section(self.symbology_offset, self.product_symbology_format, self.product_symbology_fields)

        f = self.handle

        print 'Message header offset: ' + str(self.message_header_offset)
        #print struct.calcsize(self.message_header_format)
        #print struct.calcsize(self.product_description_format)

        print 'Calculated symbology offset: ' + str(self.symbology_offset)

        f.seek(0)

        w = f.read(2)
        while (w != 'BZ'):
            w = f.read(2)

        print 'BZ magic at byte ' + str(f.tell() - 2)
        #print w

        f.seek(self.symbology_offset)

        product_size = self.message_header['message_length'] \
                - struct.calcsize(self.message_header_format) \
                - struct.calcsize(self.product_description_format)

        print 'Product size: ' + str(product_size)
        compressed = f.read(product_size)
        s = bz2.decompress(compressed)

        self.symbology_block = self.read_section(0, self.symbology_format, self.symbology_fields, s)
        #print struct.unpack('>hhihhi', data[0:16])
