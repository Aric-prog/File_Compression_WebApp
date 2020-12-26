import sys
import os
from bitarray import bitarray
class LZ77():
    def LZ77(self,search,lookAhead):
        best_length = 0
        best_offset = 0
        best_char = lookAhead[0]

        # Merge both strings 
        full = search + lookAhead

        # Points to the start of the look ahead buffer.
        lookAheadIndex = len(search)
        fullLength = len(full)
        for i in range(lookAheadIndex):
            candidate_length = 0
            candidate_char = ""

            # Go through the search and look ahead buffer, stopping when the letters stops matching,
            # or when either buffer is exhausted.
            while(full[i + candidate_length] == full[lookAheadIndex + candidate_length] and candidate_length < 15):
                # Candidate length is used for storing match length, and iterating through both buffer. 
                candidate_length += 1

                # Stores char to be outputted.
                if(lookAheadIndex + candidate_length == fullLength):
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


    def compress(self,input_buffer,output_buffer):
        i = 0
        window_size = 4095
        look_size = 15
        
        
        with open((os.path.join("output/", "LZ77_Compressed.lz77")),'wb') as out:
            while(i < len(input_buffer)):
                search = input_buffer[:i]
                lookAhead = input_buffer[i:]

                offset_and_length = 0

                if(len(search) > window_size):
                    search = search[i - window_size:]
                if(len(lookAhead) > window_size):
                    lookAhead = lookAhead[:i + look_size]

                result = self.LZ77(search,lookAhead)

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
                    output_buffer.frombytes(result[2].to_bytes(1,'big'))

                    i += 1
            out.write(output_buffer.tobytes())
        return "LZ77_Compressed.lz77"

    def decompress(self, input_buffer,extension):
        # print(pair)
        # Todo change output to byte IO
        output = bytearray("",encoding = 'utf-8')
        length = len(input_buffer)

        print("DECOMPRESS\n")
        with open((os.path.join("output/", ("LZ77_Decompressed." + extension))),'wb') as out:
            while(length >= 9):
                # Case true :
                if(input_buffer.pop(0)):
                    offset_and_length = int.from_bytes(input_buffer[:16].tobytes(),'big') 
                    offset = offset_and_length >> 4
                    match_length = offset_and_length - (offset << 4)
                    start_pos = len(output) - offset

                    output += output[start_pos : start_pos + match_length]
                    del input_buffer[:16]
                    length -= 17
                else:
                    element = input_buffer[:8].tobytes()
                    del input_buffer[:8]
                    length -= 9
                    output += element
                    # print(output)
            out.write(output)
        return "LZ77_Decompressed." + extension
