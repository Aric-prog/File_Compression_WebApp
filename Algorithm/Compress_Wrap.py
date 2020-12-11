from bitarray import bitarray
from LZW_Final import LZW
from LZ77_Final import LZ77

import os 
import sys

def read4(filename):
    input_buffer = bitarray(endian = 'big')
    with open((os.path.join(sys.path[0],filename)),'rb') as r:
        input_buffer.fromfile(r)
    extension = (input_buffer[:32].tobytes().decode('utf-8'))
    del input_buffer[:32]
    # print(extension)
    return input_buffer,extension

def write4(filename):
    extension = get_extension(filename)
    output_buffer = bitarray(endian='big')
    output_buffer.frombytes(bytes(extension,encoding='utf-8'))

    with open((os.path.join(sys.path[0],filename)), 'rb') as fh:
        input_buffer = bytearray(fh.read())
    # print(input_buffer)
    return input_buffer, output_buffer

def get_extension(filename):
    if(len(filename.split('.')[1]) <= 4):
        return filename.split('.')[1] + (" " * (4 - len(filename.split('.')[1])))
    else:
        return "    "

def LZ77_compress(filename):
    compressor = LZ77()
    compressor.compress(*write4(filename))

def LZ77_decompress(filename):
    decompressor = LZ77()
    decompressor.decompress(*read4(filename))
    
def LZW_compress(filename):
    compressor = LZW()
    # print(write4(filename))
    compressor.run_compress(*(write4(filename)))

def LZW_decompress(filename):
    decompressor = LZW()
    decompressor.decompress(*read4(filename))
    
# LZW_compress('test_inputs/Okayu.png')
LZW_decompress('LZW_Compressed.lzw')
# LZ77_decompress('LZ77_Compressed.lz77')
# read4('LZ77_Compressed.bin')