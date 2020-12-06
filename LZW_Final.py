from bitarray import bitarray
import os
import sys

from io import StringIO,BytesIO

string = "mahi magi magi mahi mahi hello mahi madi mahi mahi mahi facebook hello world mahi magi magi mahi mahi hello mahi madi mahi mahi mahi facebook hello world mahi magi magi mahi mahi hello mahi madi mahi mahi mahi facebook hello world "
uncompressed = "KDW UIAJDOIAWUOIDUHAWOIAUHWDOIAUHDOIAUHDOIAWUHDOIUH WOIUHD AWOUIHD  AOIWhu daw"

class LZW():
    def LZWCompress(self,inputString):
        dictSize = 256
        dictionary = {i.to_bytes(1,byteorder='big'): i for i in range(dictSize)}
        # print(dictionary)

        firstChar = bytearray(inputString[0].to_bytes(1,'big'))
        result = []

        # # print("Before compression:", len(inputString))

        for i in range(len(inputString)):
            if i != len(inputString) - 1:
                nextChar = (inputString[i + 1].to_bytes(1,'big'))
            if bytes(firstChar + nextChar) in dictionary:
                firstChar += nextChar
            else:
                # print(firstChar, dictionary[firstChar], firstChar + nextChar, dictSize)
                result.append(dictionary[bytes(firstChar)])
                dictionary[bytes(firstChar + nextChar)] = dictSize
                dictSize += 1
                firstChar = bytearray(nextChar)
            nextChar = bytes(0)
        result.append(dictionary[bytes(firstChar)])
        # print(dictionary)
        return result

    def decompress(self,filename):
        ba = bitarray(endian ='big')
        with open(os.path.join(sys.path[0],filename), 'rb') as f:
            ba.fromfile(f)

        output_list = []
        output = ba.to01()
        length = len(output)
        i = 9

        while(length - 9 > 0):
            current_element = output[i - 9 : i]
            # print(current_element)
            if(int(current_element[0])):
                output_list.append(int(current_element[1:] , 2))
            else:
                output_list.append(int(current_element[1:] , 2) + 255)
            i += 9
            length -= 9
            # print(current_element)
            # print(length)
        # return list_to_str(output_list)
        return(output_list)

    def list_to_str(self,compressed):

        # Build the dictionary.
        dict_size = 256
        dictionary = {i: i.to_bytes(1,byteorder='big') for i in range(dict_size)}
        
        # print(dictionary)

        # StringIO is used when you have some API that only takes files, but you need to use a string.
        # StringIO is considerably faster if we are dealing with multiple megabytes of character-data
        # when compared to expressions like mystr += "more stuff\n" within a loop
        # use StringIO, otherwise this becomes O(N^2)
        # due to string concatenation in a loop

        result = BytesIO()
        firstChar = (compressed.pop(0)).to_bytes(1,'big')
        result.write(firstChar)
        for decimalOfaChar in compressed:
            # if 65 in dictionary entry = dictionary[65] = A
            # stringEntry = "A"
            # result = "AA"  dictionary[256] = "AA" an so on
            if decimalOfaChar in dictionary:
                stringEntry = dictionary[decimalOfaChar]
                
            elif decimalOfaChar == dict_size:
                # if we find a decimal baru yang barusan dimasukin ke dictionary cth during a loop we found D|D|D
                stringEntry = firstChar + firstChar[0].to_bytes(1,'big')
                # printing to check how it works
                # print(stringEntry)
            else:
                raise ValueError('Bad compressed k: %s' % decimalOfaChar)
            result.write(stringEntry)
            # printing to keep track of the algo
            # print(result.getvalue())

            # add new char in the dictionary
            # print(firstChar , stringEntry[0])
            dictionary[dict_size] = firstChar + stringEntry[0].to_bytes(1,'big')
            dict_size += 1
            firstChar = stringEntry

        # print(dictionary)
        with open('fuck.png','wb') as f:
            f.write(result.getvalue())

    def run_compress(self,filename):
        output_buffer = bitarray(endian='big')
        result = []

        with open((os.path.join(sys.path[0],filename)),'rb') as f:
            input_ba = bytearray(f.read())

        result = self.LZWCompress(input_ba)
        print(len(result))

        with open('LZW_Output.bin','wb')as w:
            for i in result:
                if(i < 256):
                    output_buffer.append(True)
                    output_buffer.frombytes(i.to_bytes(1,'big'))
                else:
                    output_buffer.append(False)
                    output_buffer.frombytes((i - 255).to_bytes(1,'big'))
            w.write(output_buffer.tobytes())

    def run_decompress(self,filename):
        # Make the function list to str write to file
        self.list_to_str(self.decompress(filename))


compressor = LZW()
(compressor.run_compress('test_img.png'))
# di kompres
# print(compressor.run_decompress('LZW_Output.bin'))

# compress > output > binary > dibaca > output > original



# 255 normal
# 0 1111 1111

# Maybe - 255
# 1 1111 1111 1111 1111