import sys
import re
import math
#input_str: target string for replacement
#opt_type: the type for replacement
def get_type(input_str, opt_type):
        if opt_type == 'opt':
                #for the words with more than 2 characters and only have capitals
                p_cap_all = re.compile('^[A-Z][A-Z]+$')
                match = p_cap_all.match(input_str)
                if match: 
                        return '_CAPALL_'
                #for the words with the capital headers
                p_cap_fst = re.compile('^[A-Z][A-Za-z]+$')
                match = p_cap_fst.match(input_str)
                if match:
                        return '_CAPFST_'
                #for the single capital character 
                p_cap = re.compile('^[A-Z]$')
                match = p_cap.match(input_str)
                if match:
                        return '_CAP_'
                #for the numbers
                p_num = re.compile('^[0-9]+$')
                match = p_num.match(input_str)
                if match:
                        return '_NUM_'
                #for the words with only capitals and dots. Such as I.B.M.
                p_org = re.compile('^[A-Z\.]*\.[A-Z\.]*$')
                if match:
                        return '_ORG_'
        return '_RARE_' 
