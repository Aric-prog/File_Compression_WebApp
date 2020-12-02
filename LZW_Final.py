from bitarray import bitarray
import os
import sys

from io import StringIO

def LZWCompress(inputString):
    dictSize = 256
    dictionary = {chr(i): i for i in range(dictSize)}
    # print(dictionary)
    firstChar = inputString[0]
    nextChar = ""
    result = []
    # print("Before compression:", len(inputString))

    for i in range(len(inputString)):
        if i != len(inputString) - 1:
            nextChar += inputString[i + 1]
        if firstChar + nextChar in dictionary:
            firstChar += nextChar
        else:
            # print(firstChar, dictionary[firstChar], firstChar + nextChar, dictSize)
            result.append(dictionary[firstChar])
            dictionary[firstChar + nextChar] = dictSize
            dictSize += 1
            firstChar = nextChar
        nextChar = ""
    result.append(dictionary[firstChar])
    return result

def run(string):
    output_buffer = bitarray(endian='big')
    result = LZWCompress(string)
    with open('BryanOutput.bin','wb')as w:
        for i in result:
            if(i < 256):
                output_buffer.append(True)
                output_buffer.frombytes(i.to_bytes(1,'big'))
            else:
                output_buffer.append(False)
                output_buffer.frombytes((i - 255).to_bytes(1,'big'))
        w.write(output_buffer.tobytes())

string = "mahi magi magi mahi mahi hello mahi madi mahi mahi mahi facebook hello world mahi magi magi mahi mahi hello mahi madi mahi mahi mahi facebook hello world mahi magi magi mahi mahi hello mahi madi mahi mahi mahi facebook hello world "
uncompressed = "KDW UIAJDOIAWUOIDUHAWOIAUHWDOIAUHDOIAUHDOIAWUHDOIUH WOIUHD AWOUIHD  AOIWhu daw"

def list_to_str(compressed):

    # Build the dictionary.
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    # print(dictionary)

    # StringIO is used when you have some API that only takes files, but you need to use a string.
    # StringIO is considerably faster if we are dealing with multiple megabytes of character-data
    # when compared to expressions like mystr += "more stuff\n" within a loop
    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    firstChar = chr(compressed.pop(0))
    result.write(firstChar)
    for decimalOfaChar in compressed:
        # if 65 in dictionary entry = dictionary[65] = A
        # stringEntry = "A"
        # result = "AA"  dictionary[256] = "AA" an so on
        if decimalOfaChar in dictionary:
            stringEntry = dictionary[decimalOfaChar]
        elif decimalOfaChar == dict_size:
            # if we find a decimal baru yang barusan dimasukin ke dictionary cth during a loop we found D|D|D
            stringEntry = firstChar + firstChar[0]
            # printing to check how it works
            # print(stringEntry)
        else:
            raise ValueError('Bad compressed k: %s' % decimalOfaChar)
        result.write(stringEntry)
        # printing to keep track of the algo
        # print(result.getvalue())

        # add new char in the dictionary
        dictionary[dict_size] = firstChar + stringEntry[0]
        dict_size += 1
        firstChar = stringEntry

    # print(dictionary)
    return result.getvalue()

def decompress(filename):
    ba = bitarray(endian ='big')
    with open(os.path.join(sys.path[0],filename), 'rb') as f:
        ba.fromfile(f)

    output_list = []
    output = ba.to01()
    length = len(output)
    i = 9 
    while(length - 9 > 9):
        current_element = output[i - 9 : i]
        i += 9
        length -= 9

        if(int(current_element[0])):
            output_list.append(int(current_element[1:] , 2))
        else:
            output_list.append(int(current_element[1:] , 2) + 255)
    return list_to_str(output_list)


run(string)
print(decompress("BryanOutput.bin"))
