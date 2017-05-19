#!/usr/bin/env python3
import os
import sys
import struct
import tiff
import lzw

class NotTiffFileError(Exception):
    pass


class IFD():

    def __init__(self, ftype, count, value):
        self.ftype = ftype
        self.count = count
        self.value = value


def read_tiff(filename):
    with open(filename, 'rb') as f:
        #reading byte order
        data = f.read(2)
        if data == b'II':
            byte_order = '<'
        elif data == b'MM':
            byte_order = '>'
        else:
            raise NotTiffFileError
        is_tiff, idf_addr = struct.unpack('{}hl'.format(byte_order), f.read(6))
        #reading ifd entries
        f.seek(idf_addr)
        ifd_count = struct.unpack('{}h'.format(byte_order), f.read(2))[0]
        ifd_list = {}

        for i in range(0, ifd_count):
            tiff_tag, tiff_ftype, tiff_count, tiff_value = struct.unpack('{}HHLL'.format(byte_order), f.read(12))
            ifd_list[tiff_tag] = IFD(tiff_ftype, tiff_count, tiff_value)

        #reading small_tiff entry

        f.seek(ifd_list[273].value)

        length = ifd_list[279].value
        data = f.read(length)
        
        raw_data = list(struct.unpack('{}{}B'.format(byte_order, length), data))
        unpacked_data = lzw.unpack_bits(raw_data, 9)
        decompressed_data = lzw.decompress(unpacked_data)
        unpack_bit = '\n'.join(['{:008b}'.format(d) for d in decompressed_data])
        print(unpack_bit)
#        decompressed_data = [elem.encode('hex') for elem in lzw.decompress(compressed_data)]
#        print(decompressed_data)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        abs_file = os.path.join(os.curdir, sys.argv[1])
        if os.path.isfile(abs_file):
            read_tiff(abs_file)
        else:
            print('file does not exist')


    else:
        print('please specify file')

