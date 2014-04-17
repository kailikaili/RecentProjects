# Compute emission parameters

import sys
import re
import math
def gen_count(inputf):
        f_in = open(inputf, 'r')
        tbl = {}
        #find the patterns of grams
        pattern = re.compile('(\d+)\s(?:1-GRAM|2-GRAM|3-GRAM)\s(.*)')
        for line in f_in:
                match = pattern.match(line)
                if match:
                        tbl[match.group(2)] = match.group(1) 
        f_in.close()
        return tbl
#arg1: the name of the input file(count of the words and grams)
#arg2: output the prior observation format: [probability] [word] [tag]
if __name__ == "__main__":
        f_in = open(sys.argv[1], 'r')
        f_out = open(sys.argv[2], 'w')
        tbl = gen_count(sys.argv[1])
        #find the patterns of words
        pattern = re.compile('(\d+)\sWORDTAG\s(\S+)\s(.*)')
        for line in f_in:
                match = pattern.match(line)
                if match:
                        f_out.write(str(float(match.group(1))/float(tbl[match.group(2)])) + ' ' + match.group(2) + ' ' + match.group(3) + '\n')
        f_in.close()
        f_out.close()
