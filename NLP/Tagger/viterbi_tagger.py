# viterbi

import sys
import re
import math
from checker import get_type
#function for generating the tag set S and the emission
def gen_prior(inputf):
        f_in = open(inputf, 'r')
        tbl_prior = {}  
        taggs = set(['*', 'STOP'])
        pattern = re.compile('(\S+)\s(\S+)\s(\S+)')
        for line in f_in:
                match = pattern.match(line)
                if match:
                        word = match.group(3)
                        tag = match.group(2)
                        val = math.log(float(match.group(1)))
                        if word in tbl_prior:
                                tbl_prior[word][tag] = val
                        else:
                                tbl_prior[word] = {tag:val}
                        taggs.add(tag)
        f_in.close()
        return (tbl_prior, taggs)

#function for generating the trigrams
def gen_tri(inputf):
        f_in = open(inputf, 'r')
        tbl = {}
        pattern = re.compile('(\S+)\s(\S+)\s(\S+)\s(\S+)')
        for line in f_in:
                match = pattern.match(line)
                if match:
                        tbl[match.group(1),match.group(2),match.group(3)] = float(match.group(4))
        f_in.close()
        return tbl

#the viterbi algorithm
#x: the input sentence
#S: the tag set
#q: the trigram
#w: the emission
#opt_type: type of replacement
def viterbi(x, S, q, e, opt_type):
        n = len(x)
        #initialization for the DP
        pi = {(-1,'*','*'):0}
        trace = {(-1,'*','*'):[]}
        for u in S:
                for v in S:
                        if u == '*' and v == '*':
                                continue
                        pi[-1,u,v] = float('-inf') 
                        trace[-1,u,v] = []
        for k in range(0, n): 
                x_k = x[k]
                if x_k not in e:
                        #replace for the rare words
                        x_k = get_type(x_k, opt_type)
                for u in S:
                        for v in S:
                                max_prob = float('-inf');
                                max_w = ''
                                e_xv = float('-inf')
                                if v in e[x_k]:
                                        e_xv = e[x_k][v]
                                for w in S:
                                        q_wuv = float('-inf')
                                        pi_kwu = float('-inf')
                                        if (w,u,v) in q:
                                                q_wuv = q[w,u,v]
                                        if (k-1,w,u) in pi:
                                                pi_kwu = pi[k-1,w,u]
                                        #update the new probability
                                        tmp_prob = pi_kwu + q_wuv + e_xv
                                        #find argmax_w
                                        if tmp_prob > max_prob:
                                                max_prob = tmp_prob
                                                max_w = w
                                if max_w != '':
                                        tl = list(trace[k-1,max_w,u])
                                        tl.append((max_w,max_prob))
                                        trace[k,u,v] = tl 
                                        pi[k,u,v] = max_prob
        cand_u = ''
        cand_v = ''
        max_prob = float('-inf')
        #find argmax_uv(pi(n-1,u,v)q('STOP'|u,v))
        for u in S:
                for v in S:
                        q_wuv = float('-inf')
                        pi_kuv = float('-inf')
                        if (u,v,'STOP') in q:
                                q_wuv = q[u,v,'STOP']
                        if (n-1,u,v) in pi:
                                pi_kuv = pi[n-1,u,v]
                        tmp_prob = pi_kuv + q_wuv
                        if tmp_prob > max_prob:
                                max_prob = tmp_prob
                                cand_u = u
                                cand_v = v
        taglist = list(trace[n-1,cand_u,cand_v])
        taglist.append((cand_u, 'misc'))
        taglist.append((cand_v, 'misc'))
        #find the trace of the tags
        out = ''
        for k in range(0, n - 1):
                out = out + x[k] + ' ' + taglist[k+2][0] + ' ' + str(taglist[k][1]) + '\n'
        out = out + x[n - 1] + ' ' + cand_v + ' ' + str(max_prob) + '\n'
        return out
#arg1: log emission probability of words and tags       
#arg2: log trigram probability 
#arg3: the input set of sentences
#arg4: the result words with tages
#arg5: the type of replacement
if __name__ == "__main__":
        (prior_tbl, tag_set) = gen_prior(sys.argv[1])
        tri_tbl = gen_tri(sys.argv[2]) 
        passage = open(sys.argv[3], 'r')
        f_out = open(sys.argv[4], 'w')
        opt_type = sys.argv[5]
        sentence = []
        for line in passage:
                line=line.strip('\n')
                if(len(line) == 0):
                        #run the viterbi algorithm
                        f_out.write(viterbi(sentence, tag_set, tri_tbl, prior_tbl, opt_type) + '\n')
                        sentence = []
                else:
                        sentence.append(line)
        passage.close()
        f_out.close()
