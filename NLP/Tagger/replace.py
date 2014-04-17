# replace word(count<5) --> _RARE_

import sys
import re
from checker import get_type

# argument1: input file: original file
# argument2: output file: replaced file
# argument3: switch for the advanced replacement for the rare words

if __name__ == "__main__":
        f_in = open(sys.argv[1], 'r')
        f_out = open(sys.argv[2], 'w')
        opt_type = sys.argv[3];
        tbl = {}
        pattern = re.compile('(\S+)\s(\S+)')
        for line in f_in:
                match = pattern.match(line)
                if match:
                        word = match.group(1)
                        if word in tbl:
                                tbl[word] = tbl[word] + 1 
                        else:
                                tbl[word] = 1
        f_in.seek(0, 0)
        for line in f_in:
                match = pattern.match(line)
                if match:
                        word = match.group(1)
                        #check the word frequency and process the replacement
                        if tbl[word] < 5:
                                f_out.write( get_type(word, opt_type) + ' ' + match.group(2) + '\n')
                        else:
                                f_out.write(line)
                else:
                        f_out.write(line)
        f_in.close()
        f_out.close()
