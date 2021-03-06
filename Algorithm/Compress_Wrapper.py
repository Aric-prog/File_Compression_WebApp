from bitarray import bitarray
from algorithm.LZW_Final import LZW
from algorithm.LZSS_Final import LZSS

import cProfile
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

def LZSS_compress(filename):
    compressor = LZSS()
    return compressor.compress(*write4(filename))

def LZSS_decompress(filename):
    decompressor = LZSS()
    return decompressor.decompress(*read4(filename))
    
def LZW_compress(filename):
    compressor = LZW()
    # print(write4(filename))
    return compressor.run_compress(*(write4(filename)))

def LZW_decompress(filename):
    decompressor = LZW()
    return decompressor.decompress(*read4(filename))
    
# cProfile.run("LZSS_compress('index.html')") 
# cProfile.run("LZW_decompress('LZW_Compressed.lzw')")