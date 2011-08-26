import decoder

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
            # 26x?
            'max_reflectivity', # h
            # 6x?
            'compression_method', # h
            'uncompressed_data_size', # i
            'version', # b
            'spot_blank', # b
            'offset_to_symbology', # i
            'offset_to_graphic', # i
            'offset_to_tabular'] # i

    product_description_format = '>2x2i7hihi4x5h26xh6xhi2b3i'
