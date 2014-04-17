# output log probability of triagram

import sys
import re
import math

# argument1: the input counts of words and grams
# argument2: the result file of trigram.
#            Format: [tag1] [tag2] [tag3] [log p(tag3|tag1, tag2)]

def gen_count(inputf):
        f_in = open(inputf, 'r')
        tbl = {}
        #find the lines that of grams
        pattern = re.compile('(\d+)\s(?:1-GRAM|2-GRAM|3-GRAM)\s(.*)')
        for line in f_in:
                match = pattern.match(line)
                if match:
                        tbl[match.group(2)] = match.group(1) 
        f_in.close()
        return tbl

if __name__ == "__main__":
        tbl = gen_count(sys.argv[1])
        f_in = open(sys.argv[1], 'r')
        f_out = open(sys.argv[2], 'w')
        #find the lines that has the 3-grams
        pattern = re.compile('(\d+)\s3-GRAM\s((\S+\s\S+)\s\S+)')
        for line in f_in:
                match = pattern.match(line)
                if match:
                        f_out.write(match.group(2) + ' ' + str(math.log(float(match.group(1))/float(tbl[match.group(3)]))) + '\n');
        f_in.close()
        f_out.close()
