from bitarray import bitarray

import os
import sys
import binascii
string = "mahi magi magi mahi mahi hello mahi madi mahi mahi mahi facebook hello world mahi magi magi mahi mahi hello mahi madi mahi mahi mahi facebook hello world mahi magi magi mahi mahi hello mahi madi mahi mahi mahi facebook hello world "
newString = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus sollicitudin risus sit amet tincidunt fermentum. Mauris fringilla arcu id nisi posuere, vitae imperdiet risus rhoncus. Curabitur varius nunc quis diam lobortis feugiat. Nam eros ex, pretium id suscipit vitae, scelerisque et tellus. Cras tincidunt accumsan ultricies. Aliquam feugiat diam massa, in posuere leo imperdiet fringilla. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus."
newnew = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
abra = "mahi magi magi mahi mahi hello "
# Accepts string arguments for both search and look ahead.
# Returns a tuple output containing (offset, match_length, character) 

def LZ77(search,lookAhead):
    best_length = 0
    best_offset = 0
    best_char = lookAhead[0]
    
    # Merge both strings 
    full = search + lookAhead

    # Points to the start of the look ahead buffer.
    lookAheadIndex = len(search)
    for i in range(len(search)):
        candidate_length = 0
        candidate_char = ""
        
        # Go through the search and look ahead buffer, stopping when the letters stops matching,
        # or when either buffer is exhausted.
        while(full[i + candidate_length] == full[lookAheadIndex + candidate_length] and candidate_length < 15):
            # Candidate length is used for storing match length, and iterating through both buffer. 
            candidate_length += 1

            # Stores char to be outputted.
            if(lookAheadIndex + candidate_length == len(full)):
                candidate_length -= 1
                candidate_char = lookAhead[-1]
                break
            candidate_char = full[lookAheadIndex + candidate_length]
            if(i + candidate_length >= lookAheadIndex):
                candidate_char = full[lookAheadIndex + (candidate_length - 1)]
                break
            
    
        # Finds the longest match length and lowest offset.
        if(best_length < candidate_length and candidate_length > 1):
            best_length = candidate_length
            best_offset = lookAheadIndex - i
            best_char = candidate_char
        elif(best_length == candidate_length):
            new_offset = lookAheadIndex - i
            if(new_offset < best_offset):
                best_offset = new_offset

    return best_offset,best_length, best_char


# Run the LZ77 algorithm, accepts a string argument.
def compress(string):
    pair = 0
    i = 0
    window_size = 4095
    look_size = 15
    output_buffer = bitarray(endian='big')

    with open("output.bin",'wb') as out:
        while(i < len(string)):
            search = string[:i]
            lookAhead = string[i:]

            offset_and_length = 0

            if(len(search) > window_size):
                search = search[i - window_size:]
            if(len(lookAhead) > window_size):
                lookAhead = lookAhead[:i + look_size]

            result = LZ77(search,lookAhead)
            # print(search , lookAhead)
            # print(result)

            offset_and_length += result[0] << 4
            offset_and_length += result[1]

            if(result[1] > 1):
                # offset and then length
                output_buffer.append(True)
                output_buffer.frombytes(offset_and_length.to_bytes(2,'big'))
                
                i += result[1]
            else:
                # Write raw char because it saves more space.
                output_buffer.append(False)
                print("{0:b}".format(int(result[2] , 16)).zfill(4))
                output_buffer.frombytes(bytes(result[2],'utf-8'))

                i += 1
            pair += 1
        print(pair)
        out.write(output_buffer.tobytes())

def decompress():
    # print(pair)
    input_buffer = bitarray(endian = 'big')
    with open("output.bin",'rb') as r:
        input_buffer.fromfile(r)
    
    output = ""
    length = len(input_buffer)
    while(length >= 9):
        # Case true :
        if(input_buffer.pop(0)):
            offset_and_length = int.from_bytes(input_buffer[:16].tobytes(),'big') 
            offset = offset_and_length >> 4

            match_length = offset_and_length - (offset << 4)

            start_pos = len(output) - offset
            
            # print("(",offset,match_length,")")
            # print(start_pos)
            # print(output)
            output += output[start_pos : start_pos + match_length]
            del input_buffer[:16]
            length -= 17
        else:

            element = chr(int.from_bytes(input_buffer[:8].tobytes(),'big'))
            del input_buffer[:8]
            length -= 9
            output += element
            
    print(output == newString)



# print(LZ77(newString[:1],newString[1:]))
# print(newString[:1] , newString[1:])
# print(len(newString[:0]))

with open(os.path.join(sys.path[0],"kobe.py"),'rb') as f:
    content = f.read()
s = binascii.hexlify(content)

hex = str(binascii.hexlify(content), 'ascii')
formatted_hex = ''.join(hex[i:i+2] for i in range(0, len(hex), 2))
# print(formatted_hex)
compress(formatted_hex)
decompress()