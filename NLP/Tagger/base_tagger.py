# base tagger, tag y* = argmax e(x|y)

# argument1: the name of the input file (prior.dat)
# argument2: test file name. format: word
# argument3: output file name. format: word\stag

import sys
import re
import math
from checker import get_type
def gen_prior(inputf):
        f_in = open(inputf, 'r')
        tbl = {}
        pattern = re.compile('(\S+)\s(\S+)\s(\S+)')
        for line in f_in:
                match = pattern.match(line)
                if match:
                        word = match.group(3)
                        tag = match.group(2)
                        val = math.log(float(match.group(1)))
                        if word in tbl:
                                tbl[word][tag] = val 
                        else:
                                tbl[word] = {tag:val}
        f_in.close()
        return tbl

if __name__ == "__main__":
        prior_tbl = gen_prior(sys.argv[1])
        test = open(sys.argv[2], 'r')
        output = open(sys.argv[3], 'w')
        for line in test:
                line=line.strip('\n')
                if len(line) == 0:
                        output.write('\n')
                        continue
                alias = line
                if alias not in prior_tbl:
                        #using get_types to assign a new value for rare words(in this case it is '_RARE_')
                        alias = get_type(alias, '')
                val = float('-inf')
                tag = ''
                cand_set = prior_tbl[alias]
                #find the tag with maximal emission probability
                for cand in cand_set: 
                        tmp_max = cand_set[cand] 
                        if tmp_max > val:
                                val = tmp_max 
                                tag = cand 
                output.write(line + ' ' + tag + ' ' + str(val) + '\n')
        test.close()
        output.close()
            

